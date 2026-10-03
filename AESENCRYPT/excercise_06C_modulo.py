data = bytes([250, 251, 252, 253, 254, 255])

for value in data:
    print(value, "->", (value + 10) % 256)