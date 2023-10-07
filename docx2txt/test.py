import docx2txt

def main():
    syllabus = docx2txt.process("/Users/jasonjasoon/Documents/Job Stuff/Resume (New 3, Jason Lei).docx")
    print(syllabus)
    nolinebreaks = syllabus.split("\n")
    
    nospaces = []
    for word in nolinebreaks:
        if word == "":
            pass
        else:
            nospaces.append(word)

    #print(nospaces)
    lastName = nospaces[1]
    firstName = nospaces[2]
    email = nospaces[5]

    print(lastName)
    print(firstName)
    print(email)    
    
main()






