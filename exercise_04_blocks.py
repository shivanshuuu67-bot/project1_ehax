val = input("Enter a string: ")
data = val.encode("utf-8")

for i in range(0, len(data), 16):
    chunk = data[i:i+16]

    print("Block", i // 16 + 1, ":", chunk)
    print("Block", i // 16 + 1, "in list:", list(chunk))
    print("Block", i // 16 + 1, "in hex:", chunk.hex())