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

def inv_mix_columns(state):

    for col in range(4):

        a0 = state[0][col]
        a1 = state[1][col]
        a2 = state[2][col]
        a3 = state[3][col]

        state[0][col] = (gf_multiply(a0, 0x0E) ^ gf_multiply(a1, 0x0B) ^ gf_multiply(a2, 0x0D) ^ gf_multiply(a3, 0x09))

        state[1][col] = (gf_multiply(a0, 0x09) ^ gf_multiply(a1, 0x0E) ^ gf_multiply(a2, 0x0B) ^ gf_multiply(a3, 0x0D))

        state[2][col] = (gf_multiply(a0, 0x0D) ^ gf_multiply(a1, 0x09) ^ gf_multiply(a2, 0x0E) ^ gf_multiply(a3, 0x0B))

        state[3][col] = (gf_multiply(a0, 0x0B) ^ gf_multiply(a1, 0x0D) ^ gf_multiply(a2, 0x09) ^ gf_multiply(a3, 0x0E))

    return state

state = [
    [0xdb, 0x13, 0x53, 0x45],
    [0x13, 0x53, 0x45, 0xdb],
    [0x53, 0x45, 0xdb, 0x13],
    [0x45, 0xdb, 0x13, 0x53]
]

state = inv_mix_columns(state)

for row in state:
    print([hex(x) for x in row])