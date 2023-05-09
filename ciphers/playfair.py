from tkinter import messagebox
import re

def playfair_encrypt(plainText, key):
    # Remove non-alphabetic characters from plaintext and key
    plainText = re.sub("[^a-z]", "", plainText.lower().replace('j', 'i'))
    key = re.sub("[^a-z]", "", key.lower().replace('j', 'i'))

    # Check if plaintext and key are empty after removing non-alphabetic characters
    if not plainText:
        messagebox.showerror('Error', 'Plaintext must contain at least one alphabetic character')
        return ''
    if not key:
        messagebox.showerror('Error', 'Key must contain at least one alphabetic character')
        return ''

    # Check that all characters in plaintext and key are allowed in the Playfair cipher
    allowed_chars = 'abcdefghiklmnopqrstuvwxyz'
    for c in plainText + key:
        if c not in allowed_chars:
            messagebox.showerror('Error', f'Character "{c}" is not allowed in the Playfair cipher')
            return ''

    # Create Playfair matrix
    key = key.replace('j', 'i')
    key += allowed_chars
    matrix = []
    for c in key:
        if c not in matrix:
            matrix.append(c)

    # Split plaintext into digraphs
    digraphs = re.findall('[a-z][a-z]', plainText)
    if len(digraphs) * 2 < len(plainText):
        digraphs.append(plainText[-1] + 'x')

    # Encrypt each digraph
    ciphertext = ''
    for d in digraphs:
        row0, col0 = divmod(matrix.index(d[0]), 5)
        row1, col1 = divmod(matrix.index(d[1]), 5)
        if row0 == row1:
            ciphertext += matrix[row0*5 + (col0+1)%5]
            ciphertext += matrix[row1*5 + (col1+1)%5]
        elif col0 == col1:
            ciphertext += matrix[((row0+1)%5)*5 + col0]
            ciphertext += matrix[((row1+1)%5)*5 + col1]
        else:
            ciphertext += matrix[row0*5 + col1]
            ciphertext += matrix[row1*5 + col0]

    return ciphertext

def playfair_decrypt(cipherText, key):
    # Remove non-alphabetic characters from ciphertext and key
    cipherText = re.sub("[^a-z]", "", cipherText.lower().replace('j', 'i'))
    key = re.sub("[^a-z]", "", key.lower().replace('j', 'i'))

    # Check if ciphertext and key are empty after removing non-alphabetic characters
    if not cipherText:
        messagebox.showerror('Error', 'Ciphertext must contain at least one alphabetic character')
        return ''
    if not key:
        messagebox.showerror('Error', 'Key must contain at least one alphabetic character')
        return ''

    # Check that all characters in ciphertext and key are allowed in the Playfair cipher
    allowed_chars = 'abcdefghiklmnopqrstuvwxyz'
    for c in cipherText + key:
        if c not in allowed_chars:
            messagebox.showerror('Error', f'Character "{c}" is not allowed in the Playfair cipher')
            return ''

    # Create Playfair matrix
    key = key.replace('j', 'i')
    key += allowed_chars
    matrix = []
    for c in key:
        if c not in matrix:
            matrix.append(c)

    # Decrypt each digraph
    plaintext = ''
    for i in range(0, len(cipherText), 2):
        row0, col0 = divmod(matrix.index(cipherText[i]), 5)
        row1, col1 = divmod(matrix.index(cipherText[i+1]), 5)
        if row0 == row1:
            plaintext += matrix[row0*5 + (col0-1)%5]
            plaintext += matrix[row1*5 + (col1-1)%5]
        elif col0 == col1:
            plaintext += matrix[((row0-1)%5)*5 + col0]
            plaintext += matrix[((row1-1)%5)*5 + col1]
        else:
            plaintext += matrix[row0*5 + col1]
            plaintext += matrix[row1*5 + col0]

    return plaintext