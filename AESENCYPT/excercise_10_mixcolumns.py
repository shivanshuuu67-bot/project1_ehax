def gf_multiply(a, b):

    result = 0

    for i in range(8):

        if b & 1:
            result ^= a

        a <<= 1

        if a & 0x100:
            a ^= 0x11B

        b >>= 1

    return result

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

state = [
    [0x00, 0x04, 0x08, 0x0C],
    [0x01, 0x05, 0x09, 0x0D],
    [0x02, 0x06, 0x0A, 0x0E],
    [0x03, 0x07, 0x0B, 0x0F]
]

result = mix_columns(state)

for row in result:
    print([hex(x) for x in row])