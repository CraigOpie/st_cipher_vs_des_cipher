# ST Cipher vs DES Cipher

This README provides an overview of the differences between simple substitution-transposition (ST) ciphers and the Data Encryption Standard (DES) cipher. It includes explanations of key terms, the structure of a Feistel network, and how DES solves the problems posed by ST ciphers. Additionally, it references Python programs demonstrating ST and DES ciphers.

## Key Terms

- **Confusion**: The property of a cipher that obscures the relationship between the plaintext and the ciphertext, typically achieved through substitution.
- **Diffusion**: The property of a cipher that dissipates the redundancy of the plaintext across the ciphertext, typically achieved through transposition or permutation.
- **Ideal Cipher**: A hypothetical cipher that provides perfect secrecy, meaning the ciphertext reveals no information about the plaintext without the key. An ideal cipher is a theoretical construct in which every possible plaintext-ciphertext pair is equally likely, assuming a randomly chosen key. No real-world cipher can be truly ideal, but good ciphers strive to approach this property.
- **Perfect Cipher**: A cipher where the ciphertext, key, and plaintext are all equally probable and independent. A perfect cipher is a cipher that cannot be broken, even with unlimited computational resources. The one-time pad, which uses a truly random key the same length as the plaintext, is an example of a perfect cipher. However, perfect ciphers are often impractical for real-world use due to key management and distribution challenges.
- **Idempotent**: A mathematical operation that, when applied multiple times, has the same effect as if it were applied only once.
- **Redundancy**: The presence of predictable patterns or repetitions in the plaintext, which can make it easier for attackers to perform frequency analysis or other types of cryptanalysis. A good cipher should minimize redundancy in the ciphertext to resist such attacks.

## ST Ciphers

An ST cipher is a classical encryption scheme that combines substitution and transposition techniques. Substitution replaces each character in the plaintext with another character, while transposition changes the order of the characters. An ST cipher aims to achieve two cryptographic properties: *confusion* and *diffusion*. Confusion refers to the relationship between the plaintext, ciphertext, and the key, making it difficult to identify the key even if parts of the plaintext and ciphertext are known. Diffusion means that small changes in the plaintext result in significant changes in the ciphertext, making it challenging to identify patterns or relationships between them.

### Problems with ST Ciphers

1. **Susceptibility to frequency analysis**: Simple ST ciphers can be vulnerable to frequency analysis attacks, which exploit patterns in the ciphertext.
1. **Limited key space**: Classical ST ciphers often have a limited key space, making them susceptible to brute-force attacks.
1. **Insufficient confusion and diffusion**: Classical ST ciphers might not provide adequate confusion (relationship between plaintext, ciphertext, and key) and diffusion (spreading of plaintext patterns in the ciphertext) properties, making it easier for attackers to decipher the ciphertext.

### Python Code for ST Cipher

A simple Python program demonstrating an ST cipher using the Caesar cipher for substitution and a columnar transposition cipher for transposition can be found in the **`st_cipher.py`** file.

## Data Encryption Standard (DES)

DES is a symmetric-key block cipher that was designed to address the weaknesses of classical ST ciphers by providing stronger confusion and diffusion properties, which help protect against attacks such as frequency analysis and brute force. It operates on 64-bit blocks of data and uses a 56-bit key.

### How DES Solves ST Cipher Problems

1. **Increased complexity**: DES employs a complex Feistel network structure with 16 rounds, making it harder for attackers to analyze the relationship between the plaintext and ciphertext.
1. **Enhanced confusion and diffusion properties**: DES combines substitution and permutation operations within its round function, providing better confusion and diffusion. The S-boxes introduce non-linearity and confusion, while the expansion and permutation steps provide strong diffusion properties.
1. **Key scheduling**: DES uses a sophisticated key scheduling mechanism that generates a unique round key for each of the 16 rounds. This process makes it harder for attackers to derive the encryption key from the ciphertext.
1. **Resistance to known attacks**: DES was designed with knowledge of existing attacks on classical ST ciphers, making it resistant to frequency analysis and brute-force attacks.

It's important to note that despite addressing the weaknesses of ST ciphers, DES itself has been considered insecure for many years due to advances in computing power and the development of more efficient attacks, such as differential and linear cryptanalysis. The Advanced Encryption Standard (AES) has since replaced DES as the recommended symmetric-key encryption standard, offering a higher level of security and resistance to modern attacks.

### Python Code for DES Cipher

A Python program demonstrating the DES cipher using the **`pycryptodome`** library can be found in the **`des_cipher.py`** file. The program illustrates how to use the library for encryption and decryption with DES, while addressing the problems posed by ST ciphers.

## Feistel Network Structure

A Feistel network is a symmetric structure used in the construction of block ciphers, including DES. It is named after Horst Feistel, a German-American cryptographer who developed the structure in the 1970s. The Feistel network combines the principles of confusion and diffusion to achieve a higher level of security compared to classical ST ciphers. It consists of multiple rounds, each performing a specific set of operations on the input data. The key features of a Feistel network include:

1. The input data (plaintext) is divided into two halves, the left half (L) and the right half (R).
1. A round function F is applied to one half of the data (usually the right half, R) and the output is combined (typically using the XOR operation) with the other half (left half, L).
1. The resulting halves are then swapped, with the modified left half becoming the new right half and the original right half becoming the new left half.
1. These steps are repeated for a fixed number of rounds, with each round using a different round key derived from the original encryption key.

After the final round, the two halves are combined to form the ciphertext. The round function F, which is key to the Feistel network's security, introduces confusion and diffusion properties by applying substitution and permutation operations on the data. The repeated application of the round function across multiple rounds increases the overall complexity of the cipher and makes it resistant to various attacks, including frequency analysis.

One notable property of the Feistel network is that the encryption and decryption processes are almost identical. The main difference is the order in which the round keys are applied. This property simplifies the implementation of encryption and decryption algorithms and reduces the chances of introducing errors.

### DES Round Function

In a Feistel network, the round function F is used to process one half of the data while the other half is left unchanged during each round. In the context of DES, the Feistel network consists of 16 rounds, and the round function F is applied in each round. Here's a step-by-step explanation of how the DES round function is used within a Feistel network to give a DES round:

1. **Split the input data**: The 64-bit input data (plaintext) is divided into two equal halves, the left half (L) and the right half (R), each containing 32 bits.
1. **Apply the round function F to the right half (R)**: The round function F performs the following operations on the right half of the input data, as previously described:
    1. **Expansion**: The right half (R) is expanded from 32 bits to 48 bits.
    1. **Key Mixing**: The expanded data is XORed with the current 48-bit round key.
    1. **Substitution**: The data is passed through 8 substitution boxes (S-boxes), reducing it from 48 bits to 32 bits.
    1. **Permutation**: A permutation is applied to the output of the substitution step.
1. **Combine the output of F with the left half (L)**: The 32-bit output from the round function F is combined with the left half (L) of the input data using the XOR operation. The result becomes the new right half (R') for the next round.
1. **Swap the halves**: The original right half (R) becomes the new left half (L'), and the result from step 3 (R') becomes the new right half for the next round.

These steps are performed for each of the 16 rounds in the DES Feistel network. After the final round, the left and right halves are combined to form the 64-bit ciphertext. It's important to note that the order of the round keys is reversed for decryption, but the process remains almost identical, making it easy to implement both encryption and decryption using the Feistel network structure.