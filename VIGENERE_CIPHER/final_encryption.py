def vigenere_encrypt(text, key):

    encrypted = ""

    for i in range(len(text)):

        p = ord(text[i]) - ord('A')
        k = ord(key[i % len(key)]) - ord('A')

        c = (p + k) % 26

        encrypted += chr(c + ord('A'))

    return encrypted

result = vigenere_encrypt("HELLO", "KEY")

print(result)