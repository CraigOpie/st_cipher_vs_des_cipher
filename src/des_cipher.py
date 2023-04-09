#!/usr/bin/env python3
from typing import List, Union

class DES:
    """A class for implementing the Data Encryption Standard (DES) symmetric-key block cipher."""
    ENCRYPT = 0
    DECRYPT = 1
    BLOCK_SIZE = 8
    BYTE_SIZE = 8
    KEY_SIZE = 8
    PAD_PKCS5 = 2
    HALF_KEY_SIZE = 28
    KEY_COMBINED_SIZE = 32
    FULL_BLOCK_SIZE = 48
    S_BOX_INPUT_SIZE = 6
    S_BOX_OUTPUT_SIZE = 4
    
    class Blocks:
        """A nested class to hold block configurations for DES."""
        def __init__(self):
            pass
    
        pc1: List[int] = [
            56, 48, 40, 32, 24, 16,  8,  0,
            57, 49, 41, 33, 25, 17,  9,  1,
            58, 50, 42, 34, 26, 18, 10,  2,
            59, 51, 43, 35, 62, 54, 46, 38,
            30, 22, 14,  6, 61, 53, 45, 37,
            29, 21, 13,  5, 60, 52, 44, 36,
            28, 20, 12,  4, 27, 19, 11,  3
        ]

        pc2: List[int] = [
            13, 16, 10, 23,  0,  4,  2, 27,
            14,  5, 20,  9, 22, 18, 11,  3,
            25,  7, 15,  6, 26, 19, 12,  1,
            40, 51, 30, 36, 46, 54, 29, 39,
            50, 44, 32, 47, 43, 48, 38, 55,
            33, 52, 45, 41, 49, 35, 28, 31
        ]

        left_rotations: List[int] = [
            1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
        ]

        initial_permutation: List[int] = [
            57, 49, 41, 33, 25, 17,  9,  1,
            59, 51, 43, 35, 27, 19, 11,  3,
            61, 53, 45, 37, 29, 21, 13,  5,
            63, 55, 47, 39, 31, 23, 15,  7,
            56, 48, 40, 32, 24, 16,  8,  0,
            58, 50, 42, 34, 26, 18, 10,  2,
            60, 52, 44, 36, 28, 20, 12,  4,
            62, 54, 46, 38, 30, 22, 14,  6
        ]

        straight_permutation: List[int] = [
            15, 6, 19, 20, 28, 11,
            27, 16, 0, 14, 22, 25,
            4, 17, 30, 9, 1, 7,
            23,13, 31, 26, 2, 8,
            18, 12, 29, 5, 21, 10,
            3, 24
        ]

        initial_permutation_reversed: List[int] = [
            39,  7, 47, 15, 55, 23, 63, 31,
            38,  6, 46, 14, 54, 22, 62, 30,
            37,  5, 45, 13, 53, 21, 61, 29,
            36,  4, 44, 12, 52, 20, 60, 28,
            35,  3, 43, 11, 51, 19, 59, 27,
            34,  2, 42, 10, 50, 18, 58, 26,
            33,  1, 41,  9, 49, 17, 57, 25,
            32,  0, 40,  8, 48, 16, 56, 24
        ]
        
        expansion_table: List[int] = [
            31,  0,  1,  2,  3,  4,
            3,  4,  5,  6,  7,  8,
            7,  8,  9, 10, 11, 12,
            11, 12, 13, 14, 15, 16,
            15, 16, 17, 18, 19, 20,
            19, 20, 21, 22, 23, 24,
            23, 24, 25, 26, 27, 28,
            27, 28, 29, 30, 31,  0
        ]

        s_boxes: List[List[int]] = [
            # S1
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
            0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
            4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
            15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

            # S2
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
            3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
            0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
            13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

            # S3
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
            13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
            13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
            1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

            # S4
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
            13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
            10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
            3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

            # S5
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
            14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
            4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
            11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

            # S6
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
            10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
            9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
            4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

            # S7
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
            13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
            1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
            6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

            # S8
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
            1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
            7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
            2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]

    def __init__(self, key: bytes) -> None:
        """Initialize a DES object with the provided key.

        Args:
            key (bytes): The encryption/decryption key, must be exactly 8 bytes long.
        """
        if len(key) != DES.KEY_SIZE:
            raise ValueError(f"Invalid DES key size. Key must be exactly {DES.KEY_SIZE} bytes long.")
        self._iv = b'\0' * DES.BLOCK_SIZE
        self._padmode = DES.PAD_PKCS5
        self._padding = None
        self._key = None
        self.L = []
        self.R = []
        self.Kn = [[0] * 48] * 16
        self.final = []
        self.key = key

    @property
    def key(self) -> bytes:
        """Return the DES key."""
        return self._key

    @key.setter
    def key(self, key: bytes) -> None:
        """Set the DES key.

        Args:
            key (bytes): The encryption/decryption key, must be exactly 8 bytes long.
        """
        key = self.ensure_ascii_encoded(key)
        self._key = key
        self.create_sub_keys()

    @property
    def pad_mode(self) -> int:
        """Return the padding mode used by the DES cipher."""
        return self._padmode

    @property
    def iv(self) -> bytes:
        """Return the initialization vector used by the DES cipher."""
        return self._iv

    @property
    def padding(self) -> None:
        """Return the padding used by the DES cipher."""
        return self._padding

    @staticmethod
    def ensure_ascii_encoded(data: Union[bytes, str]) -> bytes:
        """Ensure that the provided data is ASCII-encoded.

        Args:
            data (Union[bytes, str]): The data to be encoded.

        Returns:
            bytes: The ASCII-encoded data.
        """
        if isinstance(data, str):
            try:
                return data.encode('ascii')
            except UnicodeEncodeError:
                pass
            raise ValueError("This can only work with encoded strings, not Unicode.")
        return data

    def pad_data(self, data: bytes) -> bytes:
        """Pad the provided data according to the chosen padding mode.

        Args:
            data (bytes): The data to be padded.

        Returns:
            bytes: The padded data.
        """
        pad_len = DES.BLOCK_SIZE - (len(data) % DES.BLOCK_SIZE)
        data += bytes([pad_len] * pad_len)
        return data

    def unpad_data(self, data: bytes) -> bytes:
        """Remove padding from the given data.

        Args:
            data (bytes): The data with padding.

        Returns:
            bytes: The data without padding.
        """
        if not data:
            return data

        pad_len = data[-1]
        data = data[:-pad_len]
        return data

    def string_to_bitlist(self, data: bytes) -> List[int]:
        """Convert a byte string to a list of bits.

        Args:
            data (bytes): The byte string to be converted.

        Returns:
            List[int]: The list of bits representing the byte string.
        """
        length = len(data) * DES.BYTE_SIZE
        result = [0] * length
        pos = 0
        for char in data:
            i = DES.BYTE_SIZE - 1
            while i >= 0:
                result[pos] = int(bool(char & (1 << i)))
                pos += 1
                i -= 1
        return result

    def bitlist_to_string(self, data: List[int]) -> bytes:
        """Convert a list of bits to a byte string.

        Args:
            data (List[int]): The list of bits to be converted.

        Returns:
            bytes: The byte string representation of the list of bits.
        """
        result = []
        pos = 0
        c = 0
        while pos < len(data):
            c += data[pos] << ((DES.BYTE_SIZE - 1) - (pos % DES.BYTE_SIZE))
            if (pos % DES.BYTE_SIZE) == (DES.BYTE_SIZE - 1):
                result.append(c)
                c = 0
            pos += 1
        return bytes(result)

    def permutate(self, table: List[int], block: List[int]) -> List[int]:
        """Perform a permutation operation on a block of bits using the specified table.

        Args:
            table (List[int]): The permutation table to be used.
            block (List[int]): The block of bits to be permuted.

        Returns:
            List[int]: The permuted block of bits.
        """
        return [block[x] for x in table]

    def create_sub_keys(self) -> None:
        """Create 16 subkeys using the key."""
        key = self.permutate(DES.Blocks.pc1, self.string_to_bitlist(self.key))
        self.L, self.R = key[:DES.HALF_KEY_SIZE], key[DES.HALF_KEY_SIZE:]
        for i in range(16):
            for _ in range(DES.Blocks.left_rotations[i]):
                self.L.append(self.L.pop(0))
                self.R.append(self.R.pop(0))
            self.Kn[i] = self.permutate(DES.Blocks.pc2, self.L + self.R)

    def descrypt(self, block: List[int], crypt_type: int) -> List[int]:
        """Perform the DES encryption or decryption on a block of bits.

        Args:
            block (List[int]): The block of bits to be encrypted or decrypted.
            crypt_type (int): The type of operation (DES.ENCRYPT or DES.DECRYPT).

        Returns:
            List[int]: The encrypted or decrypted block of bits.
        """
        block = self.permutate(DES.Blocks.initial_permutation, block)
        self.L, self.R = block[:DES.KEY_COMBINED_SIZE], block[DES.KEY_COMBINED_SIZE:]
        iteration = 0 if crypt_type == DES.ENCRYPT else 15
        iteration_adjustment = 1 if crypt_type == DES.ENCRYPT else -1
        for _ in range(16):
            tempR = self.R[:]
            self.R = self.permutate(DES.Blocks.expansion_table, self.R)
            self.R = [a ^ b for a, b in zip(self.R, self.Kn[iteration])]
            B = [self.R[i:i + DES.S_BOX_INPUT_SIZE] for i in range(0, DES.FULL_BLOCK_SIZE, DES.S_BOX_INPUT_SIZE)]
            Bn = [0] * DES.KEY_COMBINED_SIZE
            for j in range(8):
                m, n = (B[j][0] << 1) + B[j][5], (B[j][1] << 3) + (B[j][2] << 2) + (B[j][3] << 1) + B[j][4]
                v = DES.Blocks.s_boxes[j][(m << 4) + n]
                Bn[j * DES.S_BOX_OUTPUT_SIZE:j * DES.S_BOX_OUTPUT_SIZE + DES.S_BOX_OUTPUT_SIZE] = [(v & 8) >> 3, (v & 4) >> 2, (v & 2) >> 1, v & 1]

            self.R = self.permutate(DES.Blocks.straight_permutation, Bn)
            self.R = [a ^ b for a, b in zip(self.R, self.L)]
            self.L = tempR
            iteration += iteration_adjustment

        self.final = self.permutate(DES.Blocks.initial_permutation_reversed, self.R + self.L)
        return self.final

    def crypt(self, data: bytes, crypt_type: int) -> bytes:
        """Encrypt or decrypt data using the DES algorithm and the selected mode of operation.

        Args:
            data (bytes): The data to be encrypted or decrypted.
            crypt_type (int): The type of operation (DES.ENCRYPT or DES.DECRYPT).

        Returns:
            bytes: The encrypted or decrypted data.
        """
        if not data:
            return b''
        if len(data) % DES.BLOCK_SIZE != 0:
            if crypt_type == DES.DECRYPT:
                raise ValueError(f"Invalid data length, data must be a multiple of {DES.BLOCK_SIZE} bytes.")
            else:
                data += bytes([self.padding] * (DES.BLOCK_SIZE - (len(data) % DES.BLOCK_SIZE)))

        iv = self.string_to_bitlist(self.iv)

        result = []
        for i in range(0, len(data), DES.BLOCK_SIZE):
            block = self.string_to_bitlist(data[i:i + DES.BLOCK_SIZE])

            if crypt_type == DES.ENCRYPT:
                block = [a ^ b for a, b in zip(block, iv)]

            processed_block = self.descrypt(block, crypt_type)

            if crypt_type == DES.DECRYPT:
                processed_block = [a ^ b for a, b in zip(processed_block, iv)]
                iv = block
            else:
                iv = processed_block

            result.append(self.bitlist_to_string(processed_block))

        return b''.join(result)

    def encrypt(self, data: Union[str, bytes]) -> bytes:
        """Encrypt a block of data with the DES algorithm.

        Args:
            block (bytes): The 8-byte block of data to be encrypted.

        Returns:
            bytes: The 8-byte encrypted block of data.
        """
        data = self.ensure_ascii_encoded(data)
        data = self.pad_data(data)
        return self.crypt(data, DES.ENCRYPT)

    def decrypt(self, data: Union[str, bytes]) -> bytes:
        """Decrypt a block of data with the DES algorithm.

        Args:
            block (bytes): The 8-byte encrypted block of data to be decrypted.

        Returns:
            bytes: The 8-byte decrypted block of data.
        """
        data = self.ensure_ascii_encoded(data)
        data = self.crypt(data, DES.DECRYPT)
        return self.unpad_data(data)
    
def main():
    """Main function."""
    data = b'HELLO, THIS IS A MESSAGE'
    k = DES(key=b'BETHEKEY')
    d = k.encrypt(data)
    print(f'Plaintext: {data}')
    print(f'Ciphertext: {d}')
    print(f'Decrypted text: {k.decrypt(d)}')

if __name__ == "__main__":
    main()
