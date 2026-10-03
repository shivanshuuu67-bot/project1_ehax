str1 = input("Enter first character: ")
str2 = input("Enter second character: ")

byte1 = str1.encode("utf-8")[0]
byte2 = str2.encode("utf-8")[0]

result = byte1 ^ byte2

print("First character's byte value:", byte1)
print("Second character's byte value:", byte2)

print("First Hex:", hex(byte1))
print("Second Hex:", hex(byte2))

print("XOR Result:", result)
print("XOR Result in Hex:", hex(result))