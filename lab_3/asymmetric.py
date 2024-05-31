from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from serialization_deserialization import deserialize_private


class AsymmetricEncryptionHandler:

    def generate_key(self, size: int) -> tuple:
        """Generates an RSA private and public key pair.

        Args:
            size (int): The size of the key.

        Returns:
            tuple: A tuple containing the private key and public key.
        """
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=size)
        public_key = private_key.public_key()
        return private_key, public_key

    def encryption(self, plain_data: bytes, rsa_public_key: rsa.RSAPublicKey)-> bytes:
        """Encrypts the provided data using the RSA public key.

        Args:
            plain_data (bytes): The data to be encrypted.
            rsa_public_key: The public key object for RSA encryption.

        Returns:
            bytes: The encrypted data.
        """
        try:
            oaep_padding = padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
            encrypted_data = rsa_public_key.encrypt(plain_data, oaep_padding)
            return encrypted_data
        except Exception as e:
            print(f"An error occurred in encryption: {e}")
            raise

    def decrypt_text(self, path_to_private_key: str, encrypted_text: bytes) -> bytes:
        """Decrypts the encrypted text using the private key.

        Args:
            path_to_private_key (str): The path to the private key file.
            encrypted_text (bytes): The text to be decrypted.

        Returns:
            bytes: The decrypted text.
        """
        try:
            private_key = deserialize_private(path_to_private_key)
            decrypted_text = private_key.decrypt(
                encrypted_text,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted_text
        except Exception as e:
            print(f"An error occurred in decrypt_text: {e}")
            raise
