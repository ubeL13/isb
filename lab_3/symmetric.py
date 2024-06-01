import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class Symmetric:
    """
    Class for symmetrical encryption and decryption using the Camellia algorithm.
    """
    def create_key(self, bits: int) -> bytes:
        return os.urandom(bits // 8)

    def encrypt_text_symmetric(self, plain_data: bytes, key: bytes, bits: int) -> bytes:
        try:
            if bits not in (128, 192, 256):
                raise ValueError("Invalid key size. Choose 128, 192, or 256 bits.")
            data_padder = padding.PKCS7(bits).padder()
            padded_data = data_padder.update(plain_data) + data_padder.finalize()

            iv_value = os.urandom(16)
            camellia_cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv_value))
            encryptor_instance = camellia_cipher.encryptor()
            cipher_data = encryptor_instance.update(padded_data) + encryptor_instance.finalize()

            return iv_value + cipher_data
        except Exception as e:
            print(f"An error occurred during encryption: {e}")
            raise e

    def decrypt_text_symmetrict(self, cipher_data: bytes, key: bytes, bits: int) -> str:
        try:
            iv_value = cipher_data[:16]
            cipher_data = cipher_data[16:]

            camellia_cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv_value))
            decryptor_instance = camellia_cipher.decryptor()
            decrypted_data = decryptor_instance.update(cipher_data) + decryptor_instance.finalize()

            data_unpadder = padding.PKCS7(bits).unpadder()
            decrypted_padded_data = data_unpadder.update(decrypted_data) + data_unpadder.finalize()

            return decrypted_padded_data.decode('utf-8')
        except Exception as e:
            print(f"An error occurred during decryption: {e}")
            raise e
