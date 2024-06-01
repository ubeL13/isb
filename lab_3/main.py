import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from constants import PATHS
from hybrid import Mixed
from serialization_deserialization import load_json_file


class Window(tk.Tk):
    """
    Represents a Window for the hybrid cryptosystem application.
    This class includes methods to initialize the Window, create a cryptosystem, generate keys, encrypt and decrypt text.
    """

    def __init__(self):
        """
        Initializes the class instance by setting up the base class, initializing
        the cryptosystem attribute to None, and setting up the user interface.
        """
        super().__init__()
        self.cryptosystem = None
        self.init_ui()

    def init_ui(self):
        """
        Sets up the user interface for the hybrid cryptosystem application.

        This method creates and arranges the GUI components, including the window title,
        geometry, labels, a combobox for key bit selection, and buttons for initializing
        the cryptosystem, generating keys, encrypting and decrypting text, handling JSON
        paths for encryption and decryption, generating keys from JSON, and exiting the application.
        """
        self.title("Гибридная Криптосистема")
        self.geometry("500x500")

        self.label_number_of_bits = tk.Label(self, text="Выберите количество битов для ключей:")
        self.label_number_of_bits.pack()

        self.combo_box = ttk.Combobox(self, values=["128", "196", "256"])
        self.combo_box.pack()

        tk.Button(self, text="Инициализация криптосистемы", command=self.create_cryptosystem).pack()
        tk.Button(self, text="Создание ключей", command=self.generate_keys_for_cryptosystem).pack()
        tk.Button(self, text="Зашифровать текст", command=self.encrypt_text).pack()
        tk.Button(self, text="Дешифровать текст", command=self.decrypt_text).pack()
        tk.Button(self, text="Зашифровать с путями из JSON", command=self.encrypt_with_paths_from_json).pack()
        tk.Button(self, text="Дешифровать с путями из JSON", command=self.decrypt_with_paths_from_json).pack()
        tk.Button(self, text="Создание ключей с путями из JSON", command=self.generate_keys_from_json).pack()
        tk.Button(self, text="Выход", command=self.quit).pack(side=tk.BOTTOM)

    def create_cryptosystem(self) -> None:
        """
        Creates and initializes the cryptosystem with the selected number of bits for the keys.
        This method reads the selected value from the combobox, which represents the key size,
        and initializes the cryptosystem with this value. A message box then informs the user
        that the cryptosystem has been successfully initialized.
        """
        number_of_bits = int(self.combo_box.get())
        self.cryptosystem = Mixed(number_of_bits)
        messagebox.showinfo("Информация", "Криптосистема инициализирована.")

    def generate_keys_for_cryptosystem(self) -> None:
        """
        Generates keys for the initialized cryptosystem.
        This method checks if the cryptosystem has been created. If not, it shows an error
        message box prompting the user to create a cryptosystem first. Otherwise, it proceeds
        to generate the keys for the cryptosystem.
        """

        if not self.cryptosystem:
            messagebox.showerror("Ошибка", "Сначала создайте криптосистему!")
            return

        path_to_symmetric_key = filedialog.asksaveasfilename(defaultextension=".txt",
                                                             filetypes=[("Key files", "*.txt")])
        path_to_public_key = filedialog.asksaveasfilename(defaultextension=".pub",
                                                          filetypes=[("Public key files", "*.pem")])
        path_to_private_key = filedialog.asksaveasfilename(defaultextension=".priv",
                                                           filetypes=[("Private key files", "*.pem")])

        if not path_to_symmetric_key or not path_to_public_key or not path_to_private_key:
            messagebox.showerror("Ошибка", "Необходимо указать пути для всех ключей!")
            return

        self.cryptosystem.generate_keys(path_to_symmetric_key, path_to_public_key, path_to_private_key)
        messagebox.showinfo("Информация", "Ключи успешно созданы.")

    def encrypt_text(self) -> None:
        """
        This method encrypts a given text using the cryptographic system.
        It prompts for the text file to be encrypted, symmetric key,
        private key files and the location to save the encrypted text file.
        An error is shown if the cryptographic system hasn't been set up yet.
        Another error will be shown if required file paths aren't supplied.
        """
        if not self.cryptosystem:
            messagebox.showerror("Ошибка", "Сначала создайте криптосистему!")
            return

        path_to_text_for_encryption = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        path_to_symmetric_key = filedialog.askopenfilename(filetypes=[("Key files", "*.txt")])
        path_to_private_key = filedialog.askopenfilename(filetypes=[("Private key files", "*.pem")])
        path_to_save_encrypted_text = filedialog.asksaveasfilename(defaultextension=".txt",
                                                                   filetypes=[("Encrypted files", "*.txt")])

        if not path_to_text_for_encryption or not path_to_symmetric_key or not path_to_private_key or not path_to_save_encrypted_text:
            messagebox.showerror("Ошибка", "Необходимо указать пути к файлам для шифрования!")
            return

        self.cryptosystem.encrypt(path_to_text_for_encryption, path_to_symmetric_key, path_to_private_key,
                                  path_to_save_encrypted_text)
        messagebox.showinfo("Информация", "Текст успешно зашифрован.")

    def decrypt_text(self) -> None:
        """
            Decrypts an encrypted text file using a specified symmetric key and private key.
            If any of the required files are not selected, an error message is displayed and the
            operation is aborted. Upon successful selection of all files, the method attempts to
            decrypt the encrypted text using the provided keys. Success or failure of the decryption
            process is communicated to the user via message boxes.
            """
        if not self.cryptosystem:
            messagebox.showerror("Ошибка", "Сначала создайте криптосистему!")
            return

        path_to_encrypted_text = filedialog.askopenfilename(title="Выберите зашифрованный текст",
                                                            filetypes=[("Encrypted files", "*.txt"),
                                                                       ("All files", "*.*")])
        if not path_to_encrypted_text:
            messagebox.showerror("Ошибка", "Файл зашифрованного текста не выбран!")
            return

        path_to_symmetric_key = filedialog.askopenfilename(title="Выберите файл с симметричным ключом",
                                                           filetypes=[("Key files", "*.txt"), ("All files", "*.*")])
        if not path_to_symmetric_key:
            messagebox.showerror("Ошибка", "Файл симметричного ключа не выбран!")
            return

        path_to_private_key = filedialog.askopenfilename(title="Выберите файл с приватным ключом",
                                                         filetypes=[("Private key files", "*.pem"),
                                                                    ("All files", "*.*")])
        if not path_to_private_key:
            messagebox.showerror("Ошибка", "Файл приватного ключа не выбран!")
            return

        path_to_save_decrypted_text = filedialog.asksaveasfilename(title="Сохранить расшифрованный текст как",
                                                                   defaultextension=".txt",
                                                                   filetypes=[("Text files", "*.txt"),
                                                                              ("All files", "*.*")])
        if not path_to_save_decrypted_text:
            messagebox.showerror("Ошибка", "Файл для сохранения расшифрованного текста не выбран!")
            return

        try:
            self.cryptosystem.decrypt(path_to_encrypted_text, path_to_symmetric_key, path_to_private_key,
                                      path_to_save_decrypted_text)
            messagebox.showinfo("Успех", "Текст успешно расшифрован.")
        except Exception as e:
            messagebox.showerror("Ошибка при дешифровании", f"Произошла ошибка: {e}")

        self.cryptosystem.decrypt(path_to_encrypted_text, path_to_symmetric_key, path_to_private_key,
                                  path_to_save_decrypted_text)
        messagebox.showinfo("Информация", "Текст успешно расшифрован.")

    def encrypt_with_paths_from_json(self) -> None:
        """
       This method encrypts text using the paths to key files specified in a JSON file.
       First, it loads the JSON file from which the file paths are extracted.
       Then, it proceeds to encrypt the text.
       A failure message is displayed in case of an exception.
       """
        if not self.cryptosystem:
            messagebox.showerror("Ошибка", "Сначала создайте криптосистему!")
            return
        try:
            paths = load_json_file(PATHS)
            self.cryptosystem.encrypt(paths['text'],
                                      paths['symmetric_key'],
                                      paths['private_key'],
                                      paths['encrypted_file'])
            messagebox.showinfo("Успех", "Текст успешно зашифрован.")
        except Exception as e:
            messagebox.showerror("Ошибка при шифровании", f"Произошла ошибка: {e}")

    def decrypt_with_paths_from_json(self) -> None:
        """
        This method decrypts encrypted text using the paths to key files specified in a JSON file.
        First, it loads the JSON file from which the file paths are extracted.
        Then, it proceeds to decrypt the text.
        A failure message is displayed in case of an exception.
        """
        if not self.cryptosystem:
            messagebox.showerror("Ошибка", "Сначала создайте криптосистему!")
            return
        try:

            paths = load_json_file(PATHS)
            self.cryptosystem.decrypt(paths['encrypted_file'],
                                      paths['symmetric_key'],
                                      paths['private_key'],
                                      paths['decrypted_file'])
            messagebox.showinfo("Успех", "Текст успешно расшифрован.")
        except Exception as e:
            messagebox.showerror("Ошибка при дешифровании", f"Произошла ошибка: {e}")

    def generate_keys_from_json(self) -> None:
        """
        This method generates keys for the cryptosystem using the paths to key files specified in a JSON file.
        First, it loads the JSON file from which the file paths are extracted.
        Then, it proceeds to generate keys.
        A failure message is displayed in case of an exception.
        """
        if not self.cryptosystem:
            messagebox.showerror("Ошибка", "Сначала создайте криптосистему!")
            return
        try:

            paths = load_json_file(PATHS)
            self.cryptosystem.generate_keys(paths['symmetric_key'],
                                            paths['public_key'],
                                            paths['private_key'])
            messagebox.showinfo("Успех", "Ключи успешно сгенерированы.")
        except Exception as e:
            messagebox.showerror("Ошибка при генерации ключей", f"Произошла ошибка: {e}")


if __name__ == "__main__":
    app = Window()
    app.mainloop()
