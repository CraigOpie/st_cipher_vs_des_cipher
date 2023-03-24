#!/usr/bin/env python3
# Initial Permutation (IP) table
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_inv = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
]

# Final Permutation (FP) table
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

# Permuted Choice 1 (PC-1) table
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# Permuted Choice 2 (PC-2) table
PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

# Left shift schedule for each round
LS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Expansion (E) table
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# Substitution boxes (S-boxes)
S = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ]
]

# Permutation (P) table
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

def initial_permutation(plaintext):
    # Apply the Initial Permutation (IP)
    return ''.join([plaintext[IP[i] - 1] for i in range(64)])

def final_permutation(ciphertext):
    # Apply the Final Permutation (FP)
    return ''.join([ciphertext[FP[i] - 1] for i in range(64)])

def des_encrypt(plaintext, key):
    if len(plaintext) != 8:  # Ensure the plaintext is 8 bytes (64 bits) long
        raise ValueError("Plaintext must be 8 bytes long")

    # Convert the plaintext to a binary string
    plaintext = ''.join(format(ord(c), '08b') for c in plaintext)

    # Apply the initial permutation
    plaintext = ''.join([plaintext[IP[i] - 1] for i in range(64)])

    # Run the core DES cipher with the given key and encryption mode
    ciphertext = des_cipher(plaintext, key, mode='encrypt')

    return ciphertext


def des_decrypt(ciphertext, key):
    if len(ciphertext) != 64:  # Ensure the ciphertext is 64 bits long
        raise ValueError("Ciphertext must be 64 bits long")

    # Run the core DES cipher with the given key and decryption mode
    decrypted_text = des_cipher(ciphertext, key, mode='decrypt')

    # Apply the inverse initial permutation
    decrypted_text = ''.join([decrypted_text[IP_inv[i] - 1] for i in range(64)])

    # Convert the binary string to plaintext
    plaintext = ''.join(chr(int(decrypted_text[i:i + 8], 2)) for i in range(0, len(decrypted_text), 8))

    return plaintext


def des_cipher(plaintext, key, mode='encrypt'):
    # Split the plaintext into left (L0) and right (R0) halves
    L0, R0 = plaintext[:32], plaintext[32:]

    # Key scheduling: Generate the 16 round keys from the input key
    round_keys = key_scheduling(key)

    # Reverse the round keys for decryption
    if mode == 'decrypt':
        round_keys = round_keys[::-1]

    # 16 rounds of the Feistel network
    L, R = L0, R0
    for i in range(16):
        new_L = R
        new_R = xor(L, f(R, round_keys[i]))  # f() represents the round function
        L, R = new_L, new_R

    # Combine the final left and right halves
    combined_text = L + R

    return combined_text

def xor(a, b):
    # XOR function for bit strings
    return ''.join('1' if a[i] != b[i] else '0' for i in range(len(a)))

def key_scheduling(key):
    if len(key) != 8:  # Ensure the key is 8 bytes (64 bits) long
        raise ValueError("Key must be 8 bytes long")

    # Convert the key to a binary string
    key = ''.join(format(ord(c), '08b') for c in key)

    # Apply the Permuted Choice 1 (PC-1)
    permuted_key = ''.join([key[PC1[i] - 1] for i in range(56)])

    # Split the permuted_key into left (C) and right (D) halves
    C, D = permuted_key[:28], permuted_key[28:]

    # Generate the 16 round keys
    round_keys = []
    for i in range(16):
        # Perform left shifts on C and D according to the LS table
        C = left_shift(C, LS[i])
        D = left_shift(D, LS[i])

        # Combine C and D and apply the Permuted Choice 2 (PC-2)
        CD = C + D
        round_key = ''.join([CD[PC2[i] - 1] for i in range(48)])

        round_keys.append(round_key)

    return round_keys

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def f(R, round_key):
    # Expansion (E) of the right half (R)
    expanded_R = ''.join([R[E[i] - 1] for i in range(48)])

    # XOR with the round key
    xor_result = xor(expanded_R, round_key)

    # Substitution using the S-boxes
    substituted = ''
    for i in range(8):
        row = int(xor_result[i*6] + xor_result[i*6 + 5], 2)
        col = int(xor_result[i*6 + 1:i*6 + 5], 2)
        substituted += format(S[i][row][col], '04b')

    # Permutation (P)
    permuted = ''.join([substituted[P[i] - 1] for i in range(32)])

    return permuted

def main():
    # Your plaintext message and key
    plaintext = "64bittxt"
    key = "bethekey"

    # Encrypt the plaintext using DES
    ciphertext = des_encrypt(plaintext, key)
    print(f"Encrypted message (ciphertext): {ciphertext}")

    # Decrypt the ciphertext using DES
    decrypted_text = des_decrypt(ciphertext, key)
    print(f"Decrypted message (plaintext): {decrypted_text}")

if __name__ == "__main__":
    main()