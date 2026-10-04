with open("input.txt", "r") as file:
    plaintext = file.read()

with open("output.txt", "w") as file:
    file.write(plaintext)

print("File copied successfully.")