from hybrid import Hybrid

def main():
    # Путь к файлам ключей и текста
    path_to_symmetric_key = 'symmetric.key'
    path_to_public_key = 'public.key'
    path_to_private_key = 'private.key'
    path_to_text_for_encryption = 'plain.txt'
    path_to_save_encrypted_text = 'encrypted.txt'
    path_to_save_decrypted_text = 'decrypted.txt'

    cryptosystem = Hybrid(2048)

    cryptosystem.generate_keys(path_to_symmetric_key, path_to_public_key, path_to_private_key)


    cryptosystem.encrypt(path_to_text_for_encryption, path_to_symmetric_key, path_to_private_key, path_to_save_encrypted_text)

    cryptosystem.decrypt(path_to_save_encrypted_text, path_to_symmetric_key, path_to_private_key, path_to_save_decrypted_text)

    print('Encryption and decryption have been completed.')

if __name__ == '__main__':
    main()
