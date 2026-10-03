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

def sub_bytes(state):

    for i in range(4):
        for j in range(4):
            state[i][j] = sbox(state[i][j])

    return state

def shift_rows(state):

    for i in range(4):
        state[i] = state[i][i:] + state[i][:i]

    return state

def mix_columns(state):

    for col in range(4):

        a = state[0][col]
        b = state[1][col]
        c = state[2][col]
        d = state[3][col]

        r0 = (gf_multiply(a, 0x02) ^ gf_multiply(b, 0x03) ^ c ^ d)

        r1 = (a ^ gf_multiply(b, 0x02) ^ gf_multiply(c, 0x03) ^ d)

        r2 = (a ^b ^ gf_multiply(c, 0x02) ^ gf_multiply(d, 0x03))

        r3 = (gf_multiply(a, 0x03) ^ b ^ c ^ gf_multiply(d, 0x02))

        state[0][col] = r0
        state[1][col] = r1
        state[2][col] = r2
        state[3][col] = r3

    return state

def add_round_key(state, round_key):

    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]

    return state

def aes_round(state, round_key):

    state = sub_bytes(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, round_key)

    return state

def aes_final_round(state, round_key):

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_key)

    return state

state = [
    [0x19, 0xA0, 0x9A, 0xE9],
    [0x3D, 0xF4, 0xC6, 0xF8],
    [0xE3, 0xE2, 0x8D, 0x48],
    [0xBE, 0x2B, 0x2A, 0x08]
]

round_key = [
    [0xA0, 0x88, 0x23, 0x2A],
    [0xFA, 0x54, 0xA3, 0x6C],
    [0xFE, 0x2C, 0x39, 0x76],
    [0x17, 0xB1, 0x39, 0x05]
]

result = aes_round(state, round_key)

for row in result:
    print([hex(x) for x in row])