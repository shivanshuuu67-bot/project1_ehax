numbers = [17, 29, 32, 255, 256, 257]
modulus = 26

for number in numbers:
    print(number, "%", modulus, "=", number % modulus)