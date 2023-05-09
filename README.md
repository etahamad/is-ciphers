# is-ciphers

is-ciphers is a Python code that provides implementations of several classic ciphers, including the Caesar cipher, Vigenere cipher, and Playfair cipher.

## Requirements

is-ciphers requires Python 3.x to run, as well as the packages listed in the requirements.txt file. You can install these dependencies using pip:

```
pip install -r requirements.txt
```

## Usage

To use is-ciphers, navigate to the project directory and run the main.py file using Python:

```
python main.py
```

This will run a simple gui.

Note that each cipher module has its own `encrypt()` and `decrypt()` functions, which take a message and a key as input. The key is used to perform the encryption or decryption, and may be a string or a number depending on the cipher.
