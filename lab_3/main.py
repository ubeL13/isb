import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from hybrid import Mixed
from serialization_deserialization import load_json_file
import constants


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cryptosystem = None
        self.init_ui()

    def init_ui(self):
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

    def create_cryptosystem(self):
        number_of_bits = int(self.combo_box.get())
        self.cryptosystem = Mixed(number_of_bits)
        messagebox.showinfo("Информация", "Криптосистема инициализирована.")

    def generate_keys_for_cryptosystem(self):
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

    def encrypt_text(self):
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

    def decrypt_text(self):
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

    def encrypt_with_paths_from_json(self):
        if not self.cryptosystem:
            messagebox.showerror("Ошибка", "Сначала создайте криптосистему!")
            return
        try:
            # Загрузка путей из файла paths.json с помощью функции load_json_file
            paths = load_json_file(constants.PATHS)
            self.cryptosystem.encrypt(paths['text'],
                                      paths['symmetric_key'],
                                      paths['private_key'],
                                      paths['encrypted_file'])
            messagebox.showinfo("Успех", "Текст успешно зашифрован.")
        except Exception as e:
            messagebox.showerror("Ошибка при шифровании", f"Произошла ошибка: {e}")

    def decrypt_with_paths_from_json(self):
        if not self.cryptosystem:
            messagebox.showerror("Ошибка", "Сначала создайте криптосистему!")
            return
        try:

            paths = load_json_file(constants.PATHS)
            self.cryptosystem.decrypt(paths['encrypted_file'],
                                      paths['symmetric_key'],
                                      paths['private_key'],
                                      paths['decrypted_file'])
            messagebox.showinfo("Успех", "Текст успешно расшифрован.")
        except Exception as e:
            messagebox.showerror("Ошибка при дешифровании", f"Произошла ошибка: {e}")

    def generate_keys_from_json(self):
        if not self.cryptosystem:
            messagebox.showerror("Ошибка", "Сначала создайте криптосистему!")
            return
        try:

            paths = load_json_file(constants.PATHS)
            self.cryptosystem.generate_keys(paths['symmetric_key'],
                                            paths['public_key'],
                                            paths['private_key'])
            messagebox.showinfo("Успех", "Ключи успешно сгенерированы.")
        except Exception as e:
            messagebox.showerror("Ошибка при генерации ключей", f"Произошла ошибка: {e}")


if __name__ == "__main__":
    app = Window()
    app.mainloop()
