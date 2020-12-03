from calculate_frequency import calculate_frequency_norm
from index_of_coincidence import key_len
from ngrams import ngrams
import pandas as pd
import string
import sys
from vigenere_cipher import vigenere_cipher

encoded = '1c41023f564b2a130824570e6b47046b521f3f5208201318245e0e6b40022643072e13183e51183f5a1f3e4702245d4b285a1b2356' \
          '1965133f2413192e571e28564b3f5b0e6b50042643072e4b023f4a4b24554b3f5b0238130425564b3c564b3c5a0727131e38564b24' \
          '5d0732131e3b430e39500a38564b27561f3f5619381f4b385c4b3f5b0e6b580e32401b2a500e6b5a186b5c05274a4b79054a6b6704' \
          '6b540e3f131f235a186b5c052e13192254033f130a3e470426521f22500a275f126b4a043e131c225f076b431924510a295f126b5d' \
          '0e2e574b3f5c4b3e400e6b400426564b385c193f13042d130c2e5d0e3f5a086b52072c5c192247032613433c5b02285b4b3c5c1920' \
          '560f6b47032e13092e401f6b5f0a38474b32560a391a476b40022646072a470e2f130a255d0e2a5f0225544b24414b2c410a2f5a0e' \
          '25474b2f56182856053f1d4b185619225c1e385f1267131c395a1f2e13023f13192254033f13052444476b4a043e131c225f076b5d' \
          '0e2e574b22474b3f5c4b2f56082243032e414b3f5b0e6b5d0e33474b245d0e6b52186b440e275f456b710e2a414b225d4b265a052f' \
          '1f4b3f5b0e395689cbaa186b5d046b401b2a500e381d4b23471f3b4051641c0f2450186554042454072e1d08245e442f5c083e5e0e' \
          '2547442f1c5a0a64123c503e027e040c413428592406521a21420e184a2a32492072000228622e7f64467d512f0e7f0d1a'

encoded_utf8 = bytes.fromhex(encoded)

SYMBOLS = string.ascii_letters + string.digits + string.punctuation + string.whitespace
ALPHABET = [tuple([ord(symbol)]) for symbol in SYMBOLS] + [(128,), (153,), (226,)]

eng_frequency = pd.read_csv('../ngrams-frequency/letter_frequency.csv')
eng_frequency['ngram'] = eng_frequency['ngram'].map(lambda ng: tuple([s for s in ng]))
eng_frequency = eng_frequency.set_index('ngram')

KEY_RANGE = 256
KEY_LEN = key_len(encoded_utf8)
KEY = []
for i in range(KEY_LEN):
    msg = encoded_utf8[i::KEY_LEN]

    best_key = -1
    best_score = sys.maxsize
    for key in range(KEY_RANGE):
        decoded_msg = vigenere_cipher(msg, chr(key).encode())
        decoded_msg = ngrams(decoded_msg, 1)
        ngrams_frequency = calculate_frequency_norm(decoded_msg)

        score = 0
        for ngram in ngrams_frequency:
            if ngram not in ALPHABET:
                score = sys.maxsize
                break
            else:
                score += (ngrams_frequency[ngram] - eng_frequency.get(ngram, 0)) ** 2
        score = score ** 0.5
        best_score, best_key = (score, key) if score < best_score else (best_score, best_key)

    KEY.append(best_key)

with open('decoded.txt', 'w') as file:
    file.write(f"Key {bytes(KEY).decode()}: {vigenere_cipher(encoded_utf8, bytes(KEY)).decode('windows-1252')}\n")
