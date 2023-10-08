from __future__ import print_function
import sys
import os
import Read 

import menu
#Google API
from google.type import date_pb2
from google.type import timeofday_pb2
import google.auth
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ['https://www.googleapis.com/auth/classroom.courses', 'https://www.googleapis.com/auth/classroom.coursework.students']

# pylint: disable=maybe-no-member
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
    course = menu.main(service)
    try:
        for assignment in syllabus.Assignments:      
            #split date here  
            # Parse the input date string into a datetime object
            # print(assignment.Date)
            # date_object = date_pb2.Date()
            # date_parts = [int(part) for part in assignment.Date.split('/')] 
            # date_object.year = date_parts[2]  # Set the year
            # date_object.month = date_parts[0]    # Set the month
            # date_object.day = date_parts[1]
            # print(date_object)
            # timeOfDay = timeofday_pb2.TimeOfDay()
            # timeOfDay.hours = 23
            # timeOfDay.minutes = 59
            # timeOfDay.seconds = 0
            # timeOfDay.seconds = 0
            date_object = date_pb2.Date()
            message
            date_object.year = 2023  # Set the year
            date_object.month = 10    # Set the month
            date_object.day = 7       # Set the day

            # Convert google.type.Date to dictionary
            date_dict = {
                "year": date_object.year,
                "month": date_object.month,
                "day": date_object.day
            }

            # Serialize the dictionary to JSON
            json_data = json.dumps(date_dict)
            time_of_day = {
                "hours": 23,
                "minutes": 59,
                "seconds": 0,
                "nanos": 0
            }
            coursework = {
                'title': assignment.Name,
                'workType': 'ASSIGNMENT',
                'state': 'PUBLISHED',
                'dueDate': json_data,
                'dueTime': json.dumps(time_of_day),
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