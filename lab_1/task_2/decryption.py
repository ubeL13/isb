import json
from typing import Dict


# Функция для чтения настроек из файла
def read_settings(settings_path):
    with open(settings_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Функция для выполнения частотного анализа текста и сохранения результатов в файл
# def frequency_analysis(text):
#     dictionary_of_frequency = {}
#     text = text.replace(' ', '').replace('n', '')  # Удаление пробелов и переносов строк
#     len_text = len(text)
#     for letter in text:
#         if letter not in dictionary_of_frequency:
#             frequency = text.count(letter) / len_text
#             dictionary_of_frequency[letter] = frequency
#     # Создание и сохранение частот в новый файл
#     with open('descryption_key.py', 'w', encoding='utf-8') as file:
#         json.dump(dictionary_of_frequency, file, ensure_ascii=False, indent=4)
#     return dictionary_of_frequency
#
#
# # Функция для сортировки словаря по значениям в убывающем порядке
# def sort_dict_values(dictionary: Dict[str, float]):
#     return sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
#
#
# # Функция для создания ключа дешифровки
# def create_decryption_key(encrypted_frequencies: Dict[str, float], known_frequencies: Dict[str, float]) -> Dict[
#     str, str]:
#     sorted_encrypted = sort_dict_values(encrypted_frequencies)
#     sorted_known = sort_dict_values(known_frequencies)
#
#     return {encrypted_char: known_char for (encrypted_char, _), (known_char, _) in zip(sorted_encrypted, sorted_known)}
from typing import Dict, List


def frequency_analysis(text: str) -> Dict[str, float]:
    """
    Анализирует частоту появления каждой буквы в тексте.

    Параметры:
        - text (str): Текст для анализа.

    Возвращает:
        - dict: Словарь, содержащий частоту каждой буквы в тексте.
    """
    size = len(text)
    frequency: Dict[str, float] = {}
    for letter in set(text):
        frequency[letter] = text.count(letter) / size
    return frequency


def sort_dict_by_values(dictionary: Dict[str, float], reverse: bool = True) -> Dict[str, float]:
    """
    Сортирует словарь по его значениям.

    Параметры:
        - dictionary (dict): Словарь, который необходимо отсортировать.
        - reverse (bool): Определяет порядок сортировки (по умолчанию убывание).

    Возвращает:
        - dict: Отсортированный словарь на основе значений.
    """
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=reverse))


def create_decryption_key(encrypted_frequencies: Dict[str, float], known_frequencies: Dict[str, float]) -> Dict[
    str, str]:
    """
    Создает ключ для дешифрования, сопоставляя зашифрованные символы с известной частотой букв.

    Параметры:
        - encrypted_frequencies (dict): Словарь частот символов зашифрованного текста.
        - known_frequencies (dict): Словарь известных частот символов алфавита.

    Возвращает:
        - dict: Словарь ключей для дешифрования.
    """
    sorted_encrypted = sort_dict_by_values(encrypted_frequencies)
    sorted_known = sort_dict_by_values(known_frequencies)

    decryption_key = {}
    for (encrypted_char, _), (known_char, _) in zip(sorted_encrypted.items(), sorted_known.items()):
        decryption_key[encrypted_char] = known_char
    return decryption_key


# Функция для дешифровки текста
def decrypt_text(encrypted_text, decryption_key):
    return ''.join(decryption_key.get(char, char) for char in encrypted_text)


# Основной код
if __name__ == "__main__":
    # Импортируем настройки
    from constants import PATHS

    paths = read_settings(PATHS)

    # Пути к файлам
    folder = paths['folder']
    source_file_path = f"{folder}/{paths['source_file']}"
    output_file_decrypted_path = f"{folder}/{paths['output_file_decrypted']}"
    key_path = 'decryption_key.py'

    # Считываем зашифрованный текст
    with open(source_file_path, 'r', encoding='utf-8') as file:
        encrypted_text = file.read()

    # Выполнение частотного анализа зашифрованного текста
    encrypted_frequencies = frequency_analysis(encrypted_text)

    # Считываем известные частоты русского алфавита
    from decryption_key import KEY as known_frequencies

    # Создание ключа дешифровки
    decryption_key = create_decryption_key(encrypted_frequencies, known_frequencies)

    # Дешифровка текста
    decrypted_text = decrypt_text(encrypted_text, decryption_key)

    # Сохранение дешифрованного текста
    with open(output_file_decrypted_path, 'w', encoding='utf-8') as file:
        file.write(decrypted_text)

    # Сохранение ключа шифрования
    with open(key_path, 'w', encoding='utf-8') as file:
        file.write(f"KEY = {json.dumps(decryption_key, ensure_ascii=False, indent=4)}")
