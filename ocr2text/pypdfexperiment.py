from PyPDF2 import PdfReader

reader = PdfReader(r'ocr2text\test_files\syllabus.pdf')
page = reader.pages[0]
extracted_text = page.extract_text()
print(extracted_text)