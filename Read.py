

file_path = "Syllabi/test.txt"

file = open(file_path)
lines = file.readlines()
length = len(lines)
i = 0
while i<length :

    words = lines[i].split(" ")
    print(words)
    i += 1