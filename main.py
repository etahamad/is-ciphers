import tkinter as tk
from tkinter import messagebox
from playfair import playfair_encrypt, playfair_decrypt
from caesar import caesar_encrypt, caesar_decrypt
from vigenere import vigenere_encrypt, vigenere_decrypt
from autokey import autokey_encrypt, autokey_decrypt
from rsa import generate_keys, rsa_encrypt, rsa_decrypt

class App:
    def __init__(self, master):
        self.master = master
        master.title('Cipher Tool')

        input_frame = tk.Frame(master)
        input_frame.grid(row=0, column=0, pady=10)

        tk.Label(input_frame, text='Enter Plain/Cipher Text:').grid(row=0,
                                                                    column=0, sticky='w')
        self.input_entry = tk.Entry(input_frame, width=50)
        self.input_entry.grid(row=1, column=0, padx=10, pady=5)

        tk.Label(input_frame, text='Enter Key/Shift Value/PublicKey:').grid(row=2,
                                                                  column=0, sticky='w')
        self.key_entry = tk.Entry(input_frame, width=20)
        self.key_entry.grid(row=3, column=0, padx=10, pady=5)

        self.cipher_var = tk.StringVar()

        dropdown_frame = tk.Frame(master)
        dropdown_frame.grid(row=0, column=1, pady=10)

        tk.Label(dropdown_frame, text='Select Cipher:').grid(
            row=0, column=0, sticky='w')
        self.cipher_dropdown = tk.OptionMenu(
            dropdown_frame, self.cipher_var, 'Playfair', 'Caesar', 'Vigenere', 'Autokey', 'RSA')
        self.cipher_dropdown.grid(row=1, column=0, padx=10, pady=5)

        button_frame = tk.Frame(master)
        button_frame.grid(row=1, column=0, columnspan=2)

        self.encrypt_button = tk.Button(
            button_frame, text='Encrypt', command=self.encrypt)
        self.encrypt_button.grid(row=0, column=0, padx=10, pady=5)

        self.decrypt_button = tk.Button(
            button_frame, text='Decrypt', command=self.decrypt)
        self.decrypt_button.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(master, text='Result:').grid(row=2, column=0, sticky='w')

        self.result_text = tk.Text(master, height=6, width=50)
        self.result_text.grid(row=3, column=0, padx=10, pady=5)

    def encrypt(self):
        plaintext = self.input_entry.get()
        key = self.key_entry.get()
        cipher = self.cipher_var.get()

        if cipher == 'Playfair':
            ciphertext = playfair_encrypt(plaintext, key)
        elif cipher == 'Caesar':
            try:
                shift = int(key)
            except ValueError:
                messagebox.showerror('Error', 'Shift value must be an integer')
                return
            ciphertext = caesar_encrypt(plaintext, shift)
        elif cipher == 'Vigenere':
            ciphertext = vigenere_encrypt(plaintext, key)
        elif cipher == 'Autokey':
            ciphertext = autokey_encrypt(plaintext, key)
        elif cipher == 'RSA':
            try:
                public_key_parts = [int(k) for k in key.split(',')]
                if len(public_key_parts) != 2:
                    raise ValueError()
                public_key = (public_key_parts[0], public_key_parts[1])
            except:
                messagebox.showerror('Error', 'Invalid public key format')
                return
            ciphertext = rsa_encrypt(plaintext, public_key)
        else:
            messagebox.showerror('Error', 'Invalid cipher selected')
            return

        if ciphertext:
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('1.0', ciphertext)

    def decrypt(self):
        ciphertext = self.input_entry.get()
        key = self.key_entry.get()
        cipher = self.cipher_var.get()

        if cipher == 'Playfair':
            plaintext = playfair_decrypt(ciphertext, key)
        elif cipher == 'Caesar':
            try:
                shift = int(key)
            except ValueError:
                messagebox.showerror('Error', 'Shift value must be an integer')
                return
            plaintext = caesar_decrypt(ciphertext, shift)
        elif cipher == 'Vigenere':
            plaintext = vigenere_decrypt(ciphertext, key)
        elif cipher == 'Autokey':
            plaintext = autokey_decrypt(ciphertext, key)
        elif cipher == 'RSA':
            try:
                private_key_parts = [int(k) for k in key.split(',')]
                if len(private_key_parts) != 2:
                    raise ValueError()
                private_key = (private_key_parts[0], private_key_parts[1])
            except:
                messagebox.showerror('Error', 'Invalid private key format')
                return
            plaintext = rsa_decrypt(ciphertext, private_key)
        else:
            messagebox.showerror('Error', 'Invalid cipher selected')
            return

        if plaintext:
            self.result_text.delete('1.0', 'end')
            self.result_text.insert('1.0', plaintext)


root = tk.Tk()
app = App(root)
root.mainloop()
