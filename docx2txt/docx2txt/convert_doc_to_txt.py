import docx2txt
import sys


def convertDocToTxt():
    filename = sys.argv[1]
    syllabus = docx2txt.process(filename)
    #print(syllabus)
    remove_linebreaks = syllabus.split("\n")
    
    remove_spaces = []
    for word in remove_linebreaks:
        if word == "":
            pass
        else:
            remove_spaces.append(word)
    return syllabus

#check if txt file input, return into txt file after parsing
def return_txt():

    parsed_text = convertDocToTxt() #parsed text
   # print(parsed_text)
    with open('syllabus.txt', 'w') as file: 
        file.write(parsed_text)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py source_docx_file.docx")
        sys.exit(1)
    return_txt()

if __name__ == '__main__':

    main()






