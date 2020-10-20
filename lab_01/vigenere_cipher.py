def vigenere_cipher(msg, key):
    key_len = len(key)
    return bytes([symbol ^ key[i % key_len] for i, symbol in enumerate(msg)])
