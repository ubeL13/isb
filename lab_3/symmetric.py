import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Symmetric:
    """
    Class for symmetrical encryption and decryption using the Camellia algorithm.
    """

    def create_key(self, bits: int) -> bytes:
        """
        Generates a random symmetric key of a specified bit length.
        The key is generated using the operating system's source of randomness, which is suitable for cryptographic use.
        :param bits: the bit length for the symmetric key. This value should be a multiple of 8.
        :return: A bytes object containing the symmetric key.
        """
        try:
            return os.urandom(bits // 8)
        except Exception as e:
            print(f"An error occurred during key generation: {e}")
            raise

    def encrypt_text_symmetric(self, plain_data: bytes, key: bytes, bits: int) -> bytes:
        """
        Encrypts plaintext data using the Camellia encryption algorithm in CBC mode.
        Parameters:
        plain_data: The plaintext data to be encrypted, provided as a bytes object.
        key: The symmetric key for encryption, also provided as a bytes object.
        bits: The bit strength of the encryption key. Must be one of 128, 192, or 256.
        Returns:
        A bytes object containing the IV followed by the encrypted data.
        """
        try:
            if bits not in (128, 192, 256):
                raise ValueError("Invalid key size. Choose 128, 192, or 256 bits.")
            data_padder = padding.PKCS7(128).padder()
            padded_data = data_padder.update(plain_data) + data_padder.finalize()

            iv_value = os.urandom(16)
            camellia_cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv_value))
            encryptor_instance = camellia_cipher.encryptor()
            cipher_data = encryptor_instance.update(padded_data) + encryptor_instance.finalize()

            return iv_value + cipher_data
        except Exception as e:
            print(f"An error occurred during encryption: {e}")
            raise

    def decrypt_text_symmetrict(self, cipher_data: bytes, key: bytes, bits: int) -> str:
        """
        Decrypts data that has been encrypted using the Camellia encryption algorithm in CBC mode.
        plain_data: The plaintext data to be encrypted, provided as a bytes object.
        key: The symmetric key for encryption, also provided as a bytes object.
        bits: The bit strength of the encryption key. Must be one of 128, 192, or 256.
        Returns:
        A bytes object containing the IV followed by the encrypted data.
        """
        try:
            iv_value = cipher_data[:16]
            cipher_data = cipher_data[16:]

            camellia_cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv_value))
            decryptor_instance = camellia_cipher.decryptor()
            decrypted_data = decryptor_instance.update(cipher_data) + decryptor_instance.finalize()

            data_unpadder = padding.PKCS7(128).unpadder()
            decrypted_padded_data = data_unpadder.update(decrypted_data) + data_unpadder.finalize()

            return decrypted_padded_data.decode('utf-8')
        except Exception as e:
            print(f"An error occurred during decryption: {e}")
            raise
