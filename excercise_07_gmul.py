def gmul(a, b):

    result = 0

    for i in range(8):

        if b & 1:
            result ^= a

        a <<= 1

        if a & 0x100:
            a ^= 0x11B

        b >>= 1

    return result

print(hex(gmul(0x57, 0x83)))

"""
def gmul(a, b):

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
"""