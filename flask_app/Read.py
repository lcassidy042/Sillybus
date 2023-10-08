import re
<<<<<<< Updated upstream
import convertd2t
=======
>>>>>>> Stashed changes

class Assignment:
    def __init__(self, Name, Type, Date,):
        self.Name = Name
        self.Type = Type
        self.Date = Date

<<<<<<< Updated upstream
# class Material:
#     def __init__(self, Name, Date):
#         self.Name = Name
#         self.Date = Date

=======
>>>>>>> Stashed changes
class Classroom:
    def __init__(self, CourseName, CourseID, Room, Summary, Assignments, misc):
        self.CourseName = CourseName
        self.CourseID = CourseID
        self.Room = Room
        self.Summary = Summary
<<<<<<< Updated upstream
        #self.Categories = Categories
        #self.Weight = Weight
        self.Assignments = Assignments
        #self.Materials = Materials
=======
        self.Assignments = Assignments
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        print("Converting DOCX to TXT...")
        file_path = convertd2t.main(file_path)
        print("converted")
=======
        print("need to convert")
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    #Categories = []
    #Weight = []
    Assignments = []
    #Materials = []
=======
    Assignments = []
>>>>>>> Stashed changes
    misc = ""
    Room = ""
    while i<length :
        isCourseName = re.search(patterns[0], lines[i])
        isCourseID = re.search(patterns[2], lines[i])
        isCourseSummary = re.search(patterns[3], lines[i])
<<<<<<< Updated upstream
        #isGradeCategories = re.search(patterns[4], lines[i])
        isAssignments = re.search(patterns[5], lines[i])
        #isMaterials = re.search(patterns[6], lines[i])
=======
        isAssignments = re.search(patterns[5], lines[i])
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        # elif isGradeCategories:
        #     for x in range(i, length-1):
        #         i += 1
        #         if isSomethingElse(lines[i]):
        #             i -= 1
        #             break
        #         words = lines[i].split()
        #         Categories.append(words[0])
        #         Weight.append(words[1])
=======
>>>>>>> Stashed changes
        elif isAssignments:
            for x in range(i, length-1):
                i += 1
                if isSomethingElse(lines[i]) :
                    i -= 1
                    break
                Assignments.append(Assignment((lines[i])[:lines[i].find('(')], (lines[i])[lines[i].find('(')+1: lines[i].find(')')], (lines[i])[lines[i].find(')')+3:]))
<<<<<<< Updated upstream
        # elif isMaterials:
        #     for x in range(i, length - 1):
        #         i += 1
        #         if isSomethingElse(lines[i]):
        #             i -= 1
        #             break
        #         words = lines[i].split(" ")
        #         Materials.append(Material((lines[i])[:lines[i].find(words[len(words)-1])-2], (lines[i])[lines[i].find(words[len(words)-1]):]))
=======
>>>>>>> Stashed changes
        else:
            misc += lines[i]
        i += 1

    NewClass = Classroom(CourseName, CourseID, Room, Summary, Assignments,misc)
    
<<<<<<< Updated upstream
    # print(NewClass.CourseName)
    # print(NewClass.CourseID)
    # print(NewClass.Summary)
    # print(NewClass.misc)
    
    return NewClass

#CreateNotebook("Syllabi/Test.txt")
=======
    return NewClass, Assignments

>>>>>>> Stashed changes
