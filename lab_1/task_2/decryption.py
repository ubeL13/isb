import json

# Функция для чтения настроек из файла
def read_settings(settings_path):
    with open(settings_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Функция для выполнения частотного анализа текста и сохранения результатов в файл
def frequency_analysis(text):
    dictionary_of_frequency = {}
    len_text = len(text)
    for letter in text:
        if letter not in dictionary_of_frequency:
            frequency = text.count(letter) / len_text
            dictionary_of_frequency[letter] = frequency
    # Создание и сохранение частот в новый файл
    with open('descryption_key.py', 'w', encoding='utf-8') as file:
        json.dump(dictionary_of_frequency, file, ensure_ascii=False, indent=4)
    return dictionary_of_frequency

# Функция для создания ключа дешифровки
def create_decryption_key(encrypted_frequencies, known_frequencies):
    sorted_encrypted = sorted(encrypted_frequencies.items(), key=lambda item: item[1], reverse=True)
    sorted_known = sorted(known_frequencies.items(), key=lambda item: item[1], reverse=True)
    return {encrypted_char: known_char for (encrypted_char, _), (known_char, _) in zip(sorted_encrypted, sorted_known)}

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
