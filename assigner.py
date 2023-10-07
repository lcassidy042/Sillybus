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
        assignments = syllabus.assignments
        materials = syllabus.materials
        for assignment in assignments:                
            coursework = {
                'title': 'Ant colonies',
                'description': '''Read the article about ant colonies
                                    and complete the quiz.''',
                'materials': [
                    {'link': {'url': 'http://example.com/ant-colonies'}},
                    {'link': {'url': 'http://example.com/ant-quiz'}}
                ],
                'workType': 'ASSIGNMENT',
                'state': 'PUBLISHED',
                'dueDate': '',
                'dueTime': ''
            }
            coursework = service.courses().courseWork().create(courseId=course['id'], body=coursework).execute()
            print(f"Assignment created with ID {coursework.get('id')}")
        for material in materials:
            coursework = {
                date.
                'title': material.name,
                'workType': 'MATERIAL',
                'state': 'PUBLISHED',
                'dueDate': {"day": },
                'dueTime': ''
            }
            coursework = service.courses().courseWork().create(courseId=course['id'], body=coursework).execute()
            print(f"Material created with ID {coursework.get('id')}")
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