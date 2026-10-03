def pkcs7_unpad(data):

    padding = data[-1]

    print("Padding length:", padding)

def pkcs7_unpad(data):

    padding = data[-1]

    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding")

    return data[:-padding]


data = b'Hello\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0c'

original = pkcs7_unpad(data)

print(original)