import random
from math import gcd

def generate_keys(key_size=1024):
    # Generate public and private keys 
    p = random_prime(key_size)
    q = random_prime(key_size)
    while q == p:
        q = random_prime(key_size)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    g = gcd(e, phi)
    while g != 1:
        e = random.randint(2, phi - 1)
        g = gcd(e, phi)

    d = inverse_modulo(e, phi)

    return ((e, n), (d, n))

def random_prime(k):
    # Generate a random prime number using a Miller-Rabin test
    while True:
        num = random.randint(10**(k-1), 10**k - 1)
        if is_prime(num):
            return num

def is_prime(n, k=50):
    # Check if a number is prime
    if n <= 1:
        return False

    for _ in range(k):
        a = random.randint(1, n-1)
        if pow(a, n-1, n) != 1:
            return False

    return True

def inverse_modulo(a, m):
    # Calculate the modular multiplicative inverse of a mod m
    gcd, x, y = extended_euclidean_algorithm(a, m)
    if gcd != 1:
        raise Exception('No modular inverse exists')
    return x % m

def extended_euclidean_algorithm(a, b):
    # Calculate the greatest common divisor of a and b and their Bezout coefficients x, y
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_euclidean_algorithm(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def rsa_encrypt(plaintext, pubkey):
    # Encrypt plaintext using RSA public key
    e, n = pubkey
    ciphertext = []
    for char in plaintext:
        m = ord(char)
        c = pow(m, e, n)
        ciphertext.append(c)
    return ciphertext

def rsa_decrypt(ciphertext, privkey):
    # Decrypt ciphertext using RSA private key
    d, n = privkey
    plaintext = ''
    for c in ciphertext:
        m = pow(c, d, n)
        plaintext += chr(m)
    return plaintext

def save_private_key(privkey, filename='private.key'):
    # Save private key to file
    with open(filename, 'w') as f:
        f.write('Private Key\n')
        f.write(str(privkey[0]) + '\n')
        f.write(str(privkey[1]))

def load_private_key(filename='private.key'):
    # Load private key from file
    with open(filename, 'r') as f:
        lines = f.readlines()
        try:
            d = int(lines[1])
            n = int(lines[2])
            return (d, n)
        except (IndexError, ValueError):
            raise Exception('Invalid private key file')
