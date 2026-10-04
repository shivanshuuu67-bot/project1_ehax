with open("input.txt", "r") as file:
    plaintext = file.read()

print("Plaintext:", plaintext)

data = plaintext.encode("utf-8")

print("Bytes:", data)
print("Byte list:", list(data))