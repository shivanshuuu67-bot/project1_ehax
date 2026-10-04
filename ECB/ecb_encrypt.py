def bytes_to_state(data):

    state = []

    for i in range(4):
        row = []

        for j in range(4):
            row.append(data[j * 4 + i])

        state.append(row)

    return state

def state_to_bytes(state):
    data = []

    for col in range(4):
        for row in range(4):
            data.append(state[row][col])

    return data

def rot_word(word):

    return word[1:] + word[:1]

def gf_multiply(a, b):

    result = 0

    for i in range(8):

        if b & 1:
            result ^= a

        if a & 0x80:
            a = (a << 1) ^ 0x1B
        else:
            a <<= 1

        a &= 0xFF
        b >>= 1

    return result


def multiplicative_inverse(a):

    if a == 0:
        return 0

    for b in range(1, 256):

        if gf_multiply(a, b) == 1:
            return b

def rotate_left(byte, n):
    return ((byte << n) | (byte >> (8 - n))) & 0xFF

def affine_transform(x):

    result = x

    result ^= rotate_left(x, 1)
    result ^= rotate_left(x, 2)
    result ^= rotate_left(x, 3)
    result ^= rotate_left(x, 4)

    result ^= 0x63

    return result

def sbox(byte):

    inverse = multiplicative_inverse(byte)

    result = affine_transform(inverse)

    return result

def sub_bytes(state):

    for i in range(4):
        for j in range(4):
            state[i][j] = sbox(state[i][j])

    return state

def sub_word(word):

    result = []

    for byte in word:
        result.append(sbox(byte))

    return result

rcon = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

def g(word, round_number):

    word = rot_word(word)

    word = sub_word(word)

    word[0] ^= rcon[round_number - 1]

    return word

def key_expansion(key):

    words = []

    # Split original 16-byte key into 4 words
    for i in range(0, 16, 4):
        words.append(key[i:i+4])

    # Generate remaining 40 words
    for round_number in range(1, 11):

        w0 = words[-4]
        w1 = words[-3]
        w2 = words[-2]
        w3 = words[-1]

        w4 = [a ^ b for a, b in zip(w0, g(w3, round_number))]
        w5 = [a ^ b for a, b in zip(w1, w4)]
        w6 = [a ^ b for a, b in zip(w2, w5)]
        w7 = [a ^ b for a, b in zip(w3, w6)]

        words.extend([w4, w5, w6, w7])

    return words

def make_round_keys(words):

    round_keys = []

    for i in range(0, 44, 4):

        words_for_round = words[i:i+4]

        round_key = []

        for row in range(4):

            current_row = []

            for word in words_for_round:
                current_row.append(word[row])

            round_key.append(current_row)

        round_keys.append(round_key)

    return round_keys


def shift_rows(state):

    for i in range(4):
        state[i] = state[i][i:] + state[i][:i]

    return state

def mix_columns(state):

    for col in range(4):

        a = state[0][col]
        b = state[1][col]
        c = state[2][col]
        d = state[3][col]

        r0 = (gf_multiply(a, 0x02) ^ gf_multiply(b, 0x03) ^ c ^ d)

        r1 = (a ^ gf_multiply(b, 0x02) ^ gf_multiply(c, 0x03) ^ d)

        r2 = (a ^b ^ gf_multiply(c, 0x02) ^ gf_multiply(d, 0x03))

        r3 = (gf_multiply(a, 0x03) ^ b ^ c ^ gf_multiply(d, 0x02))

        state[0][col] = r0
        state[1][col] = r1
        state[2][col] = r2
        state[3][col] = r3

    return state

def add_round_key(state, round_key):

    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]

    return state

def aes_round(state, round_key):

    state = sub_bytes(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, round_key)

    return state

def final_round(state, round_key):

    state = sub_bytes(state)

    state = shift_rows(state)

    state = add_round_key(state, round_key)

    return state



def aes_encrypt(plaintext, key):

    data = plaintext.encode("utf-8")

    state = bytes_to_state(data)

    words = key_expansion(key)

    round_keys = make_round_keys(words)

    # Initial AddRoundKey
    state = add_round_key(state, round_keys[0])

    # Rounds 1–9
    for round_number in range(1, 10):
        state = aes_round(state, round_keys[round_number])

    # Round 10 
    state = final_round(state, round_keys[10])

    # Convert final state → ciphertext
    cipher_bytes = state_to_bytes(state)
    ciphertext = ''.join(f'{byte:02x}' for byte in cipher_bytes)

    return ciphertext

def ecb_encrypt(data, key):

    ciphertext = ""

    for i in range(0, len(data), 16):

        block = data[i:i+16]

        encrypted_block = aes_encrypt(block, key)

        ciphertext += encrypted_block

    return ciphertext

key = [
    0x00, 0x01, 0x02, 0x03,
    0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b,
    0x0c, 0x0d, 0x0e, 0x0f
]

data = "abcdefghijklmnop" + "qrstuvwxyzabcdef"

ciphertext = ecb_encrypt(data, key)

print(ciphertext)
print(len(ciphertext))