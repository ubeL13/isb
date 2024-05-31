import json

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


def load_key(path: str, file_mode: str, func, *args) ->any:
    """
    Load and return a key from a file.

    Parameters:
    path (str): The path to the file containing the key.
    file_mode (str): The mode in which to open the file. 'rb' for keys, 'r' for text.
    func: The function to apply to the file content.
    *args: The arguments to pass to func.
    Returns:
    The result of applying func to the file content.
    """
    try:
        with open(path, file_mode) as file:
            return func(file.read(), *args)
    except FileNotFoundError:
        print("File not founded.")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise


def deserialize_private(path_to_private_key: str) -> rsa.RSAPrivateKey:
    """
    Load and return a private RSA key from a file.
    Parameters:
    path_to_private_key (str): The path to the file containing the private key.
    Returns:
    rsa.RSAPrivateKey: The private RSA key.
    """
    return load_key(path_to_private_key, 'rb', load_pem_private_key, None)


def deserialize_public(path_to_public_key: str) -> rsa.RSAPublicKey:
    """
    Load and return a public RSA key from a file.
    Parameters:
    path_to_public_key (str): The path to the file containing the public key.
    Returns:
    rsa.RSAPublicKey: The public RSA key.
    """
    return load_key(path_to_public_key, 'rb', load_pem_public_key)


def write_key(path: str, file_mode: str, key, func, **kwargs):
    """
    Write a key to a file.

    Parameters:
    path (str): The path to the file where the key will be written.
    file_mode (str): The mode in which to open the file. 'wb' for binary files, 'w' for text files.
    key: The key to write to the file.
    func: The method of the key object to serialize the key.
    **kwargs: Additional keyword arguments to pass to func.
    """
    try:
        with open(path, file_mode) as file:
            file.write(func(**kwargs))
    except FileNotFoundError:
        print("File not found")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

# Исправляем вызовы функций serialize_private и serialize_public:
def serialize_private(path_to_private_key: str, private_key: rsa.RSAPrivateKey) -> None:
    return write_key(path_to_private_key, 'wb', private_key, private_key.private_bytes,
                     encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL,
                     encryption_algorithm=serialization.NoEncryption())

def serialize_public(path_to_public_key: str, public_key: rsa.RSAPublicKey) -> None:
    return write_key(path_to_public_key, 'wb', public_key, public_key.public_bytes,
                     encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
def serialize_asymmetric_keys(path_to_private_key: str, path_to_public_key: str, private_key: rsa.RSAPrivateKey,
                              public_key: rsa.RSAPublicKey) -> None:
    """
    Serialize and write both private and public RSA keys to their respective files.
    Parameters:
    path_to_private_key (str): The path to the file where the private key will be written.
    path_to_public_key (str): The path to the file where the public key will be written.
    private_key: The private RSA key to serialize.
    public_key: The public RSA key to serialize.
    Returns:
    None
    """
    serialize_private(path_to_private_key, private_key)
    serialize_public(path_to_public_key, public_key)


def serialize_symmetric_key(path_to_symmetric_key: str, symmetric_key: bytes) -> None:
    """
    Serialize and write a symmetric key to a file.
    Parameters:
    path_to_symmetric_key (str): The path to the file where the symmetric key will be written.
    symmetric_key (bytes): The symmetric key to serialize.
    Returns:
    None
    """
    write_key(path_to_symmetric_key, 'wb', symmetric_key, lambda x, *args: x)


def deserialize_symmetric_key(path_to_symmetric_key: str) -> bytes:
    """
    Load and return a symmetric key from a file.
    Parameters:
    path_to_symmetric_key (str): The path to the file containing the symmetric key.
    Returns:
    bytes: The deserialized symmetric key.
    """
    return load_key(path_to_symmetric_key, 'rb', lambda x, *args: x)


def save_text(file_name: str, text: bytes)-> None:
    """
    Save binary text to a file.
    Parameters:
    file_name (str): The name of the file where the text will be saved.
    text (bytes): The binary text to save.
    Returns:
    None
    """
    write_key(file_name, 'wb', text, lambda x, *args: x)


def save_text_str(file_name: str, text: str)-> None:
    """
    Save text to a file in text format.
    Parameters:
    file_name (str): The name of the file where the text will be saved.
    text (str): The text to save.
    Returns:
    None
    """
    write_key(file_name, 'w', text, lambda x, *args: x)


def read_text(file_name: str)-> bytes:
    """
    Read binary text from a file.
    Parameters:
    file_name (str): The name of the file to read from.
    Returns:
    bytes: The binary text read from the file.
    """
    return load_key(file_name, 'rb', lambda x, *args: x)


def read_json_file(file_path: str) -> dict:
    """
    Read a JSON file and return the data as a dictionary.
    Parameters:
    file_path (str): The path to the JSON file.
    Returns:
    dict: The data from the JSON file.
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        print("File not founded.")
        raise
    except json.JSONDecodeError:
        print("Error while reading json file.")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise
