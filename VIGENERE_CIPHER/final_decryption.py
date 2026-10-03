def vigenere_decrypt(text, key):

    decrypted = ""

    for i in range(len(text)):

        c = ord(text[i]) - ord('A')
        k = ord(key[i % len(key)]) - ord('A')

        p = (c - k) % 26

        decrypted += chr(p + ord('A'))

    return decrypted

result = vigenere_decrypt("RIJVS", "KEY")

print(result)