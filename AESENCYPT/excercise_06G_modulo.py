def xtime(a):

    if a & 0x80:
        return ((a << 1) ^ 0x1B) & 0xFF #or we can use return ((a << 1) ^ 0x11B) but this one is optimized for 8 bits (the one in the code)
    else:
        return (a << 1) & 0xFF


print(hex(xtime(0x57)))
print(hex(xtime(0x83)))