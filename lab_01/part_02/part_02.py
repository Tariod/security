from calculate_frequency import calculate_frequency_norm
from ngrams import ngrams
import pandas as pd
import string
from vigenere_cipher import vigenere_cipher

encoded = 'Yx`7cen7v7ergrvc~yp:|rn7OXE7t~g.re97R9p97~c7d.xb{s7cv|r7v7dce~yp75.r{{x7`xe{' \
          's57vys;7p~ary7c.r7|rn7~d75|rn5;7oxe7c.r7q~edc7{rccre75.57`~c.75|5;7c.ry7oxe75r57`~c.75r5;7c.ry75{' \
          '57`~c.75n5;7vys7c.ry7oxe7yroc7t.ve75{' \
          r'57`~c.75|57vpv~y;7c.ry75x57`~c.75r57vys7dx7xy97Nxb7zvn7bdr7vy7~ysro7xq7tx~yt~srytr;7_vzz~yp7s~dcvytr;7\vd' \
          '~d|~7rovz~yvc~xy;7dcvc~dc~tv{7crdcd7xe7`.vcrare7zrc.xs7nxb7qrr{7`xb{s7d.x`7c.r7urdc7erdb{c9 '

KEY_RANGE = 256
ALPHABET = list(string.ascii_letters + string.digits + string.punctuation + string.whitespace)
ALPHABET = [tuple([ord(symbol)]) for symbol in ALPHABET]

with open('decoded.txt', 'w') as file:
    eng_frequency = pd.read_csv('../ngrams-frequency/letter_frequency.csv')
    eng_frequency['ngram'] = eng_frequency['ngram'].map(lambda ngram: tuple([s for s in ngram]))
    eng_frequency = eng_frequency.set_index('ngram')

    best_key = -1
    best_score = 100
    for key in range(KEY_RANGE):
        decoded_msg = vigenere_cipher(encoded.encode(), chr(key).encode())
        decoded_msg = ngrams(decoded_msg, 1)
        ngrams_frequency = calculate_frequency_norm(decoded_msg)

        score = 0
        for ngram in ngrams_frequency:
            if ngram not in ALPHABET:
                score = 100 ** 2
                break
            score += (ngrams_frequency[ngram] - eng_frequency.get(ngram, 0)) ** 2
        score = score ** 0.5
        best_score, best_key = (score, key) if score < best_score else (best_score, best_key)

    decoded_msg = vigenere_cipher(encoded.encode(), chr(best_key).encode())
    print('Key: ' + str(best_key))
    print(decoded_msg)
    file.write(f'Key {best_key}: {decoded_msg}\n')
