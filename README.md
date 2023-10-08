# Sillybus
<div align="center">
  <img src="https://github.com/lcassidy042/Sillybus/assets/133998249/a712e885-9584-47d8-989d-63baf00a8222" width="450">
</div>
 <br><br>
Sillybus (🤪) is a tool for creating a Google Classroom from a PDF, TXT, or DOCX file of a Syllabus. This tool utilizes: Python+Flask, HTML, CSS, JavaScript and Google Cloud to make a teacher's life easier! 

# How to Run 🏃:
1. Install Python dependency packages using the command ```pip install Flask pdfminer.six google-api-python-client google-auth-httplib2 google-auth-oauthlib docx2txt jsonify``` in Command Prompt/Terminal.
2. Create a Google Cloud project.
3. Create an OAuth Client_ID with classroom API scopes ```classroom.courses``` and ```classroom.coursework.students```.
4. Add authorized users' Google accounts' emails in the process of creating the OAuth Client_ID.
5. Download the OAuth Client_ID as a JSON file and rename it to credentials.json. Add it to the root folder (i.e. Sillybus/credentials.json).
6. Run flask_app/app.py locally. Click on the IP address listed in the output to view the GUI webapp. Sample files are available in the subfolder Sillybus/Syllabi. 

# Directions (For File Upload/Input) 🗞:
* Please ensure that the file being uploaded is of type TXT, DOCX, or PDF.
* Date should be in MM/DD/YYYY format.
* Dates should be in the future.

# Template 📑:
Summary:<br>
SUMMARY GOES HERE<br>
AND HERE<br>
Course Name: COURSE NAME HERE<br>
Course ID: COURSE ID HERE<br>
Room: ROOM HERE<br>

Assignments: <br>
NAME(TYPE), DATE<br>
NAME(TYPE), DATE<br>
NAME(TYPE), DATE<br>
NAME(TYPE), DATE<br>

MISCELLANEOUS: <br>
Email: teacher@school.edu <br>
Feel Free to Reach Out!

# Parts of Your Syllabus 📖:
💬 Summary:
* This will be the summary of your course. Type "Summary:" then hit enter and type your summary on the following lines. It can be more than one line.<br><br> 
📛 Course Name:
* This will be the name of your course. Type "Course Name:," then hit space and type the name of your course as you would like it to appear. <br><br>
🪧 Course ID:
* This will be the ID of your course. Type "Course ID," then hit space and type the ID of your course as you would like it to appear. This does not need to be an integer and will display however you type it. <br><br>
🏫 Room:
* This will be the room of your course. Type "Room," then hit space and type the location of your class. <br><br>
📚 Assignments:
* This will be the assignments of your course. Type "Assignments," then hit enter and type your assignments on the following lines. It needs to be in the format NAME(TYPE), DATE, with only one entry on each line and no breaks between entries. <br><br>
🔖 Miscellaneous:
* This is not a particular category, but it will catch all other text in your syllabi and add it to the end of the description. This could include email or any other contact information.


