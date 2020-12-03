def substitution_cipher(msg, substitutions):
    sub_len = len(substitutions)
    return ''.join([substitutions[i % sub_len][letter] for i, letter in enumerate(msg)])
