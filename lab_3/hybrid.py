from asymmetric import Asymmetric
from symmetric import Symmetric
from serialization_deserialization import load_text, write_text, write_text_str, load_symmetric_key, \
    write_symmetric_key, write_asymmetric_keys


class Mixed:
    """
    Class for handling encryption and decryption using a combination of symmetric and asymmetric key algorithms.
    """

    def __init__(self, bits: int):
        """
        Initialize the Mixed object with symmetric and asymmetric encryption components.
        Args:
        number_of_bits (int): The number of bits to use for the symmetric key.
        """
        self.symmetric = Symmetric()
        self.asymmetric = Asymmetric()
        self.number_of_bits = bits

    def generate_keys(self, path_to_symmetric_key: str, path_to_public_key: str, path_to_private_key: str) -> None:
        """
        Generate and store asymmetric keys and an encrypted symmetric key.
        Args:
        path_to_symmetric_key (str): The file path where the encrypted symmetric key will be saved.
        path_to_public_key (str): The file path where the public key will be saved.
        path_to_private_key (str): The file path where the private key will be saved.
        Raises:
        Exception: If an error occurs during the key generation or file writing processes.
        """
        try:
            symmetric_key = self.symmetric.create_key(self.number_of_bits)
            keys = self.asymmetric.create_keys()
            write_asymmetric_keys(path_to_private_key, path_to_public_key, keys[0], keys[1])
            write_symmetric_key(path_to_symmetric_key, self.asymmetric.encrypt_text_asymmetric(symmetric_key, keys[1]))
        except Exception as e:
            print(f"An error occurred during key generation: {e}")

    def encrypt(self, path_to_text_for_encryption: str, path_to_symmetric_key: str, path_to_private_key: str,
                path_to_save_encrypted_text: str) -> None:
        """
        Encrypts a plaintext file using a symmetric key that is itself encrypted with an asymmetric algorithm.
        Args:
        path_to_text_for_encryption (str): The file path to the plaintext that needs to be encrypted.
        path_to_symmetric_key (str): The file path to the encrypted symmetric key.
        path_to_private_key (str): The file path to the private key used to decrypt the symmetric key.
        path_to_save_encrypted_text (str): The file path where the encrypted text will be saved.
        Raises:
         Exception: If any errors occur during the encryption process.
        """
        try:
            encrypted_symmetric_key = load_symmetric_key(path_to_symmetric_key)
            decrypted_symmetric_key = self.asymmetric.decrypt_text_asymmetric(path_to_private_key,
                                                                              encrypted_symmetric_key)
            text = load_text(path_to_text_for_encryption)
            write_text(path_to_save_encrypted_text, self.symmetric.encrypt_text_symmetric(text, decrypted_symmetric_key,
                                                                                          self.number_of_bits))
        except Exception as e:
            print(f"An error occurred during encryption: {e}")

    def decrypt(self, path_to_encrypted_text: str, path_to_symmetric_key: str, path_to_private_key: str,
                path_to_save_decrypted_text: str) -> None:
        """
        Decrypts an encrypted text file using a symmetric key that has been decrypted with an asymmetric algorithm.
        Args:
        path_to_encrypted_text (str): The file path to the encrypted text that needs to be decrypted.
        path_to_symmetric_key (str): The file path to the encrypted symmetric key.
        path_to_private_key (str): The file path to the private key used to decrypt the symmetric key.
        path_to_save_decrypted_text (str): The file path where the decrypted text will be saved.
        Raises:
        Exception: If any errors occur during the decryption process.
        """
        try:
            encrypted_symmetric_key = load_symmetric_key(path_to_symmetric_key)
            decrypted_symmetric_key = self.asymmetric.decrypt_text_asymmetric(path_to_private_key,
                                                                              encrypted_symmetric_key)
            encrypted_text = load_text(path_to_encrypted_text)
            write_text_str(path_to_save_decrypted_text,
                           self.symmetric.decrypt_text_symmetrict(encrypted_text, decrypted_symmetric_key,
                                                                  self.number_of_bits))
        except Exception as e:
            print(f"An error occurred during decryption: {e}")
