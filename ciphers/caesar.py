import re
from tkinter import messagebox


def caesar_encrypt(plainText, shift):
    # Remove non-alphabetic characters from plaintext
    plainText = re.sub("[^a-zA-Z]", "", plainText)

    # Check if plaintext is empty after removing non-alphabetic characters
    if not plainText:
        messagebox.showerror('Error', 'Plaintext must contain at least one alphabetic character')
        return ''

    # Encrypt plaintext using Caesar cipher
    cipherText = ''
    for c in plainText:
        if c.islower():
            cipherText += chr((ord(c)-97+shift) % 26 + 97) # a = 0 in the cipher but it's actually 97 in ASCII
        else:
            cipherText += chr((ord(c)-65+shift) % 26 + 65) # A = 0 in the cipher but it's actually 65 in ASCII

    return cipherText

def caesar_decrypt(cipherText, shift):
    # Remove non-alphabetic characters from ciphertext
    cipherText = re.sub("[^a-zA-Z]", "", cipherText)

    # Check if ciphertext is empty after removing non-alphabetic characters
    if not cipherText:
        messagebox.showerror('Error', 'Ciphertext must contain at least one alphabetic character')
        return ''

    # Decrypt ciphertext using Caesar cipher
    plainText = ''
    for c in cipherText:
        if c.islower():
            plainText += chr((ord(c)-97-shift) % 26 + 97)
        else:
            plainText += chr((ord(c)-65-shift) % 26 + 65)

    return plainText