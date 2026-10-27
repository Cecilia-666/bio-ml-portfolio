

#open the file
with open("dna.txt", "r", encoding="utf-8") as f:
    file_contents = f.read()
    print(file_contents)
