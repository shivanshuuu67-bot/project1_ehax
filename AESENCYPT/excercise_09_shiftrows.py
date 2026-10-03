state = [
    [0x00, 0x04, 0x08, 0x0C],
    [0x01, 0x05, 0x09, 0x0D],
    [0x02, 0x06, 0x0A, 0x0E],
    [0x03, 0x07, 0x0B, 0x0F]
]

def shift_rows(state):

    for i in range(4):
        state[i] = state[i][i:] + state[i][:i]

    return state


shifted = shift_rows(state)

for row in shifted:
    print([hex(x) for x in row])