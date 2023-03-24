#!/usr/bin/env python
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def des_cipher(key, plaintext, mode):
    """
    DES cipher: Encrypts the plaintext using the key
    - key: 8-byte (64-bit) key, of which 56 bits are used for encryption
    - plaintext: input string (plaintext)
    - mode: DES.MODE_ECB or DES.MODE_CBC, to specify the block cipher mode
    """
    cipher = DES.new(key, mode)
    return cipher.encrypt(pad(plaintext.encode(), DES.block_size))

def des_decipher(key, ciphertext, mode):
    """
    DES decipher: Decrypts the ciphertext using the key
    - key: 8-byte (64-bit) key, of which 56 bits are used for decryption
    - ciphertext: input string (ciphertext)
    - mode: DES.MODE_ECB or DES.MODE_CBC, to specify the block cipher mode
    """
    cipher = DES.new(key, mode)
    return unpad(cipher.decrypt(ciphertext), DES.block_size).decode()

# DES uses a 64-bit key, but only 56 bits are effectively used for encryption
key = get_random_bytes(8)

plaintext = "HELLO, THIS IS A MESSAGE"
mode = DES.MODE_ECB  # Electronic Codebook mode

# DES addresses the problems posed by ST ciphers through a more complex structure,
# multiple rounds, and strong confusion and diffusion properties.
ciphertext = des_cipher(key, plaintext, mode)
print(f"Ciphertext: {ciphertext.hex()}")

decrypted_text = des_decipher(key, ciphertext, mode)
print(f"Decrypted text: {decrypted_text}")