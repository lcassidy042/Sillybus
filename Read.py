import re

class Classroom:
    def __init__(self, CourseName, CourseID, Summary, Categories, Weight, AssignmentName, AssignmentType, AssingmentDate, misc):
        self.CourseName = CourseName
        self.CourseID = CourseID
        self.Summary = Summary
        self.Categories = Categories
        self.Weight = Weight
        self.AssignmentName = AssignmentName
        self.AssignmentType = AssignmentType
        self.AssignmentDate = AssingmentDate
        self.misc = misc
def isSomethingElse(line):
    for pattern in patterns:
        if(re.search(pattern, line)):
            return True
        if(line == "\n"):
            return True
    return False
patterns = [r'Course Name:\s*(.*)', r'Syllabus\s*(.*)', r'Course ID:\s*(.*)', r'Summary:\s*(.*)',
            r'Grade Categories:\s*(.*)', r'Assignments:\s*(.*)']


def CreateNotebook(file_path):
    file = open(file_path)
    lines = file.readlines()
    length = len(lines)
    i = 0
    Summary = ""
    CourseID = 0
    CourseName = ""
    Categories = []
    Weight = []
    AssignmentName = []
    AssignmentType = []
    AssignmentDate = []
    misc = ""
    while i<length :
        isCourseName = re.search(patterns[0], lines[i])
        isCourseID = re.search(patterns[2], lines[i])
        isCourseSummary = re.search(patterns[3], lines[i])
        isGradeCategories = re.search(patterns[4], lines[i])
        isAssignments = re.search(patterns[5], lines[i])

        if isCourseID:
            CourseID = isCourseID.group(1)
        elif isCourseName:
            CourseName = isCourseName.group(1)
        elif isCourseSummary:
            for x in range (i, length-1):
                i += 1
                if isSomethingElse(lines[i]):
                    i -= 1
                    break
                Summary += lines[i]
        elif isGradeCategories:
            for x in range(i, length-1):
                i += 1
                if isSomethingElse(lines[i]):
                    i -= 1
                    break
                words = lines[i].split()
                Categories.append(words[0])
                Weight.append(words[1])
        elif isAssignments:
            for x in range(i, length-1):
                i += 1
                if isSomethingElse(lines[i]) :
                    i -= 1
                    break
                AssignmentName.append((lines[i])[:lines[i].find('(')])
                AssignmentType.append((lines[i])[lines[i].find('(')+1: lines[i].find(')')])
                AssignmentDate.append((lines[i])[lines[i].find(')')+3:])
        else:
            misc += lines[i]
        i += 1

    NewClass = Classroom(CourseName, CourseID, Summary, Categories, Weight, AssignmentName, AssignmentType, AssignmentDate, misc)
    print(NewClass.CourseName)
    print(NewClass.CourseID)
    print(NewClass.Summary)
    print(NewClass.Categories)
    print(NewClass.Weight)
    print(NewClass.AssignmentName)
    print(NewClass.AssignmentType)
    print(NewClass.AssignmentDate)
    print(NewClass.misc)
    return NewClass

CreateNotebook("Syllabi/Test.txt")