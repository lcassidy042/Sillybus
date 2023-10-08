from pdfminer.high_level import extract_text

text = extract_text(r'ocr2text\test_files\syllabus.pdf')
print(text) 