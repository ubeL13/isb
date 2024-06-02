import json

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


class CryptoFileManager:
    def load_private_key(self, file_path: str) -> rsa.RSAPrivateKey:
        """
        Load an RSA private key from a PEM file.
        :param file_path: Path to the PEM file containing the private key.
        :return: An RSAPrivateKey object.
        """
        try:
            with open(file_path, 'rb') as file:
                private_key_data = file.read()
            private_key = load_pem_private_key(private_key_data, password=None)
            return private_key
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
            raise
        except ValueError:
            print("The private key could not be deserialized.")
            raise

    def load_public_key(self, file_path: str) -> rsa.RSAPublicKey:
        """
        Load an RSA public key from a PEM file.
        :param file_path: Path to the PEM file containing the public key.
        :return: An RSAPublicKey object.
        """
        try:
            with open(file_path, 'rb') as file:
                public_key_data = file.read()
            public_key = load_pem_public_key(public_key_data)
            return public_key
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
            raise
        except ValueError:
            print("The public key could not be deserialized.")
            raise

    def load_symmetric_key(self, file_path: str) -> bytes:
        """
        Load a symmetric key from a file.
        :param file_path: Path to the file containing the symmetric key.
        :return: The symmetric key.
        """
        try:
            with open(file_path, 'rb') as file:
                key = file.read()
            return key
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
            raise
        except IOError as e:
            print(f"An I/O error occurred while reading from {file_path}: {e}")
            raise

    def write_private_key(self, file_path: str, key: rsa.RSAPrivateKey) -> None:
        """
        Write an RSA private key to a PEM file.
        :param file_path: Path where the PEM file will be saved.
        :param key: An RSAPrivateKey object to serialize.
        """
        try:
            private_key_pem = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(file_path, 'wb') as file:
                file.write(private_key_pem)
        except IOError as e:
            print(f"An I/O error occurred: {e}")
            raise

    def write_public_key(self, file_path: str, key: rsa.RSAPublicKey) -> None:
        """
        Write an RSA public key to a PEM file.
        :param file_path: Path where the PEM file will be saved.
        :param key: An RSAPublicKey object to serialize.
        """
        try:
            public_key_pem = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            with open(file_path, 'wb') as file:
                file.write(public_key_pem)
        except IOError as e:
            print(f"An I/O error occurred: {e}")
            raise

    def write_asymmetric_keys(self, private_key_path: str, public_key_path: str, private_key: rsa.RSAPrivateKey,
                              public_key: rsa.RSAPublicKey) -> None:
        """
        Write both RSA private and public keys to their respective PEM files.
        :param private_key_path: Path to save the private key PEM file.
        :param public_key_path: Path to save the public key PEM file.
        :param private_key: An RSAPrivateKey object to serialize.
        :param public_key: An RSAPublicKey object to serialize.
        """

        self.write_private_key(private_key_path, private_key)
        self.write_public_key(public_key_path, public_key)

    def write_symmetric_key(self, file_path: str, key: bytes) -> None:
        """
        Write a symmetric key to a file.
        :param file_path: Path where the file will be saved.
        :param key: The symmetric key to write.
        """
        try:
            with open(file_path, 'wb') as file:
                file.write(key)
        except IOError as e:
            print(f"An I/O error occurred while writing to {file_path}: {e}")
            raise

    def write_text(self, file_name: str, text: bytes) -> None:
        """
        Write binary text to a file.
        :param file_name: The name of the file to write to.
        :param text: The binary text to write.
        """
        try:
            with open(file_name, 'wb') as file:
                file.write(text)
        except IOError as e:
            print(f"An I/O error occurred while writing to {file_name}: {e}")
            raise

    def write_text_str(self, file_name: str, text: str) -> None:
        """
        Write string text to a file.
        :param file_name: The name of the file to write to.
        :param text: The string text to write.
        """
        try:
            with open(file_name, 'w') as file:
                file.write(text)
        except IOError as e:
            print(f"An I/O error occurred while writing to {file_name}: {e}")
            raise

    def load_text(self, file_name: str) -> bytes:
        """
        Load binary text from a file.
        :param file_name: The name of the file to read from.
        :return: The binary text.
        """
        try:
            with open(file_name, 'rb') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"The file {file_name} was not found.")
            raise
        except IOError as e:
            print(f"An I/O error occurred while reading from {file_name}: {e}")
            raise

    def load_json_file(self, file_path: str) -> dict:
        """
        Load a JSON object from a file.
        :param file_path: The path to the file.
        :return: The JSON object.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            return json_data
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
            raise
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_path}.")
            raise
        except IOError as e:
            print(f"An I/O error occurred while reading from {file_path}: {e}")
            raise
