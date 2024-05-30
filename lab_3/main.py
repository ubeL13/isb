import os
import json
import logging
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import  hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logging.basicConfig(level=logging.INFO)




def main():
    # Загрузка путей из файла конфигурации
    with open("paths.json") as paths_file:
        paths = json.load(paths_file)

    # Пути для сериализации ключей
    symmetric_key_path = os.path.join(paths["symmetric_key"])
    public_key_path = os.path.join(paths["public_path"])
    private_key_path = os.path.join(paths["private_path"])

    # 1.1. Сгенерировать ключ для симметричного алгоритма
    symmetric_key = os.urandom(32)

    # 1.2. Сгенерировать ключи для асимметричного алгоритма
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # 1.3. Сериализовать асимметричные ключи
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # 1.4. Зашифровать ключ симметричного шифрования открытым ключом и сохранить по указанному пути
    oaep_padding = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
    encrypted_symmetric_key = public_key.encrypt(symmetric_key, oaep_padding)


    with open(private_key_path, "wb") as private_file:
        private_file.write(private_pem)
    logging.info(f"Private key saved to {private_key_path}")

    with open(public_key_path, "wb") as public_file:
        public_file.write(public_pem)
    logging.info(f"Public key saved to {public_key_path}")

    with open(symmetric_key_path, "wb") as encrypted_key_file:
        encrypted_key_file.write(encrypted_symmetric_key)
    logging.info(f"Encrypted symmetric key saved to {symmetric_key_path}")

    sym_crypto = SymmetricCryptography(paths['sym_path'])
    asym_handler = AsymmetricEncryptionHandler(paths['private_path'], paths['public_path'])
    with open(paths['text'], 'rb') as f:
        plaintext = f.read()

    encrypted_data = sym_crypto.encrypt_data(plaintext)

    with open(paths['encrypted_text'], 'wb') as f:
        f.write(encrypted_data)

    logging.info(f"Encrypted text saved to {paths['encrypted_text']}")

if __name__ == "__main__":
    main()