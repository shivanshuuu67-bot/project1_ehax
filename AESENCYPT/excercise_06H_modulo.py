def xtime(a):
    if a & 0x80:
        return ((a << 1) ^ 0x1B) & 0xFF
    else:
        return (a << 1) & 0xFF


def gf_multiply(a, b):
    result = 0

    for i in range(8):
        if b & 1:
            result ^= a

        a = xtime(a)
        b >>= 1

    return result


print(hex(gf_multiply(0x57, 0x83)))