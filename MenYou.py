from __future__ import print_function
import os.path
import inquirer #Asks questions
import Read
#Google API
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses']

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time
    OurClass = Read.CreateNotebook("Syllabi/Test.txt")
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('classroom', 'v1', credentials=creds)
        create_or_use = inquirer.prompt([inquirer.List('create_or_use',message="Create a Course or Use Existing Course?",choices=["Create a Course", "Use Existing Course"])])
        # Call the Classroom API
        results = service.courses().list(pageSize=10).execute()
        courses = results.get('courses', [])
        if create_or_use['create_or_use'] == "Use Existing Course":
            #Prompts the user to select a course from their list and saves the API course object to course.
            if not courses:
                print('No courses found.')
                return
            tuples = []
            for course in courses:
                tuples.append((course['name'], course))
            courseList = inquirer.List('course',message="What course do you need?",choices=tuples)
            course = inquirer.prompt([courseList])['course']
        elif create_or_use['create_or_use'] == "Create a Course":
            #Prompts the user to create a course with given specifications and saves the API course object to course
            course = {'name' : OurClass.CourseName, 'section': OurClass.CourseID, 'descriptionHeading' : "", 'description' : OurClass.Summary + OurClass.misc,'room' : OurClass.Room,  'ownerId' : 'me', 'courseState' : 'PROVISIONED'}
            print(course)
            course = service.courses().create(body=course).execute() #Create course in api
            print(f"Course created:  {(course.get('name'), course.get('id'))}")
        return course
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
