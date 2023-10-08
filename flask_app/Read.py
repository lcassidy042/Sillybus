import re

class Assignment:
    def __init__(self, Name, Type, Date,):
        self.Name = Name
        self.Type = Type
        self.Date = Date

class Classroom:
    def __init__(self, CourseName, CourseID, Room, Summary, Assignments, misc):
        self.CourseName = CourseName
        self.CourseID = CourseID
        self.Room = Room
        self.Summary = Summary
        self.Assignments = Assignments
        self.misc = misc

def isSomethingElse(line):
    for pattern in patterns:
        if(re.search(pattern, line)):
            return True
        if(line == "\n"):
            return True
    return False
patterns = [r'Course Name:\s*(.*)', r'Syllabus\s*(.*)', r'Course ID:\s*(.*)', r'Summary:\s*(.*)',
            r'Grade Categories:\s*(.*)', r'Assignments:\s*(.*)', r'Materials:\s*(.*)', r'Room:\s*(.*)']

def CreateNotebook(file_path):
    if file_path.endswith('.pdf'):
        print("need to convert")
        return
    elif file_path.endswith(('.docx')):
        print("need to convert")
        file = open(file_path)

    elif not file_path.endswith('.txt'):
        print("what are you")
    else: file = open(file_path)
    lines = file.readlines()
    length = len(lines)
    i = 0
    Summary = ""
    CourseID = 0
    CourseName = ""
    Assignments = []
    misc = ""
    Room = ""
    while i<length :
        isCourseName = re.search(patterns[0], lines[i])
        isCourseID = re.search(patterns[2], lines[i])
        isCourseSummary = re.search(patterns[3], lines[i])
        isAssignments = re.search(patterns[5], lines[i])
        isRoom = re.search(patterns[7], lines[i])

        if isCourseID:
            CourseID = isCourseID.group(1)
        elif isCourseName:
            CourseName = isCourseName.group(1)
        elif isRoom:
            Room = isRoom.group(1)
        elif isCourseSummary:
            for x in range (i, length-1):
                i += 1
                if isSomethingElse(lines[i]):
                    i -= 1
                    break
                Summary += lines[i]
        elif isAssignments:
            for x in range(i, length-1):
                i += 1
                if isSomethingElse(lines[i]) :
                    i -= 1
                    break
                Assignments.append(Assignment((lines[i])[:lines[i].find('(')], (lines[i])[lines[i].find('(')+1: lines[i].find(')')], (lines[i])[lines[i].find(')')+3:]))
        else:
            misc += lines[i]
        i += 1

    NewClass = Classroom(CourseName, CourseID, Room, Summary, Assignments,misc)
    
    return NewClass, Assignments

