from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes

from serialization_deserialization import load_private_key


class Asymmetric:
    def create_keys(self) -> tuple:
        """
        Generate a private and public RSA key pair.
        Returns:
        tuple: A tuple containing the RSA private key and public key objects.
        """
        private_key_obj = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        rsa_private_key = private_key_obj
        rsa_public_key = private_key_obj.public_key()
        return rsa_private_key, rsa_public_key

    def encrypt_text_asymmetric(self, data: bytes, pub_key: rsa.RSAPublicKey) -> bytes:
        """
        Encrypt data using the RSA public key.
        Args:
        data (bytes): The plaintext data to encrypt.
        pub_key (RSAPublicKey): The RSA public key for encryption.
        Returns:
        bytes: The encrypted data.
        """
        try:
            oaep_padding = asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
            encrypted_data = pub_key.encrypt(data, oaep_padding)
            return encrypted_data
        except Exception as e:
            print(f"Encryption failed with error: {e}")
            raise

    def decrypt_text_asymmetric(self, private_key_filepath: str, encrypted_data: bytes) -> bytes:
        """
        Decrypt data using the RSA private key.
        Args:
        private_key_filepath (str): The file path to the serialized private key.
        encrypted_data (bytes): The encrypted data to decrypt.
        Returns:
        bytes: The decrypted data.
        """
        try:
            rsa_private_key = load_private_key(private_key_filepath)
            oaep_padding = asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
            decrypted_data = rsa_private_key.decrypt(encrypted_data, oaep_padding)
            return decrypted_data
        except Exception as e:
            print(f"Decryption failed with error: {e}")
            raise
