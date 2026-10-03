def byte_to_polynomial(byte):
    terms = []

    for i in range(8):
        if byte & (1 << i): 
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("x")
            else:
                terms.append(f"x^{i}")
        
    return " + ".join(reversed(terms))


a = 0x57
b = 0x83
result = a ^ b

print("A:", byte_to_polynomial(a))
print("B:", byte_to_polynomial(b))
print("A XOR B:", byte_to_polynomial(result))