import json

from typing import Dict

from constants import PATHS
from decryption_frequency import KEY as known_frequencies
from decryption_key import KEY as key_for_decryption


def read_settings(settings_path: str) -> Dict:
    """
    Reads a JSON settings file.
    Args:
        settings_path: A string representing the path to the settings file.
    Returns:
        A dictionary containing the settings.
    """
    try:
        with open(settings_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Settings file not found: {error}")
    except json.JSONDecodeError as error:
        raise json.JSONDecodeError(f"Error decoding JSON: {error}")


def read_text(file_path: str) -> str:
    """
    Reads and returns the content of the specified text file.
    Args:
        file_path: The path to the text file to be read.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Text file not found: {error}")
    except IOError as error:
        raise IOError(f"Error reading text file: {error}")


def frequency_analysis(text: str) -> Dict:
    """
    Analyzes the frequency of letters in a text.
    Args:
        text: A string representing the text to analyze.
    Returns:
        A dictionary where keys represent letters and values their frequency in the text.
    """
    dictionary_of_frequency = {}
    len_text = len(text)
    for letter in text:
        if letter not in dictionary_of_frequency:
            dictionary_of_frequency[letter] = text.count(letter) / len_text
    return dictionary_of_frequency


def create_decryption_key(encrypted_frequencies: Dict, known_frequencies: Dict) -> Dict:
    """
    Creates a decryption key.
    Args:
        encrypted_frequencies: A dictionary representing the frequency of encrypted letters.
        known_frequencies: A dictionary representing the frequency of known letters.
    Returns:
        A dictionary serving as a decryption key, tying encrypted letters to their substitutes.
    """
    sorted_encrypted = sorted(encrypted_frequencies.items(), key=lambda item: item[1], reverse=True)
    sorted_known = sorted(known_frequencies.items(), key=lambda item: item[1], reverse=True)
    return {encrypted_char: known_char for (encrypted_char, _), (known_char, _) in zip(sorted_encrypted, sorted_known)}


def write_decryption_key_to_file(key: Dict, file_path: str):
    """
    This function creates a file at a specified path with
    a representation of the decryption key.
    :param key: A dictionary representing the decryption key.
    :param file_path: The file path where the key should be written.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"KEY = {json.dumps(key, ensure_ascii=False, indent=4)}")
    except IOError as error:
        raise IOError(f"Error writing to key file: {error}")


def decrypt_text(encrypted_text: str, decryption_key: Dict) -> str:
    """
    Decrypts a text using a decryption key.
    Args:
        encrypted_text: The text to decrypt.
        decryption_key: The key to use for decryption.
    Returns:
        The decrypted text.
    """
    return ''.join(decryption_key.get(char, char) for char in encrypted_text)


if __name__ == "__main__":
    try:
        paths = read_settings(PATHS)
        folder = paths['folder']
        source_file_path = f"{folder}/{paths['source_file']}"
        output_file_decrypted_path = f"{folder}/{paths['output_file_decrypted']}"
        key_path = 'decryption_key.py'

        encrypted_text = read_text(source_file_path)
        encrypted_frequencies = frequency_analysis(encrypted_text)

        if len(key_for_decryption) == 0:
            decryption_key = create_decryption_key(encrypted_frequencies, known_frequencies)
            write_decryption_key_to_file(decryption_key, key_path)
        else:
            decryption_key = key_for_decryption

        decrypted_text = decrypt_text(encrypted_text, decryption_key)
        with open(output_file_decrypted_path, 'w', encoding='utf-8') as file:
            file.write(decrypted_text)
    except (FileNotFoundError, IOError) as error:
        print(f"File error: {error}")
    except json.JSONDecodeError as error:
        print(f"Error decoding JSON: {error}")
