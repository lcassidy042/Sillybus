from __future__ import print_function
import sys
import re
import datetime
import Read 
import menu
#Google API

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# pylint: disable=maybe-no-member
def assigner(file_name):
    syllabus = Read.CreateNotebook(file_name) 
    course = menu()
    creds, _ = google.auth.default()
    try:
        service = build('classroom', 'v1', credentials=creds)
        for assignment in syllabus.assignments:      
            #split date here  
            date_parts = [int(part) for part in assignment.Date.split('/')] 
            coursework = {
                'title': assignment.Name,
                'workType': 'ASSIGNMENT',
                'state': 'PUBLISHED',
                'dueDate': {"year": date_parts[0],
                            "month": date_parts[1],
                            "day": date_parts[2]},
                'dueTime': {"hours": 23,
                            "minutes": 59,
                            "seconds": 0,
                            "nanos": 0}
            }
            coursework = service.courses().courseWork().create(courseId=course['id'], body=coursework).execute()
            print(f"Assignment created with ID {coursework.get('id')}")
        return coursework
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script_name.py source_pdf_file.pdf")
        sys.exit(1)
    source = sys.argv[1]
    assigner(source)