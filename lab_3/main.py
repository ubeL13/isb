import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
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
        tk.Label(self, text="Привет пользователь!").pack()

        self.label_number_of_bits = tk.Label(self, text="Выберите количество битов для ключей:")
        self.label_number_of_bits.pack()

        self.combo_box = ttk.Combobox(self, values=[ "128","196", "256" ])
        self.combo_box.pack()

        tk.Button(self, text="Инициализация криптосистемы", command=self.create_cryptosystem).pack()
        tk.Button(self, text="Создание ключей", command=self.generate_keys_for_cryptosystem).pack()
        tk.Button(self, text="Зашифровать текст", command=self.encrypt_text).pack()
        tk.Button(self, text="Дешифровать текст", command=self.decrypt_text).pack()

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

        # Запрос пользователю выбрать файл зашифрованного текста
        path_to_encrypted_text = filedialog.askopenfilename(title="Выберите зашифрованный текст",
                                                            filetypes=[("Encrypted files", "*.txt"),
                                                                       ("All files", "*.*")])
        if not path_to_encrypted_text:
            messagebox.showerror("Ошибка", "Файл зашифрованного текста не выбран!")
            return

        # Запрос пользователю выбрать файл с зашифрованным симметричным ключом
        path_to_symmetric_key = filedialog.askopenfilename(title="Выберите файл с симметричным ключом",
                                                           filetypes=[("Key files", "*.txt"), ("All files", "*.*")])
        if not path_to_symmetric_key:
            messagebox.showerror("Ошибка", "Файл симметричного ключа не выбран!")
            return

        # Запрос пользователю выбрать файл с приватным ключом
        path_to_private_key = filedialog.askopenfilename(title="Выберите файл с приватным ключом",
                                                         filetypes=[("Private key files", "*.pem"),
                                                                    ("All files", "*.*")])
        if not path_to_private_key:
            messagebox.showerror("Ошибка", "Файл приватного ключа не выбран!")
            return

        # Запрос пользователю выбрать место для сохранения расшифрованного текста
        path_to_save_decrypted_text = filedialog.asksaveasfilename(title="Сохранить расшифрованный текст как",
                                                                   defaultextension=".txt",
                                                                   filetypes=[("Text files", "*.txt"),
                                                                              ("All files", "*.*")])
        if not path_to_save_decrypted_text:
            messagebox.showerror("Ошибка", "Файл для сохранения расшифрованного текста не выбран!")
            return


        # Попытка расшифровать текст с использованием выбранных файлов и сохранить результат
        try:
            self.cryptosystem.decrypt(path_to_encrypted_text, path_to_symmetric_key, path_to_private_key,
                                      path_to_save_decrypted_text)
            messagebox.showinfo("Успех", "Текст успешно расшифрован.")
        except Exception as e:
            messagebox.showerror("Ошибка при дешифровании", f"Произошла ошибка: {e}")

        self.cryptosystem.decrypt(path_to_encrypted_text, path_to_symmetric_key, path_to_private_key,
                                  path_to_save_decrypted_text)
        messagebox.showinfo("Информация", "Текст успешно расшифрован.")



if __name__ == "__main__":
    app = Window()
    app.mainloop()