

file_path = "Syllabi/test.txt"

file = open(file_path)
lines = file.readlines()
for line in lines:
    print(line)