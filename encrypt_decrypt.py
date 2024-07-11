import tkinter as tk
from tkinter import ttk, filedialog
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

class FileEncryptorApp:
    def __init__(self, master):
        self.master = master
        master.title("File Encryptor")

        # File Selection
        self.file_label = ttk.Label(master, text="Select File:")
        self.file_entry = ttk.Entry(master, state="readonly")
        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_file)

        # Password Entry for Encryption
        self.encrypt_password_label = ttk.Label(master, text="Enter Password for Encryption:")
        self.encrypt_password_entry = ttk.Entry(master, show="*")

        # Encrypt Button
        self.encrypt_button = ttk.Button(master, text="Encrypt", command=self.encrypt_file)

        # Password Entry for Decryption
        self.decrypt_password_label = ttk.Label(master, text="Enter Password for Decryption:")
        self.decrypt_password_entry = ttk.Entry(master, show="*")

        # Decrypt Button
        self.decrypt_button = ttk.Button(master, text="Decrypt", command=self.decrypt_file)

        # Layout
        self.file_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)
        self.browse_button.grid(row=0, column=3, pady=5)

        self.encrypt_password_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.encrypt_password_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)
        self.encrypt_button.grid(row=1, column=3, pady=5)

        self.decrypt_password_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.decrypt_password_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)
        self.decrypt_button.grid(row=2, column=3, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_entry.configure(state="normal")
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)
        self.file_entry.configure(state="readonly")

    def encrypt_file(self):
        file_path = self.file_entry.get()
        password = self.encrypt_password_entry.get()

        if not file_path or not password:
            return

        # Generate a key from the password
        key = self.generate_key(password)

        # Read the plaintext file
        with open(file_path, 'rb') as file:
            plaintext = file.read()

        # Create a cipher object
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

        # Encrypt the file
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        # Save the encrypted file
        encrypted_path = file_path + '.enc'
        with open(encrypted_path, 'wb') as encrypted_file:
            encrypted_file.write(iv + ciphertext)

        print(f"File encrypted: {file_path} -> {encrypted_path}")

    def decrypt_file(self):
        file_path = self.file_entry.get()
        password = self.decrypt_password_entry.get()

        if not file_path or not password:
            return

        # Generate a key from the password
        key = self.generate_key(password)

        # Read the encrypted file
        with open(file_path, 'rb') as encrypted_file:
            iv = encrypted_file.read(16)
            ciphertext = encrypted_file.read()

        # Create a cipher object
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

        # Decrypt the file
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Save the decrypted file
        decrypted_path = file_path.rstrip('.enc')
        with open(decrypted_path, 'wb') as decrypted_file:
            decrypted_file.write(plaintext)

        print(f"File decrypted: {file_path} -> {decrypted_path}")

    def generate_key(self, password):
        # Use a key derivation function to generate a key from a password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=os.urandom(16),
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        return key

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()
