from flask import Flask, render_template, request, jsonify, redirect, url_for
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
class_data = None
edited_assignments = []

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
        file_path = os.path.join(os.getcwd(), "uploads", uploaded_file.filename)
        uploaded_file.save(file_path)

        global class_data  # Make class_data a global variable
        global edited_assignments  # Make edited_assignments a global variable
        class_data, edited_assignments = Read.CreateNotebook(file_path)

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
                return redirect(url_for('display_assignments'))

            except HttpError as error:
                return f'An error occurred: {error}'

    return redirect(url_for('index'))

@app.route('/assignments', methods=['GET', 'POST'])
def display_assignments():
    global class_data  # Access the global variable
    global edited_assignments  # Access the global variable

    if class_data is None:
        return redirect(url_for('index'))  # Redirect to the main page if no file has been uploaded

    if request.method == 'POST':
        # Update assignment values with user-edited values
        for i, assignment in enumerate(class_data.Assignments):
            assignment.Name = request.form.get(f'name_{i}')
            assignment.Type = request.form.get(f'type_{i}')
            assignment.Date = request.form.get(f'date_{i}')
            edited_assignments[i] = assignment

    assignments = edited_assignments if edited_assignments else class_data.Assignments
    return render_template('assignments.html', assignments=assignments)

@app.route('/create_assignments', methods=['POST'])
def create_assignments():
    creds = get_credentials()

    if request.method == 'POST' and class_data:
        service = build('classroom', 'v1', credentials=creds)

        try:
            for assignment in edited_assignments:
                date_parts = [int(part) for part in assignment.Date.split('/')]
                coursework = {
                    'title': assignment.Name,
                    'workType': 'ASSIGNMENT',
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
                coursework = service.courses().courseWork().create(courseId=class_data.CourseID, body=coursework).execute()
                print(f"Assignment created with ID {coursework.get('id')}")

            return redirect(url_for('final_display'))

        except HttpError as error:
            return f'An error occurred: {error}'

    return redirect(url_for('display_assignments'))

@app.route('/final_display')
def final_display():
    global class_data

    if class_data:
        return render_template('final_display.html', created_course=class_data)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
