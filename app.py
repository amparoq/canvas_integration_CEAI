from flask import Flask, request, render_template, redirect, url_for, abort
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

ACCESS_TOKEN = "7~aAXTMm8KY9RKRQXaMPJRDAn4mrBx6tZXBHhc4akaPEUPLhUEJFverU6zWL2vwath"

def check_deadline(assignment_id, course_id):
    deadline = get_assignment_deadline(course_id, assignment_id, ACCESS_TOKEN)
    if deadline and datetime.now() > datetime.fromisoformat(deadline):
        # Ejecuta el envío de los reportes
        get_submissions(course_id, assignment_id, ACCESS_TOKEN)

def get_submissions(course_id, assignment_id, access_token):
    url = f'https://canvas.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()  # Retorna las entregas de los estudiantes

def get_assignment_deadline(course_id, assignment_id, access_token):
    url = f'https://canvas.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    # Hacer la solicitud a la API de Canvas
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        assignment = response.json()
        return assignment.get('due_at')  # Obtiene la fecha de entrega
    else:
        print(f"Error al obtener la fecha límite: {response.status_code}")
        return None






app = Flask(__name__)

# Configura LTI
LTI_SECRET = 'secret-key'
LTI_CONSUMER_KEY = 'consumer-key'
LTI_URL = '/'

class LTIRequestValidator(RequestValidator):
    def __init__(self):
        super().__init__()
        self.client_key = LTI_CONSUMER_KEY
        self.client_secret = LTI_SECRET

    @property
    def enforce_ssl(self):
        return False

    def get_client_secret(self, client_key, request):
        return self.client_secret


validator = LTIRequestValidator()
endpoint = SignatureOnlyEndpoint(validator)

def verify_lti_request():
    uri = request.url
    http_method = request.method
    body = request.form.to_dict()
    headers_dict = dict(request.headers)

    print("URI:", uri)
    print("HTTP Method:", http_method)
    print("Body:", body)
    print("Headers:", headers_dict)

    valid, oauth_request = endpoint.validate_request(uri, http_method, body, headers_dict)
    print("Valid request:", valid)

    return valid

@app.route('/lti_launch', methods=['GET', 'POST'])
def lti_launch():
    # Verificar si es POST o GET
    if request.method == 'POST':
        if not verify_lti_request():
            abort(401)  # Si la solicitud no es válida, devuelve un error 401 (no autorizado)
        
        # Aquí procesamos los parámetros enviados por Canvas
        course_id = request.form.get('custom_canvas_course_id')
        assignment_id = request.form.get('custom_canvas_assignment_id')

        # Lógica para iniciar el chequeo del deadline
        scheduler.add_job(check_deadline, 'interval', hours=1, args=[assignment_id, course_id])
        scheduler.start()

        return "Chequeo del deadline iniciado", 200
    else:
        return "Solicitud inválida", 400


def crear_tablas():
    Base.metadata.create_all(session.bind)
    session.close()

crear_tablas()

# Este es el token que generaste manualmente
ACCESS_TOKEN = "7~AhwVwLHZH4BQMar7BzHMkFnU9G6HMt6uxfD2WHLuWHYZLv2P7XX2Le22RNrhLyWy"


@app.route('/students', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        student_name = request.form.get('name')
        if student_name:
            new_student = Student(name=student_name)
            session.add(new_student)
            session.commit()
            return redirect(url_for('create_student'))
        else:
            return 'Name is required', 400
    
    return render_template('students/create.html')

@app.route('/reports', methods=['GET'])
def get_reports():
    if request.method == 'GET':
        reports = session.query(Report).all()
        return render_template("reports/index.html", reports=reports)

@app.route('/upload_reports', methods=['GET', 'POST'])
def upload_report():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        file = request.files.get('report_pdf')

        if file and file.filename.endswith('.pdf'):
            pdf_content = file.read()

            new_report = Report(student_id=student_id, report_pdf=pdf_content)
            session.add(new_report)
            session.commit()

            return redirect("/reports")
        else:
            return 'File not allowed or no file provided', 400
    
    if request.method == "GET":
        students = session.query(Student).all()
        return render_template('reports/upload.html', students=students)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
