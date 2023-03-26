#!/usr/bin/env python3
import lib.constants as lib

def permutate(list_to_permutate, ref_table):
    """Permutate a list using the specified table"""
    return [list_to_permutate[x - 1] for x in ref_table]

def text_to_binary(plaintext):
    # Convert the plaintext to a binary string
    binary_text = ''.join(format(ord(c), '08b') for c in plaintext)
    return [int(bit, 2) for bit in binary_text]

def binary_to_text(binary_text):
    binary_text = ''.join([str(bit) for bit in binary_text])
    return ''.join(chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8))

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def key_scheduling(key):
    if len(key) != 8:  # Ensure the key is 8 bytes (64 bits) long
        raise ValueError("Key must be 8 bytes long")

    # Convert the key to a binary string
    key = text_to_binary(key)

    # Apply the Permuted Choice 1 (PC-1)
    permuted_key = permutate(key, lib.PC1)

    # Split the permuted_key into left (C) and right (D) halves
    C, D = permuted_key[:28], permuted_key[28:]

    # Generate the 16 round keys
    round_keys = []
    for i in range(16):
        # Perform left shifts on C and D according to the LS table
        C = left_shift(C, lib.LS[i])
        D = left_shift(D, lib.LS[i])

        # Combine C and D and apply the Permuted Choice 2 (PC-2)
        CD = C + D
        round_key = permutate(CD, lib.PC2)

        round_keys.append(round_key)

    return round_keys

def des_cipher(text, key, mode='encrypt'):
    # Key scheduling: Generate the 16 round keys from the input key
    round_keys = key_scheduling(key)

    if mode == 'encrypt':
        if len(text) != 8:  # Ensure the plaintext is 8 bytes (64 bits) long
            raise ValueError("Plaintext must be 8 bytes long")
        text = text_to_binary(text)
        text = permutate(text, lib.IP)
    else:
        if len(text) != 64:  # Ensure the ciphertext is 64 bits long
            raise ValueError("Ciphertext must be 64 bits long")

    # Split the plaintext into left and right halves
    left, right = text[:32], text[32:]

    # 16 rounds of the Feistel network
    iterations = range(16) if mode == 'encrypt' else reversed(range(16))
    for i in iterations:
        # Save a copy of right to use as the new left
        temp = right[:]
        
        # Expand right to match key size and xor with key
        right = permutate(right, lib.E)
        right = [r ^ k for r, k in zip(right, round_keys[i])]

        # Apply S-boxes
        chunks = [right[x:x+6] for x in range(0, 48, 6)]
        Bn = []
        for j, chunk in enumerate(chunks):
            m = (chunk[0] << 1) + chunk[5]
            n = ((chunk[1] << 3) + (chunk[2] << 2) + (chunk[3] << 1) + chunk[4])
            v = lib.S_BOXES[j][(m << 4) + n]
            Bn += [(v >> x) & 1 for x in reversed(range(4))]
        right = permutate(Bn, lib.P)
        
        # Xor with left
        right = [r ^ l for r, l in zip(right, left)]
        left = temp

    # Combine the final left and right halves
    combined_text = left + right

    # Final permutation
    final = permutate(combined_text, lib.FP)

    if mode == 'decrypt':
        final = binary_to_text(final)
        
    return final

def main():
    # Your plaintext message and key
    plaintext = "64bittxt"
    key = "bethekey"

    # Encrypt the plaintext using DES
    ciphertext = des_cipher(plaintext, key, 'encrypt')
    print(f"Encrypted message (ciphertext): {ciphertext}")

    # Decrypt the ciphertext using DES
    decrypted_text = des_cipher(ciphertext, key, 'decrypt')
    print(f"Decrypted message (plaintext):  {decrypted_text}")

if __name__ == "__main__":
    main()
