#!/usr/bin/env python3
import math

def caesar_cipher(text, shift, mode):
    """Encrypt or decrypt a string using the Caesar cipher.

    Args:
        text (str): The text to be encrypted or decrypted.
        shift (int): The shift value for the Caesar cipher.
        mode (str): The mode of operation ('encrypt' or 'decrypt').

    Returns:
        str: The encrypted or decrypted text.
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
    """Encrypt or decrypt a string using the columnar transposition cipher.

    Args:
        text (str): The text to be encrypted or decrypted.
        key (str): The key for the columnar transposition cipher.
        mode (str): The mode of operation ('encrypt' or 'decrypt').

    Returns:
        str: The encrypted or decrypted text.
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
    """Encrypt or decrypt a string using a substitution-transposition cipher.

    Args:
        text (str): The text to be encrypted or decrypted.
        substitution_key (int): The key for the Caesar substitution cipher.
        transposition_key (str): The key for the columnar transposition cipher.
        mode (str): The mode of operation ('encrypt' or 'decrypt').

    Returns:
        str: The encrypted or decrypted text.
    """
    if mode == 'encrypt':
        substituted = caesar_cipher(text, substitution_key, mode)
        return columnar_transposition(substituted, transposition_key, mode)
    elif mode == 'decrypt':
        transposed = columnar_transposition(text, transposition_key, mode)
        return caesar_cipher(transposed, substitution_key, mode)

def main():
    """Main function."""
    plaintext = 'HELLO, THIS IS A MESSAGE'
    substitution_key = 3
    transposition_key = 'KEY'

    print(f'Plaintext: {plaintext}')

    ciphertext = st_cipher(plaintext, substitution_key, transposition_key, 'encrypt')
    print(f'Ciphertext: {ciphertext}')

    decrypted_text = st_cipher(ciphertext, substitution_key, transposition_key, 'decrypt')
    print(f'Decrypted text: {decrypted_text}')

if __name__ == "__main__":
    main()
