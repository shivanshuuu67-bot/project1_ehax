def rot_word(word):

    return word[1:] + word[:1]

word = [0x09, 0xCF, 0x4F, 0x3C]

print([hex(x) for x in rot_word(word)])