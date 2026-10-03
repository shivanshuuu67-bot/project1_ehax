def gf_multiply(a, b):

    result = 0

    for i in range(8):

        if b & 1:
            result ^= a

        if a & 0x80:
            a = (a << 1) ^ 0x1B
        else:
            a <<= 1

        a &= 0xFF
        b >>= 1

    return result


def multiplicative_inverse(a):

    if a == 0:
        return 0

    for b in range(1, 256):

        if gf_multiply(a, b) == 1:
            return b

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

def sbox(byte):

    inverse = multiplicative_inverse(byte)

    result = affine_transform(inverse)

    return result

s_box = []

for i in range(256):
    s_box.append(sbox(i))

inv_s_box = [0] * 256

for i in range(256):
    inv_s_box[s_box[i]] = i

def inv_sub_bytes(state):

    for row in range(4):
        for col in range(4):
            state[row][col] = inv_s_box[state[row][col]]

    return state

state = [
    [0x7a, 0x9f, 0x10, 0x27],
    [0x89, 0xd5, 0xf5, 0x0b],
    [0x2b, 0xef, 0xfd, 0x9f],
    [0x3d, 0xca, 0x4e, 0xa7]
]

print("Before InvSubBytes:")

for row in state:
    print([hex(x) for x in row])

state = inv_sub_bytes(state)

print("\nAfter InvSubBytes:")

for row in state:
    print([hex(x) for x in row])
