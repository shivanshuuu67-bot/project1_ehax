text = input("Enter exactly 16 characters: ")

data = text.encode("utf-8")

if len(data) != 16:
    print("Error: input must be exactly 16 bytes.")
else:
    #FOR BYTES
    for i in range(4):
        for j in range(4):
            print(data[j * 4 + i], end=" ")
        print()

    #FOR CHARACTERS
    for i in range(4):
        for j in range(4):
            print(text[j * 4 + i], end=" ")
        print()