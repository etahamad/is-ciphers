def vigenere_encrypt(plaintext, key):
    ord_plaintext, ord_key = [ord(i) for i in plaintext], [ord(i) for i in key]
    encrypted_text, len_of_txt, len_of_key = '', len(plaintext), len(key)

    for i in range(len_of_txt):
        val = (ord_plaintext[i] + ord_key[i % len_of_key]) % 26
        if plaintext[i].isupper():
            encrypted_text += chr(val+65)
        else:
            encrypted_text += chr(val+97)
    print(encrypted_text)
    return encrypted_text


def vigenere_decrypt(plaintext, key):
    ord_plaintext, ord_key = [ord(i) for i in plaintext], [ord(i) for i in key]
    encrypted_text, len_of_txt, len_of_key = '', len(plaintext), len(key)
    for i in range(len_of_txt):
        val = (ord_plaintext[i] - ord_key[i % len_of_key]) % 26
        if plaintext[i].isupper():
            encrypted_text += chr(val+65)
        else:
            encrypted_text += chr(val+97)
    return encrypted_text


"""
print(vigenere_encrypt("CODESPEEDY" , 'TIME'))
print(vigenere_decrypt("VWPILXQIWG" , 'TIME'))
# VWPILXQIWG
"""
