from asymmetric import AsymmetricEncryptionHandler
from symmetric import SymmetricCryptography
from serialization_deserialization import read_text, save_text, save_text_str, deserialize_symmetric_key, \
    serialize_symmetric_key, serialize_asymmetric_keys


class Hybrid:
    """
    Class for Cryptosystem:
    @methods:
        __init__:
        generate_keys:
        encrypt:
        decrypt:

    """

    def __init__(self, number_of_bits: int):

        self.symmetric = SymmetricCryptography()
        self.asymmetric = AsymmetricEncryptionHandler()
        self.number_of_bits = number_of_bits

    def generate_keys(self, path_to_symmetric_key: str, path_to_public_key: str, path_to_private_key: str) -> None:

        symmetric_key = self.symmetric.generate_key(self.number_of_bits)
        keys = self.asymmetric.generate_key(self.number_of_bits)
        serialize_asymmetric_keys(path_to_private_key, path_to_public_key, keys[0], keys[1])
        symmetric_key_encrypted = self.asymmetric.encryption(symmetric_key, keys[1])
        serialize_symmetric_key(path_to_symmetric_key, symmetric_key_encrypted)

    def encrypt(self, path_to_text_for_encryption: str, path_to_symmetric_key: str, path_to_private_key: str,
                path_to_save_encrypted_text: str) -> None:

        encrypted_symmetric_key = deserialize_symmetric_key(path_to_symmetric_key)
        decrypted_symmetric_key = self.asymmetric.decrypt_text(path_to_private_key, encrypted_symmetric_key)
        text = read_text(path_to_text_for_encryption)
        encrypted_text = self.symmetric.encryption(text, decrypted_symmetric_key, self.number_of_bits)
        save_text(path_to_save_encrypted_text, encrypted_text)

    def decrypt(self, path_to_encrypted_text: str, path_to_symmetric_key: str, path_to_private_key: str,
                path_to_save_decrypted_text: str) -> None:

        encrypted_symmetric_key = deserialize_symmetric_key(path_to_symmetric_key)
        decrypted_symmetric_key = self.asymmetric.decrypt_text(path_to_private_key, encrypted_symmetric_key)
        encrypted_text = read_text(path_to_encrypted_text)
        decrypted_text = self.symmetric.decryption(encrypted_text, decrypted_symmetric_key, self.number_of_bits)
        save_text_str(path_to_save_decrypted_text, decrypted_text)
