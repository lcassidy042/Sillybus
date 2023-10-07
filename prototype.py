from __future__ import print_function

import os.path
import inquirer

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']


def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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
            if not courses:
                print('No courses found.')
                return
            # Prints the names of the first 10 courses.
            courseNames = []
            courseIds = []
            for course in courses: 
                courseNames.append(course['name'])
                courseIds.append(course['id'])
            courseSelected = inquirer.prompt([inquirer.List('course',message="What course do you need?",choices=courseNames)])
            service.courses.get(id=courses['name'==courseSelected['courseSelected']]).execute() 
        elif create_or_use['create_or_use'] == "Create a Course":
            print("To be continued")
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
