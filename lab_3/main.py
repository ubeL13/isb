import os
import json
import logging
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

logging.basicConfig(level=logging.INFO)


class SymmetricCryptography:
    def __init__(self, key_path: str) -> None:
        self.key_path = key_path

    def generate_key(self, size: int) -> bytes:
        key = os.urandom(size)
        return key


class AsymmetricCryptography:
    def __init__(self, private_key_path: str, public_key_path: str) -> None:
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path

    def generate_key(self, size: int) -> tuple:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key


def main():
    with open("paths.json") as paths_file:
        paths = json.load(paths_file)

    folder = paths["folder"]
    encrypted_file = os.path.join(paths["encrypted_file"])
    decrypted_file = os.path.join(paths["decrypted_file"])
    symmetric_key = os.path.join(paths["symmetric_key"])
    public_path = os.path.join(paths["public_path"])
    private_path = os.path.join(paths["private_path"])

    symmetric_crypto = SymmetricCryptography(symmetric_key)
    symmetric_key_data = symmetric_crypto.generate_key(32)

    with open(symmetric_key, "wb") as key_file:
        key_file.write(symmetric_key_data)

    asymmetric_crypto = AsymmetricCryptography(private_path, public_path)
    private_key, public_key = asymmetric_crypto.generate_key(2048)

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(private_path, "wb") as private_file:
        private_file.write(private_pem)

    with open(public_path, "wb") as public_file:
        public_file.write(public_pem)

    logging.info(f"Symmetric key saved to: {symmetric_key}")
    logging.info(f"Private key saved to: {private_path}")
    logging.info(f"Public key saved to: {public_path}")


if __name__ == "__main__":
    main()
