import os
import shutil
import errno
import subprocess
from tempfile import mkdtemp

try:
    from PIL import Image
except ImportError:
    print('Error: You need to install the "Image" package. Type the following:')
    print('pip install Image')

try:
    import pytesseract
except ImportError:
    print('Error: You need to install the "pytesseract" package. Type the following:')
    print('pip install pytesseract')
    exit()

try:
    from pdf2image import convert_from_path, convert_from_bytes
except ImportError:
    print('Error: You need to install the "pdf2image" package. Type the following:')
    print('pip install pdf2image')
    exit()
import time
import sys


def update_progress(progress):
    barLength = 10  
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format(
        "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def run(args):
    # run a subprocess and put the stdout and stderr on the pipe object
    try:
        pipe = subprocess.Popen(
            args,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except OSError as e:
        if e.errno == errno.ENOENT:
            # File not found.
            # This is equivalent to getting exitcode 127 from sh
            raise RuntimeError(
                ' '.join(args), 127, '', '',
            )

    # pipe.wait() ends up hanging on large files. using
    # pipe.communicate appears to avoid this issue
    stdout, stderr = pipe.communicate()

    # if pipe is busted, raise an error (unlike Fabric)
    if pipe.returncode != 0:
        raise RuntimeError(
            ' '.join(args), pipe.returncode, stdout, stderr,
        )

    return stdout, stderr


def extract_tesseract(filename):
    temp_dir = mkdtemp()
    base = os.path.join(temp_dir, 'conv')
    contents = []
    try:
        stdout, _ = run(['pdftoppm', filename, base])

        for page in sorted(os.listdir(temp_dir)):
            page_path = os.path.join(temp_dir, page)
            page_content = pytesseract.image_to_string(Image.open(page_path))
            contents.append(page_content)
        return ''.join(contents)
    finally:
        shutil.rmtree(temp_dir)


def convert(sourcefile, destination_file, count, pdfCounter):
    text = extract_tesseract(sourcefile)
    with open(destination_file, 'w', encoding='utf-8') as f_out:
        f_out.write(text)
    print()
    print('Converted ' + sourcefile)
    count += 1
    update_progress(count / pdfCounter)
    return count

count = 0
print()
print('********************************')
print('*** PDF to TXT file, via OCR ***')
print('********************************')
print()

# Pass the source file as an argument to the script
if len(sys.argv) != 2:
    print("Usage: python script_name.py source_pdf_file.pdf")
    sys.exit(1)

source = sys.argv[1]

# Output file will be in the same directory as the source
output_directory, source_filename = os.path.split(source)
filename, file_extension = os.path.splitext(source_filename)
if (file_extension.lower() == '.pdf'):
    destination = os.path.join(output_directory, filename + '.txt')
else:
    print("Error: Input file must have a .pdf extension.")
    sys.exit(1)

count = convert(source, destination, count, 1)
print(str(count) + ' file converted')
