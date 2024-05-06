import json
from key_for_encryption import KEY
from constant import PATHS, SIGNS


def read_config(config_file: str) -> dict:
    """
        Load and return the configuration data from a JSON file.
        :param config_file: The path to the JSON configuration file.
        :return: A dictionary containing the configuration data.
        """
    with open(config_file, "r", encoding="utf-8") as file:
        return json.load(file)


def read_text(file_path: str) -> str:
    """
        Read and return the content of a text file.
        :param file_path: The path to the text file to be read.
        :return: A string containing the contents of the file.
        """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def polybius_encrypt(text: str) -> str:
    """
        Encrypt a text using the Polybius square cipher.
        :param text: The plain text string to be encrypted.
        :return: The encrypted text as a string.
        """
    encrypted_text = ""
    for char in text.upper():
        if char in SIGNS:
            encrypted_text += char
        else:
            found = False
            for i, row in enumerate(KEY):
                if char in row:
                    j = row.index(char)
                    encrypted_text += f"{i + 1}{j + 1}"
                    found = True
                    break
            if not found:
                encrypted_text += char
    return encrypted_text


def write_text(file_path: str, text: str) -> None:
    """
        Write text to a file, overwriting it if it already exists.
        :param file_path: The path to the file where the text will be written.
        :param text: The text to write to the file.
        """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)


def main() -> None:
    """
        Main function to read configuration, encrypt the source file content,
        and write the output to the target file.
        """
    config = read_config(PATHS)
    folder = config["folder"]
    source_file = config["source_file"]
    target_file = config["target_file"]

    source_text = read_text(f"{folder}/{source_file}")
    encrypted_text = polybius_encrypt(source_text)
    write_text(f"{folder}/{target_file}", encrypted_text)


if __name__ == "__main__":
    main()
