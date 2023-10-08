from flask import Flask, render_template, request, jsonify
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import Read  # Import your other Python script as a module

app = Flask(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses']

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

        # Call the CreateNotebook function from read.py to parse the file
        OurClass = Read.CreateNotebook(file_path)

        if OurClass:
            # Prepare a dictionary with the parsed data
            parsed_data = {
                'CourseName': OurClass.CourseName,
                'CourseID': OurClass.CourseID,
                'Room': OurClass.Room,
                'Summary': OurClass.Summary + OurClass.misc,
                # Add other parsed fields here
            }

            return jsonify(parsed_data)
        else:
            return jsonify({'error': 'Failed to parse the file.'}), 400
    else:
        return jsonify({'error': 'No file uploaded.'}), 400

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    creds = get_credentials()
    service = build('classroom', 'v1', credentials=creds)

    if request.method == 'POST':
        # Handle the form submission as before
        course = {
            'name': request.form['name'],
            'section': request.form['section'],
            'description': request.form['description'],
            'room': request.form['room'],
            'ownerId': 'me',
            'courseState': 'PROVISIONED'
        }

        try:
            course = service.courses().create(body=course).execute()
            return f'Course created: {(course.get("name"), course.get("id"))}'
        except HttpError as error:
            return f'An error occurred: {error}'

    # Render the template without autofilled values
    return render_template('create_course.html')


if __name__ == '__main__':
    app.run(debug=True)
