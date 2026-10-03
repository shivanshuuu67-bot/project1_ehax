text = "HELLOWORLD"
key = "KEY"

repeated_key = ""

for i in range(len(text)):
    repeated_key += key[i % len(key)]

print(repeated_key)

text = "HELLO"

for char in text:
    value = ord(char) - ord('A')
    print(char, "=", value)