import os

print("Current directory:", os.getcwd())

with open("input.txt", "r") as file:
    plaintext = file.read()

print(plaintext)