from __future__ import print_function
#Standard library
import sys
import os

#Other programs
import Read 


#Time libraries
from datetime import datetime, time

#Google API
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/classroom.courses', 'https://www.googleapis.com/auth/classroom.coursework.students']


def assigner(file_name):
    syllabus = Read.CreateNotebook(file_name) 
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
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

    service = build('classroom', 'v1', credentials=creds)
    course = {'name' : syllabus.CourseName, 'section': syllabus.CourseID, 'descriptionHeading' : "", 'description' : syllabus.Summary + syllabus.misc,'room' : syllabus.Room,  'ownerId' : 'me', 'courseState' : 'PROVISIONED'}
    
    try:

        course = service.courses().create(body=course).execute() #Create course in api

        for assignment in syllabus.Assignments:      
            date_parts = [int(part) for part in assignment.Date.split('/')] 
            coursework = {
                'title': assignment.Name,
                'workType': 'ASSIGNMENT',
                'state': 'PUBLISHED',
                'dueDate':{
                    'year': date_parts[2],
                    'month': date_parts[0],
                    'day': date_parts[1]
                },
                'dueTime':{ #Midnight EST converted to UTC, daylight savings is not accounted for
                    'hours': 3,
                    'minutes': 59,
                    'seconds': 0,
                    'nanos': 0
                }
            }
            coursework = service.courses().courseWork().create(courseId=course['id'], body=coursework).execute()
            print(f"Assignment created with ID {coursework.get('id')}")
        return coursework
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python assigner.py source_pdf_file.pdf")
        sys.exit(1)
    source = sys.argv[1]
    assigner(source)