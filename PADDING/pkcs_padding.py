def padding_length(data):

    block_size = 16

    remainder = len(data) % block_size

    padding = block_size - remainder

    return padding  

def pkcs7_pad(data):

    block_size = 16

    padding = block_size - (len(data) % block_size)

    return data + bytes([padding]) * padding

data = b"1234567890123456"

padded = pkcs7_pad(data)

print(padded)
print(len(padded))
print(padded.hex())