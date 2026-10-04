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

s_box = []

for i in range(256):
    s_box.append(sbox(i))

inv_s_box = [0] * 256

for i in range(256):
    inv_s_box[s_box[i]] = i

def inv_sub_bytes(state):

    for row in range(4):
        for col in range(4):
            state[row][col] = inv_s_box[state[row][col]]

    return state

def inv_shift_rows(state):

    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]

    return state

def inv_mix_columns(state):

    for col in range(4):

        a0 = state[0][col]
        a1 = state[1][col]
        a2 = state[2][col]
        a3 = state[3][col]

        state[0][col] = (gf_multiply(a0, 0x0E) ^ gf_multiply(a1, 0x0B) ^ gf_multiply(a2, 0x0D) ^ gf_multiply(a3, 0x09))

        state[1][col] = (gf_multiply(a0, 0x09) ^ gf_multiply(a1, 0x0E) ^ gf_multiply(a2, 0x0B) ^ gf_multiply(a3, 0x0D))

        state[2][col] = (gf_multiply(a0, 0x0D) ^ gf_multiply(a1, 0x09) ^ gf_multiply(a2, 0x0E) ^ gf_multiply(a3, 0x0B))

        state[3][col] = (gf_multiply(a0, 0x0B) ^ gf_multiply(a1, 0x0D) ^ gf_multiply(a2, 0x09) ^ gf_multiply(a3, 0x0E))

    return state

def add_round_key(state, round_key):

    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]

    return state

def rot_word(word):

    return word[1:] + word[:1]

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



def aes_decrypt(state, round_keys):

    # Initial AddRoundKey
    state = add_round_key(state, round_keys[10])

    # Rounds 9 → 1
    for round_number in range(9, 0, -1):

        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, round_keys[round_number])
        state = inv_mix_columns(state)

    # Final round
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, round_keys[0])

    return state

def ecb_decrypt(ciphertext, key):

    ciphertext_bytes = list(bytes.fromhex(ciphertext))

    words = key_expansion(key)
    round_keys = make_round_keys(words)

    plaintext = []

    for i in range(0, len(ciphertext_bytes), 16):

        block = ciphertext_bytes[i:i+16]

        state = bytes_to_state(block)

        state = aes_decrypt(state, round_keys)

        decrypted_block = state_to_bytes(state)

        plaintext.extend(decrypted_block)

    return plaintext

key = [
    0x00, 0x01, 0x02, 0x03,
    0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b,
    0x0c, 0x0d, 0x0e, 0x0f
]

ciphertext = "d25363fc721337648a68f34abef3b405"

plaintext = ecb_decrypt(ciphertext, key)

print(plaintext)
print(bytes(plaintext).decode("utf-8"))