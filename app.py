from flask import Flask, request, jsonify, redirect, url_for, render_template
import os
import requests
from database import session, LLAVE
from models import Report, Student, Base
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import oauthlib.oauth1
from oauthlib.oauth1 import RequestValidator, SignatureOnlyEndpoint
from collections import defaultdict

scheduler = BackgroundScheduler()

# Access token para autenticar las llamadas a la API de Canvas
ACCESS_TOKEN = "7~aAXTMm8KY9RKRQXaMPJRDAn4mrBx6tZXBHhc4akaPEUPLhUEJFverU6zWL2vwath"

app = Flask(__name__)

LTI_SECRET = 'secret-key'
LTI_CONSUMER_KEY = 'consumer-key'

# Función para obtener las entregas de un assignment
def get_submissions(course_id, assignment_id, access_token):
    url = f'https://canvas.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions'
    headers = {'Authorization': f'Bearer {access_token}'}
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

    # Renderizar una página HTML para mostrar en Canvas
    return render_template('delivery.html', course_id=course_id, assignment_id=assignment_id)


# Ruta para procesar las entregas cuando el profesor presiona el botón
@app.route('/process_submissions', methods=['GET', 'POST'])
def process_submissions():
    print(request.data)
    
    course_id = request.form.get('course_id')
    assignment_id = request.form.get('assignment_id')

    print(course_id)
    print(assignment_id)

    if not course_id or not assignment_id:
        return "Course ID o Assignment ID faltante", 400

    # Obtener las entregas de Canvas usando el ID del curso y de la tarea
    submissions = get_submissions(course_id, assignment_id, ACCESS_TOKEN)

    if "error" in submissions:
        return jsonify(submissions), 400

    # Procesar las entregas aquí según sea necesario (por ejemplo, guardarlas en la base de datos)
    # Por ahora, solo devolvemos las entregas como respuesta JSON
    return jsonify(submissions), 200

# Función para crear las tablas de la base de datos
def crear_tablas():
    Base.metadata.create_all(session.bind)
    session.close()

crear_tablas()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
