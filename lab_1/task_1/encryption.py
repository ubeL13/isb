import json
from key_for_encryption import KEY
from constant import PATHS, SIGNS

def read_config(config_file):
    with open(config_file, "r", encoding="utf-8") as file:
        return json.load(file)

def read_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def polybius_encrypt(text):
    encrypted_text = ""
    for char in text.upper():
        if char in SIGNS:
            encrypted_text += char
        else:
            found = False
            for i, row in enumerate(KEY):
                if char in row:
                    j = row.index(char)
                    encrypted_text += f"{i+1}{j+1}"
                    found = True
                    break
            if not found:
                encrypted_text += char  # Если символ не найден, оставляем его без изменений
    return encrypted_text

def write_text(file_path, text):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

def main():
    config = read_config(PATHS)
    folder = config["folder"]
    source_file = config["source_file"]
    target_file = config["target_file"]

    source_text = read_text(f"{folder}/{source_file}")
    encrypted_text = polybius_encrypt(source_text)
    write_text(f"{folder}/{target_file}", encrypted_text)
    print("Текст успешно зашифрован и сохранен.")

if __name__ == "__main__":
    main()
