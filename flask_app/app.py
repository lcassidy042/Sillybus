from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import Read

app = Flask(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses', 'https://www.googleapis.com/auth/classroom.coursework.students']

# Initialize a variable to hold the parsed data and assignments
global class_data

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

@app.route('/')
def index():
    return render_template('create_course.html')

@app.route('/process_file', methods=['POST'])
def process_file():
    uploaded_file = request.files.get('file')

    if uploaded_file:
        upload_folder = os.path.join(os.getcwd(), "uploads")
        os.makedirs(upload_folder, exist_ok=True)  # This line creates the directory if it doesn't exist
        file_path = os.path.join(upload_folder, uploaded_file.filename)        
        uploaded_file.save(file_path)

        global class_data 
        class_data, _ = Read.CreateNotebook(file_path)

        if class_data:
            parsed_data = {
                'CourseName': class_data.CourseName,
                'CourseID': class_data.CourseID,
                'Room': class_data.Room,
                'Summary': class_data.Summary + class_data.misc,
            }
            
            return jsonify(parsed_data)
        else:
            return jsonify({'error': 'Failed to parse the file.'}), 400
    else:
        return jsonify({'error': 'No file uploaded.'}), 400

@app.route('/create_course', methods=['POST'])
def create_class():
    creds = get_credentials()

    if request.method == 'POST' and class_data:
        course_name = request.form.get('name')
        section = request.form.get('section')
        description = request.form.get('description')
        room = request.form.get('room')

        # Create a class using the Google Classroom API
        if creds:
            service = build('classroom', 'v1', credentials=creds)
            course = {
                'name': course_name,
                'section': section,
                'descriptionHeading': course_name,
                'description': description,
                'room': room,
                'ownerId': "me",
            }
            try:
                course = service.courses().create(body=course).execute()
                course_id = course['id']
                return redirect(url_for('display_assignments', course_id=course_id))

            except HttpError as error:
                return f'An error occurred: {error.resp}'

    return redirect(url_for('index'))

@app.route('/assignments', methods=['GET', 'POST'])
def display_assignments():
    course_id = request.args.get('course_id')

    if class_data is None:
        return redirect(url_for('index'))  # Redirect to the main page if no file has been uploaded
    
    assignments = class_data.Assignments
    return render_template('assignments.html', assignments=assignments, course_id=course_id)


## when u fix this bug, u better add some beautiful css and loading bar and confetti upon assignment creation
@app.route('/create_assignments', methods=['POST'])
def create_assignments():
    creds = get_credentials()

    course_id = request.args.get('course_id')
    class_data = session.get('class_data', None)
    if request.method == 'POST':
        
        service = build('classroom', 'v1', credentials=creds)

        try:
            for assignment in class_data.Assignments:
                date_parts = [int(part) for part in assignment.Date.split('/')]
                coursework = {
                    'title': assignment.Name,
                    'description': "",
                    'state': 'PUBLISHED',
                    'dueDate': {
                        'year': date_parts[2],
                        'month': date_parts[0],
                        'day': date_parts[1]
                    },
                    'dueTime': {
                        'hours': 3,
                        'minutes': 59,
                        'seconds': 0,
                        'nanos': 0
                    }
                }
                coursework = service.courses().courseWork().create(courseId=course_id, body=coursework).execute()
                print(f"Assignment created with ID {coursework.get('id')}")

            return redirect(url_for('final_display', course_id=course_id))

        except HttpError as error:
            print("error with creating assignments")
            return f'An error occurred: {error}'

    return redirect(url_for('display_assignments'))

@app.route('/final_display')
def final_display():
    global class_data
    
    if class_data:
        return render_template('final_display.html', class_data=class_data)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
