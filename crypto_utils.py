from cryptography.fernet import Fernet

# Generate a new encryption key
def generate_key():
    return Fernet.generate_key()

# Encrypt data
def encrypt_file(file_data, key):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(file_data)
    return encrypted

# Decrypt data
def decrypt_file(encrypted_data, key):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data)
    return decrypted

if __name__ == "__main__":
    key = generate_key()
    print(f"Generated Key: {key.decode()}")

    # --- Encrypt file ---
    with open("hello.txt", "rb") as f:
        original_data = f.read()

    encrypted_data = encrypt_file(original_data, key)

    with open("hello.encrypted", "wb") as f:
        f.write(encrypted_data)
    print("File encrypted -> hello.encrypted")

    # --- Decrypt file ---
    with open("hello.encrypted", "rb") as f:
        data_to_decrypt = f.read()

    decrypted_data = decrypt_file(data_to_decrypt, key)

    with open("hello_decrypted.txt", "wb") as f:
        f.write(decrypted_data)
    print("File decrypted -> hello_decrypted.txt")

