from __future__ import print_function
import os.path
import inquirer #Asks questions
#Google API
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.

def main(service):
    try:
        service = service
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
            questions = [
            inquirer.Text('name', message="Course Name?"),
            inquirer.Text('section', message="Section?"),
            inquirer.Text('descriptionHeading', message="Heading Description?"),
            inquirer.Text('description', message="Course Description?"),
            inquirer.Text('room', message="Room Number?"),
            ]
            answers = inquirer.prompt(questions)
            course = {**answers, 'ownerId': 'me', 'courseState': 'PROVISIONED'}
            print(course)
            course = service.courses().create(body=course).execute() #Create course in api
            print(f"Course created:  {(course.get('name'), course.get('id'))}")
        return course
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
