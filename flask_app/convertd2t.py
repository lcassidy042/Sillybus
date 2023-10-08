import docx2txt

def convertDocToTxt(argv):
    filename = argv
    print(filename)
    syllabus = docx2txt.process(filename)
    #print(syllabus)
    remove_linebreaks = syllabus.split("\n")
    
    remove_spaces = ""
    counter = 0
    for word in remove_linebreaks:
        counter += 1
        remove_spaces += word
        if counter %2 == 0:
            remove_spaces += '\n'
    return remove_spaces

#check if txt file input, return into txt file after parsing
def return_txt(argv):
    parsed_text = convertDocToTxt(argv) #parsed text
   # print(parsed_text)
    with open('uploads/converted_docx.txt', 'w') as file: 
        file.write(parsed_text)
def main(argv):
    #if len(sys.argv) != 2:
        #print("Usage: python script_name.py source_docx_file.docx")
        #sys.exit(1)

    return_txt(argv)
if __name__ == '__main__':

    main()






