def substitution_cipher(msg, substitutions):
    return ''.join([substitutions[letter] for letter in msg])
