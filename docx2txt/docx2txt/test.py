import docx2txt


def convertDocToTxt():
    syllabus = docx2txt.process("/Users/jasonjasoon/Documents/Job Stuff/Resume (New 3, Jason Lei).docx")
    #print(syllabus)
    nolinebreaks = syllabus.split("\n")
    
    nospaces = []
    for word in nolinebreaks:
        if word == "":
            pass
        else:
            nospaces.append(word)
    return syllabus

#check if txt file input, return into txt file after parsing
def return_txt():

    parsed_text = convertDocToTxt() #parsed text
   # print(parsed_text)
    with open('syllabus.txt', 'w') as file: 
        file.write(parsed_text)

def main():
    return_txt()

if __name__ == '__main__':
    main()






