import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class SymmetricCryptography:
    """
    Initializes the SymmetricCryptography class.
    Args:
    key_path (str): The path to the key file.
    """
    def generate_key(self, size: int) -> bytes:
        """
        Generates a random key of the specified size.
        Args:
        size (int): The size of the key in bytes.
        Returns:
        bytes: The generated key.
        """
        try:
            key = os.urandom(size)
            return key
        except Exception as e:
            print(f"An error occurred while generating the key: {e}")
            return b''

    def encryption(self, plaintext: bytes, secret_key: bytes, block_size: int)-> bytes:
        """
        Encrypt plaintext using Camellia algorithm with CBC mode.
        Args:
        plaintext (bytes): Data to be encrypted.
        Returns:
        bytes: Encrypted data with prepended IV.
        """
        try:
            iv = os.urandom(algorithms.Camellia.block_size // 8)
            padder = padding.PKCS7(block_size).padder()
            padded_plaintext = padder.update(plaintext) + padder.finalize()
            cipher = Cipher(algorithms.Camellia(secret_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_plaintext) + encryptor.finalize()
            return iv + encrypted_data
        except Exception as e:
            print(f"An error occurred while encrypting the data: {e}")
            return b''

    def decryption(self, encrypted_blob: bytes, secret_key: bytes, block_size: int) -> str:
        """
        Encrypts the plaintext using the Camellia algorithm with CBC mode.
        Args:
        plaintext (bytes): The data to be encrypted.
        secret_key (bytes): The secret key used for encryption.
        block_size (int): The block size for padding.
        Returns:
        bytes: The encrypted data with prepended IV.
        """
        try:
            iv, cipher_text = encrypted_blob[:16], encrypted_blob[16:]
            decryption_cipher = Cipher(algorithms.Camellia(secret_key), modes.CBC(iv))
            decryptor = decryption_cipher.decryptor()
            decrypted_padded_data = decryptor.update(cipher_text) + decryptor.finalize()
            depadder = padding.PKCS7(block_size).unpadder()
            clean_data = (depadder.update(decrypted_padded_data) + depadder.finalize()).decode('utf-8')
            return clean_data
        except Exception as e:
            print(f"An error occurred while decrypting the data: {e}")

