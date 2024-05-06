import json
import os
from typing import Dict

from constants import PATHS
from decryption_frequency import KEY as known_frequencies
from decryption_key import KEY as decryption_key


def read_settings(settings_path: str) -> Dict:
    """Reads a JSON settings file.
    Args:
        settings_path: A string representing the path to the settings file.
    Returns:
        A dictionary containing the settings.
    """
    with open(settings_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def frequency_analysis(text: str) -> Dict:
    """Analyzes the frequency of letters in a text.
    Args:
        text: A string representing the text to analyze.
    Returns:
        A dictionary where keys represent letters and values their frequency in the text.
    """
    dictionary_of_frequency = {}
    len_text = len(text)
    for letter in text:
        if letter not in dictionary_of_frequency:
            frequency = text.count(letter) / len_text
            dictionary_of_frequency[letter] = frequency
    return dictionary_of_frequency


def create_decryption_key(encrypted_frequencies: Dict, known_frequencies: Dict) -> Dict:
    """Creates a decryption key.
    Args:
        encrypted_frequencies: A dictionary representing the frequency of encrypted letters.
        known_frequencies: A dictionary representing the frequency of known letters.
    Returns:
        A dictionary serving as a decryption key, tying encrypted letters to their substitutes.
    """
    sorted_encrypted = sorted(encrypted_frequencies.items(), key=lambda item: item[1], reverse=True)
    sorted_known = sorted(known_frequencies.items(), key=lambda item: item[1], reverse=True)
    return {encrypted_char: known_char for (encrypted_char, _), (known_char, _) in zip(sorted_encrypted, sorted_known)}


def decrypt_text(encrypted_text: str, decryption_key: Dict) -> str:
    """Decrypts a text using a decryption key.

    Args:
        encrypted_text: The text to decrypt.
        decryption_key: The key to use for decryption.

    Returns:
        The decrypted text.
    """
    return ''.join(decryption_key.get(char, char) for char in encrypted_text)


if __name__ == "__main__":
    paths = read_settings(PATHS)
    folder = paths['folder']
    source_file_path = f"{folder}/{paths['source_file']}"
    output_file_decrypted_path = f"{folder}/{paths['output_file_decrypted']}"
    key_path = 'decryption_key.py'

    if not os.path.isfile(key_path) or os.stat(key_path).st_size == 0:
        with open(source_file_path, 'r', encoding='utf-8') as file:
            encrypted_text = file.read()
        encrypted_frequencies = frequency_analysis(encrypted_text)
        decryption_key = create_decryption_key(encrypted_frequencies, known_frequencies)
        with open(key_path, 'w', encoding='utf-8') as file:
            file.write(f"KEY = {json.dumps(decryption_key, ensure_ascii=False, indent=4)}")

    with open(source_file_path, 'r', encoding='utf-8') as file:
        encrypted_text = file.read()
    decrypted_text = decrypt_text(encrypted_text, decryption_key)
    with open(output_file_decrypted_path, 'w', encoding='utf-8') as file:
        file.write(decrypted_text)
