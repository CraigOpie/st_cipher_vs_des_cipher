#!/usr/bin/env python3
import math

def caesar_cipher(text, shift, mode):
    """
    Caesar cipher: a simple substitution cipher
    - text: input string (plaintext or ciphertext)
    - shift: number of positions each character is shifted
    - mode: 'encrypt' or 'decrypt'
    """
    result = ""
    shift = -shift if mode == 'decrypt' else shift

    for char in text:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            result += chr(((ord(char) - offset + shift) % 26) + offset)
        else:
            result += char
    return result

def columnar_transposition(text, key, mode):
    """
    Columnar transposition cipher: a simple transposition cipher
    - text: input string (plaintext or ciphertext)
    - key: string representing the transposition key
    - mode: 'encrypt' or 'decrypt'
    """
    key_order = sorted(range(len(key)), key=lambda x: key[x])
    num_columns = len(key)
    num_rows = int(math.ceil(len(text) / float(num_columns)))

    if mode == 'encrypt':
        padding = num_columns * num_rows - len(text)
        text += padding * 'X'
        matrix = [text[i:i+num_columns] for i in range(0, len(text), num_columns)]
        ciphertext = ''
        for col in key_order:
            ciphertext += ''.join([matrix[i][col] for i in range(num_rows)])
        return ciphertext
    elif mode == 'decrypt':
        num_padding = sum(1 for i in range(len(text) - num_columns, len(text)) if text[i] == 'X')
        text_segments = [''] * num_columns
        col_size = num_rows - (num_padding > 0)
        for i, col in enumerate(key_order):
            segment_size = col_size + (i < num_padding)
            text_segments[col] = text[:segment_size]
            text = text[segment_size:]
        return ''.join([''.join(row) for row in zip(*text_segments)])

def st_cipher(text, substitution_key, transposition_key, mode):
    """
    ST cipher: combines Caesar cipher (substitution) and columnar transposition cipher (transposition)
    - text: input string (plaintext or ciphertext)
    - substitution_key: integer representing the shift for the Caesar cipher
    - transposition_key: string representing the transposition key for the columnar transposition cipher
    - mode: 'encrypt' or 'decrypt'
    """
    if mode == 'encrypt':
        substituted = caesar_cipher(text, substitution_key, mode)
        return columnar_transposition(substituted, transposition_key, mode)
    elif mode == 'decrypt':
        transposed = columnar_transposition(text, transposition_key, mode)
        return caesar_cipher(transposed, substitution_key, mode)

plaintext = "HELLO, THIS IS A MESSAGE"
substitution_key = 3
transposition_key = "KEY"

ciphertext = st_cipher(plaintext, substitution_key, transposition_key, 'encrypt')
print(f"Ciphertext: {ciphertext}")

decrypted_text = st_cipher(ciphertext, substitution_key, transposition_key, 'decrypt')
print(f"Decrypted text: {decrypted_text}")