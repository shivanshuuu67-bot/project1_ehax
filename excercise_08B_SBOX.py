def rotate_left(byte, n):
    return ((byte << n) | (byte >> (8 - n))) & 0xFF

def affine_transform(x):

    result = x

    result ^= rotate_left(x, 1)
    result ^= rotate_left(x, 2)
    result ^= rotate_left(x, 3)
    result ^= rotate_left(x, 4)

    result ^= 0x63

    return result

x = 0xCA

result = affine_transform(x)

print(hex(result))