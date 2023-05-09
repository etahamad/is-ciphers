def autokey_encrypt(plaintext, key):
    """
    Encrypts plaintext using the Autokey cipher with specified key.
    """
    ciphertext = ''
    key = key.upper() + plaintext.upper()
    
    for i in range(len(plaintext)):
        # If character is not an alphabet, skip
        if plaintext[i].isalpha() == False:
            ciphertext += plaintext[i]
            continue
            
        shift = ord(key[i]) - 65
        
        # Shift plaintext character by the corresponding key character
        if plaintext[i].isupper():
            ciphertext += chr((ord(plaintext[i]) - 65 + shift) % 26 + 65)
        else:
            ciphertext += chr((ord(plaintext[i]) - 97 + shift) % 26 + 97)
    
    return ciphertext


def autokey_decrypt(ciphertext, key):
    """
    Decrypts ciphertext using the Autokey cipher with specified key.
    """
    plaintext = ''
    key = key.upper()
    
    for i in range(len(ciphertext)):
        # If character is not an alphabet, skip
        if ciphertext[i].isalpha() == False:
            plaintext += ciphertext[i]
            continue
        
        shift = ord(key[i]) - 65
        
        # Shift ciphertext character back to get plaintext character
        if ciphertext[i].isupper():
            plaintext += chr((ord(ciphertext[i]) - 65 - shift) % 26 + 65)
        else:
            plaintext += chr((ord(ciphertext[i]) - 97 - shift) % 26 + 97)
        
        # Append the decrypted character to the key
        key += plaintext[-1].upper() if plaintext[-1].isalpha() else ''
    
    return plaintext
