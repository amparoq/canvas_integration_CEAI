# Investigación Hitos - Proyecto de Título 1

A continuación, se tiene un xd.


## Configuración de la base de datos

Para configurar la base de datos en MySQL, sigue los siguientes pasos:

1. Inicia sesión en MySQL:

    ```bash
    mysql -u root -p
    ```

2. Ejecuta los siguientes comandos para crear la base de datos y el usuario:

    ```sql
    -- Crear la base de datos
    CREATE DATABASE canvas_test;

    -- Crear el usuario 'amparo' y otorgarle permisos
    CREATE USER 'amparo'@'localhost' IDENTIFIED BY '1234';
    GRANT ALL PRIVILEGES ON canvas_test.* TO 'amparo'@'localhost';
    FLUSH PRIVILEGES;
    ```

3. Sal de MySQL:
    ```bash
    exit
    ```

## Generación del Token de Acceso

Para generar el Token de acceso, debes realizar los siguientes pasos:

1. **Inicia sesión en Canvas**: Ve a tu cuenta de Canvas.
2. **Accede a la Configuración**: Haz clic en tu nombre en la esquina superior derecha y selecciona "Configuración" (Settings).
3. **Genera un nuevo token**: Busca la opción de "Nuevo Token de Acceso" (New Access Token).
4. **Rellena los campos solicitados**:
    - `Purpose`: (Escribir cualquier cosa)
    - `Expires`: (Dejarlo en blanco)
5. Apretar "Generar Token" (Generate Token)
6. Se te mostrara un Token en pantalla, **copialo** y **pegalo** dentro del programa:

    ```bash
    ACCESS_TOKEN = "TOKEN_DEL_USUARIO"
    ```

## Adición de Aplicación al Curso

Para adherir la herramienta al curso, debes realizar los siguientes pasos:

1. **Accede a la Configuración**: Haz click en el curso y selecciona "Configuración" (Settings).

2. **Crea la aplicación**: Dirigete a la sección de "Aplicaciones" (Apps), luego ve a "Ver Configuraciones de Aplicaciones" (View App Configurations) y añade una aplicación (+ App).

3. **Rellena los campos solicitados**:
    - `Configuration Type`: Paste XML
    - `Name`: (Escribir cualquier cosa)
    - `Consumer Key`: 'secret-key'
    - `Shared Secret`: 'consumer-key'
    - `XML Configuration`: (Colocar el siguiente código)

```xml
<cartridge_basiclti_link xmlns="http://www.imsglobal.org/xsd/imslticc_v1p0" 
    xmlns:blti="http://www.imsglobal.org/xsd/imsbasiclti_v1p0" 
    xmlns:lticm="http://www.imsglobal.org/xsd/imslticm_v1p0" 
    xmlns:lticp="http://www.imsglobal.org/xsd/imslticp_v1p0" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://www.imsglobal.org/xsd/imslticc_v1p0 
    http://www.imsglobal.org/profile/lticp_v1p0/imslticc_v1p0.xsd">
    
    <blti:title>Enviar todas las entregas</blti:title>
    <blti:description>Una vista en la tarea que permite enviar todas las entregas a una app externa.</blti:description>
    <blti:launch_url>http://127.0.0.1:5000/lti_launch</blti:launch_url>
    
    <!-- Claves de autenticación -->
    <blti:consumer_key>consumer-key</blti:consumer_key>
    <blti:shared_secret>secret-key</blti:shared_secret>
    
    <!-- Envío de parámetros personalizados -->
    <blti:custom>
        <blti:custom_field name="custom_course_id" value="$Course.id"/>
        <blti:custom_field name="custom_assignment_id" value="$Canvas.assignment.id"/>
    </blti:custom>

    <!-- Configurar la herramienta para la vista del assignment -->
    <blti:extensions platform="canvas.instructure.com">
        <lticm:property name="privacy_level">public</lticm:property>
        <lticm:property name="tool_id">lti_tool</lticm:property>

        <!-- Mostrar el botón en la vista de la tarea -->
        <lticm:options name="assignment_view">
            <lticm:property name="enabled">true</lticm:property>
            <lticm:property name="url">http://127.0.0.1:5000/lti_launch</lticm:property> <!-- Lanza tu vista HTML -->
            <lticm:property name="text">Ver detalles del Assignment</lticm:property>
            <lticm:property name="visibility">admins,instructors</lticm:property> <!-- Visible solo para administradores e instructores -->
        </lticm:options>
    </blti:extensions>
</cartridge_basiclti_link>
```

4. **Edita la aplicación**: Una vez creada la aplicación, aprietas el símbolo de "Engranaje" que aparecerá en la derecha del nombre de la aplicación que le otorgaste y aprietas Editar (Edit).

5. **Adición de variables**: En "Campos Personalizados" (Custom Fields), colocas el siguiente código:

    ```plaintext
    custom_course_id=$Canvas.course.id
    custom_assignment_id=$Canvas.assignment.id
    ```

## 🧭 API Endpoints 🧭

1- Obtener Información de una Tarea del Curso - [GET]

- **URL**: https://canvas.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}
- **Parametros**:
    - `course_id`: ID del Curso.
    - `assignment_id`: ID del Assignment.
- **Encabezados**:
    - `Authorization`: Bearer token de acceso.
- **Descripción**: Recupera la información de una tarea específica de un curso en Canvas.
- **Respuesta**:
    - `200`: Datos JSON de la tarea.
    - `400`: Solicitud incorrecta o token inválido.
    - `404`: Tarea o curso no encontrado.
    - `500`: Error interno del servidor.

En el caso que sea correcto, se obtiene el siguiente json:

```json
{
  "id": 50641401,
  "description": "<p>xd</p>",  // Descripción HTML del contenido de la tarea
  "due_at": "2024-10-24T05:59:59Z",  // Fecha y hora de vencimiento de la tarea
  "unlock_at": "2024-10-21T06:00:00Z",  // Fecha y hora en que la tarea se desbloquea para los estudiantes
  "lock_at": "2024-10-25T05:59:59Z",  // Fecha y hora en que la tarea se bloquea y no se puede entregar más
  "points_possible": 3.0,  // Puntos posibles para la tarea
  "grading_type": "points",  // Tipo de calificación (en puntos)
  "assignment_group_id": 12657442,  // ID del grupo al que pertenece la tarea
  "grading_standard_id": null,  // ID del estándar de calificación, si existe
  "created_at": "2024-10-27T00:10:32Z",  // Fecha y hora de creación de la tarea
  "updated_at": "2024-10-27T00:14:53Z",  // Fecha y hora de la última actualización de la tarea
  "peer_reviews": false,  // Indica si se requieren revisiones por pares
  "automatic_peer_reviews": false,  // Indica si las revisiones por pares son automáticas
  "position": 3,  // Posición de la tarea en el orden del curso
  "grade_group_students_individually": false,  // Indica si se califican a los estudiantes individualmente en tareas grupales
  "anonymous_peer_reviews": false,  // Indica si las revisiones por pares son anónimas
  "group_category_id": null,  // ID de la categoría de grupo, si existe
  "post_to_sis": false,  // Indica si la tarea se publica en el sistema de información de estudiantes
  "moderated_grading": false,  // Indica si la calificación es moderada
  "omit_from_final_grade": false,  // Indica si la tarea se omite del cálculo de la calificación final
  "intra_group_peer_reviews": false,  // Indica si hay revisiones por pares dentro de grupos
  "anonymous_instructor_annotations": false,  // Indica si las anotaciones del instructor son anónimas
  "anonymous_grading": false,  // Indica si la calificación es anónima
  "graders_anonymous_to_graders": false,  // Indica si los calificadores son anónimos entre sí
  "grader_count": 0,  // Número de calificadores asignados
  "grader_comments_visible_to_graders": true,  // Indica si los comentarios de los calificadores son visibles para otros calificadores
  "final_grader_id": null,  // ID del calificador final, si existe
  "grader_names_visible_to_final_grader": true,  // Indica si los nombres de los calificadores son visibles para el calificador final
  "allowed_attempts": -1,  // Número de intentos permitidos para la tarea (-1 significa ilimitados)
  "annotatable_attachment_id": null,  // ID de archivo adjunto que puede ser anotado, si existe
  "hide_in_gradebook": false,  // Indica si la tarea se oculta en el libro de calificaciones
  "secure_params": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsdGlfYXNzaWdubWVudF9pZCI6IjRlY2Y1Y2VlLWE0ZWMtNDg5Mi04MWY3LTlhOTM5NjAyYWI3NCIsImx0aV9hc3NpZ25tZW50X2Rlc2NyaXB0aW9uIjoiXHUwMDNjcFx1MDAzZXhkXHUwMDNjL3BcdTAwM2UifQ.BKoLamlEJkdgiN8qwCPuI-8GvMtHMZ_8qN759G_abCY",  // Parámetros seguros para la tarea
  "lti_context_id": "4ecf5cee-a4ec-4892-81f7-9a939602ab74",  // ID de contexto LTI para integración externa
  "course_id": 10424594,  // ID del curso al que pertenece la tarea
  "name": "Informe 3 - Muriendo en Quimica",  // Nombre de la tarea
  "submission_types": ["online_upload"],  // Tipos de entrega permitidos (subida en línea)
  "has_submitted_submissions": false,  // Indica si ya se han enviado entregas para la tarea
  "due_date_required": false,  // Indica si la fecha de vencimiento es obligatoria
  "max_name_length": 255,  // Longitud máxima del nombre de la tarea
  "in_closed_grading_period": false,  // Indica si la tarea está en un período de calificación cerrado
  "graded_submissions_exist": false,  // Indica si existen entregas calificadas para la tarea
  "is_quiz_assignment": false,  // Indica si la tarea es un cuestionario
  "can_duplicate": true,  // Indica si la tarea se puede duplicar
  "original_course_id": null,  // ID del curso original de la tarea duplicada, si existe
  "original_assignment_id": null,  // ID de la tarea original, si existe
  "original_lti_resource_link_id": null,  // ID de enlace de recurso LTI original, si existe
  "original_assignment_name": null,  // Nombre de la tarea original, si existe
  "original_quiz_id": null,  // ID del cuestionario original, si existe
  "workflow_state": "published",  // Estado del flujo de trabajo de la tarea (publicada)
  "important_dates": false,  // Indica si las fechas de la tarea son importantes
  "muted": true,  // Indica si la tarea está silenciada en el libro de calificaciones
  "html_url": "https://canvas.instructure.com/courses/10424594/assignments/50641401",  // URL de la tarea en Canvas
  "has_overrides": false,  // Indica si hay sobrescrituras para la tarea
  "needs_grading_count": 0,  // Número de entregas que necesitan calificación
  "sis_assignment_id": null,  // ID de la tarea en el sistema de información de estudiantes (SIS), si existe
  "integration_id": null,  // ID de integración, si existe
  "integration_data": {},  // Datos de integración adicionales
  "published": true,  // Indica si la tarea está publicada
  "unpublishable": true,  // Indica si la tarea se puede despublicar
  "only_visible_to_overrides": false,  // Indica si la tarea solo es visible para sobrescrituras
  "visible_to_everyone": true,  // Indica si la tarea es visible para todos
  "locked_for_user": false,  // Indica si la tarea está bloqueada para el usuario
  "submissions_download_url": "https://canvas.instructure.com/courses/10424594/assignments/50641401/submissions?zip=1",  // URL para descargar todas las entregas de la tarea
  "post_manually": false,  // Indica si la tarea debe ser publicada manualmente
  "anonymize_students": false,  // Indica si se deben anonimizar los estudiantes
  "require_lockdown_browser": false,  // Indica si se requiere un navegador seguro para la tarea
  "restrict_quantitative_data": false  // Indica si se restringen los datos cuantitativos
}
```

Además, es posible obtenerlo en código mediante lo siguiente:

```python
url = f'https://canvas.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}'
headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
response = (requests.get(url, headers=headers)).json()
```

2- Obtener Entregas de una Tarea del Curso - [GET]

- **URL**: https://canvas.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions
- **Parametros**:
    - `course_id`: ID del Curso.
    - `assignment_id`: ID del Assignment.
- **Encabezados**:
    - `Authorization`: Bearer token de acceso.
- **Descripción**: Recupera todas las entregas asociadas a una tarea específica de un curso en Canvas.
- **Respuesta**:
    - `200`: Datos JSON con la información de todas las entregas de la tarea.
    - `400`: Solicitud incorrecta o token inválido.
    - `404`: Tarea o curso no encontrado.
    - `500`: Error interno del servidor.

En el caso que sea correcto, se obtiene el siguiente json:

```json
[
  {
    "id": 638909097,
    "body": null,  // Cuerpo de la entrega (vacío porque no hay contenido enviado)
    "url": null,  // URL de la entrega (vacío porque no hay entrega subida)
    "grade": null,  // Calificación de la entrega (vacío porque no se ha calificado)
    "score": null,  // Puntuación de la entrega (vacío porque no se ha calificado)
    "submitted_at": null,  // Fecha y hora de envío (vacío porque no se ha enviado)
    "assignment_id": 50641401,  // ID de la tarea asociada
    "user_id": 114193347,  // ID del usuario que debería realizar la entrega
    "submission_type": null,  // Tipo de entrega (vacío porque no se ha enviado nada)
    "workflow_state": "unsubmitted",  // Estado de la entrega (no enviado)
    "grade_matches_current_submission": true,  // Indica si la calificación coincide con la última entrega
    "graded_at": null,  // Fecha de calificación (vacío porque no se ha calificado)
    "grader_id": null,  // ID del calificador (vacío porque no se ha calificado)
    "attempt": null,  // Número de intentos realizados (vacío porque no hay intentos)
    "cached_due_date": "2024-10-24T05:59:59Z",  // Fecha límite de la tarea
    "excused": null,  // Indica si el estudiante está exento (vacío porque no se aplica)
    "late_policy_status": null,  // Estado de la política de entrega tardía
    "points_deducted": null,  // Puntos deducidos por entrega tardía (vacío porque no se aplica)
    "grading_period_id": null,  // ID del período de calificación (vacío porque no está asociado)
    "extra_attempts": null,  // Intentos adicionales permitidos (vacío porque no se aplica)
    "posted_at": null,  // Fecha en que se publicó la calificación (vacío porque no se ha calificado)
    "redo_request": false,  // Indica si se ha solicitado rehacer la entrega
    "custom_grade_status_id": null,  // Estado de calificación personalizado
    "sticker": null,  // Pegatina asociada (vacío porque no hay)
    "late": false,  // Indica si la entrega fue tardía (falso porque no hay entrega)
    "missing": true,  // Indica si falta la entrega
    "seconds_late": 248001,  // Segundos de retraso si se hubiera entregado
    "entered_grade": null,  // Calificación ingresada manualmente (vacío)
    "entered_score": null,  // Puntuación ingresada manualmente (vacío)
    "preview_url": "https://canvas.instructure.com/courses/10424594/assignments/50641401/submissions/114193347?preview=1&version=0"  // URL para previsualizar la entrega
  },
  {
    "id": 638909098,
    "body": null,  // Cuerpo de la entrega (vacío porque se trata de un archivo subido)
    "url": null,  // URL de la entrega (vacío porque es un archivo adjunto)
    "grade": null,  // Calificación de la entrega (vacío porque no se ha calificado)
    "score": null,  // Puntuación de la entrega (vacío porque no se ha calificado)
    "submitted_at": "2024-10-27T01:42:29Z",  // Fecha y hora de envío
    "assignment_id": 50641401,  // ID de la tarea asociada
    "user_id": 114193934,  // ID del usuario que realizó la entrega
    "submission_type": "online_upload",  // Tipo de entrega (subida en línea)
    "workflow_state": "submitted",  // Estado de la entrega (enviado)
    "grade_matches_current_submission": true,  // Indica si la calificación coincide con la última entrega
    "graded_at": null,  // Fecha de calificación (vacío porque no se ha calificado)
    "grader_id": null,  // ID del calificador (vacío porque no se ha calificado)
    "attempt": 2,  // Número de intentos realizados (segundo intento)
    "cached_due_date": "2024-10-24T05:59:59Z",  // Fecha límite de la tarea
    "excused": null,  // Indica si el estudiante está exento (vacío porque no se aplica)
    "late_policy_status": null,  // Estado de la política de entrega tardía
    "points_deducted": 0.0,  // Puntos deducidos por entrega tardía
    "grading_period_id": null,  // ID del período de calificación (vacío porque no está asociado)
    "extra_attempts": null,  // Intentos adicionales permitidos (vacío porque no se aplica)
    "posted_at": null,  // Fecha en que se publicó la calificación (vacío porque no se ha calificado)
    "redo_request": false,  // Indica si se ha solicitado rehacer la entrega
    "custom_grade_status_id": null,  // Estado de calificación personalizado
    "sticker": null,  // Pegatina asociada (vacío porque no hay)
    "late": true,  // Indica si la entrega fue tardía
    "missing": false,  // Indica si falta la entrega (falso porque sí se entregó)
    "seconds_late": 243750,  // Segundos de retraso
    "entered_grade": null,  // Calificación ingresada manualmente (vacío)
    "entered_score": null,  // Puntuación ingresada manualmente (vacío)
    "preview_url": "https://canvas.instructure.com/courses/10424594/assignments/50641401/submissions/114193934?preview=1&version=2",  // URL para previsualizar la entrega
    "attachments": [
      {
        "id": 274755888,
        "uuid": "eOyMvXgLRLlxeATnbku4xfJCjOFJIgdnfqtQKsaL",  // UUID del archivo adjunto
        "folder_id": 61308848,  // ID de la carpeta donde está almacenado
        "display_name": "Entrega4 (4) (1).pdf",  // Nombre para mostrar del archivo
        "filename": "Entrega4+%284%29+%281%29.pdf",  // Nombre del archivo en S3
        "upload_status": "success",  // Estado de la subida (éxito)
        "content-type": "application/pdf",  // Tipo de contenido MIME
        "url": "https://canvas.instructure.com/files/274755888/download?download_frd=1&verifier=eOyMvXgLRLlxeATnbku4xfJCjOFJIgdnfqtQKsaL",  // URL para descargar el archivo
        "size": 117901,  // Tamaño del archivo en bytes
        "created_at": "2024-10-27T01:42:29Z",  // Fecha de creación del archivo
        "updated_at": "2024-10-27T01:42:40Z",  // Fecha de última actualización del archivo
        "unlock_at": null,  // Fecha de desbloqueo (vacío porque no está bloqueado)
        "locked": false,  // Indica si el archivo está bloqueado
        "hidden": false,  // Indica si el archivo está oculto
        "lock_at": null,  // Fecha de bloqueo (vacío porque no se aplica)
        "hidden_for_user": false,  // Indica si el archivo está oculto para el usuario
        "thumbnail_url": null,  // URL de la miniatura (vacío porque no hay)
        "modified_at": "2024-10-27T01:42:29Z",  // Fecha de modificación del archivo
        "mime_class": "pdf",  // Clase MIME del archivo
        "media_entry_id": null,  // ID de entrada multimedia (vacío porque no se aplica)
        "category": "uncategorized",  // Categoría del archivo
        "locked_for_user": false,  // Indica si el archivo está bloqueado para el usuario
        "preview_url": "/api/v1/canvadoc_session?blob=%7B%22moderated_grading_allow_list%22:null,%22enable_annotations%22:true,%22enrollment_type%22:%22teacher%22,%22anonymous_instructor_annotations%22:false,%22submission_id%22:638909098,%22user_id%22:70000113898643,%22attachment_id%22:274755888,%22type%22:%22canvadoc%22%7D&hmac=a7925070ee74589ed06ad58be07f0d123daa0247"  // URL para previsualizar el archivo en Canvas DocViewer
      }
    ]
  }
]
```

Además, es posible obtenerlo en código mediante lo siguiente:

```python
url = f'https://canvas.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions'
headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
response = (requests.get(url, headers=headers)).json()
```
