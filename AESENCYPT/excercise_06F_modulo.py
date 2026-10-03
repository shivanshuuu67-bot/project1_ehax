a = 0x57

result = a << 1

print(hex(result))

a = 0x83

result = a << 1

print(hex(result))

def xtime(a):

    if a & 0x80:
        return ((a << 1) ^ 0x1B) & 0xFF #or we can use return ((a << 1) ^ 0x11B)
    else:
        return (a << 1) & 0xFF


print(hex(xtime(0x57)))
print(hex(xtime(0x83)))