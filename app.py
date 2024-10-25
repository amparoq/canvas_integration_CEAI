from flask import Flask, request, jsonify, redirect, url_for, render_template
import os
import requests
from database import session, LLAVE
from models import Report, Student, Base, Assignment
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import oauthlib.oauth1
from oauthlib.oauth1 import RequestValidator, SignatureOnlyEndpoint
from collections import defaultdict
import schedule
import time
from datetime import datetime
import threading


# Access token para autenticar las llamadas a la API de Canvas
ACCESS_TOKEN = "7~aAXTMm8KY9RKRQXaMPJRDAn4mrBx6tZXBHhc4akaPEUPLhUEJFverU6zWL2vwath"

app = Flask(__name__)

LTI_SECRET = 'secret-key'
LTI_CONSUMER_KEY = 'consumer-key'


def check_deadline(assignment):
    print(f"chequeando....{datetime.now()}")
    if datetime.now() >= assignment.due_date:
        print(f"Obteniendo submissions de assignment {assignment.id}")
        get_submissions(assignment)
        return schedule.CancelJob

# Función para obtener las entregas de un assignment
def get_submissions(assignment):
    url = f'https://canvas.instructure.com/api/v1/courses/{assignment.course_id}/assignments/{assignment.id}/submissions'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to retrieve submissions. Status code: {response.status_code}"}

# Ruta principal para manejar el lanzamiento de la herramienta LTI
@app.route('/lti_launch', methods=['POST'])
def lti_launch():
    # Capturar los parámetros enviados por Canvas
    course_id = request.form.get('custom_course_id')
    assignment_id = request.form.get('custom_assignment_id')
    
    if not course_id or not assignment_id:
        return "Course ID o Assignment ID faltante", 400

    if session.query(Assignment).filter_by(id=assignment_id, course_id=course_id).first() is not None:
        if session.query(Assignment).filter_by(id=assignment_id, course_id=course_id).first().due_date is not None:
            return render_template('delivery_done.html', course_id=course_id, assignment_id=assignment_id)

    # Renderizar una página HTML para mostrar en Canvas
    return render_template('delivery.html', course_id=course_id, assignment_id=assignment_id)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Verifica cada segundo si hay tareas pendientes

# Iniciar la tarea programada en el scheduler en el hilo principal
def schedule_check_deadline(assignment):
    # Programar la tarea
    schedule.every(1).minutes.do(lambda: check_deadline(assignment))
    print(f"Tarea programada para el assignment {assignment.id} en el curso {assignment.course_id}")

    # Iniciar el scheduler en un hilo separado
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  # Hilo se cerrará cuando la app termine
    scheduler_thread.start()

# Ruta para procesar las entregas cuando el profesor presiona el botón
@app.route('/process_submissions', methods=['GET', 'POST'])
def process_submissions():
    course_id = int(request.form.get('course_id'))
    assignment_id = int(request.form.get('assignment_id'))
    
    if not course_id or not assignment_id:
        return "Course ID o Assignment ID faltante", 400
    
    new_assignment = session.query(Assignment).filter_by(id=assignment_id, course_id=course_id).first()
    if not new_assignment:
        new_assignment = Assignment(id=assignment_id, course_id=course_id)
        session.add(new_assignment)

    url = f'https://canvas.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        assignment = response.json()
        due_at_str = assignment.get('due_at')
        due_at = datetime.strptime(due_at_str, '%Y-%m-%dT%H:%M:%SZ')
        print(f"due at: {due_at}")
        new_assignment.due_date = due_at
        session.commit()
        schedule_check_deadline(new_assignment)
    else:
        return "Hubo un error", 401

    
    return "Las entregas se enviaran cuando la tarea termine su deadline", 200

# Función para crear las tablas de la base de datos
def crear_tablas():
    Base.metadata.create_all(session.bind)
    session.close()

crear_tablas()

@app.route("/assignments")
def assignments():
    assignments = session.query(Assignment).all()
    return render_template("assignments/index.html", assignments=assignments)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
