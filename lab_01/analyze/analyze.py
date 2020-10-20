import matplotlib.pyplot as plt
import re
import seaborn as sns

from calculate_frequency import calculate_frequency
from ngrams import ngrams
from vigenere_cipher import vigenere_cipher

encoded = 'c3437dbc7c1255d3a21d444d86ebf2e9234c22bdef81042e1e86acb765718ea37393a1292452bbcca3c1509bd8df6d72992b312e4f' \
          '6b7f4ce7fd3f3d3f95edc0399d06d4b84e7811dd79272c69c8ed3a5d519dc941b90db6e4c1de9ecda3d6c1a3217d184f8278c89ad1' \
          '6da05fec4fdfc61fe44798b92720422962ba8ed1df2564b3d568b0c3808c4bb5d9e2de986a93db399554210777239b937b4b8fecc0' \
          '011ef50edc9f644f7fe379d61418546a4497354298fd80598eb62148b61e75200c0a5efede36395445de68c179fe674d5b0f405154' \
          '240b3fae9f0c24222886fd6babd9c984c23628614709c15631206ad5a6f1723d68ddb143f08d65807bede824bdad67af'


def coincidence_index(ngrams, length):
    ci = 0
    for ngram in ngrams:
        ci += ngrams[ngram] * (ngrams[ngram] - 1) / (length * (length - 1))
    return ci * 100


encoded_utf8 = bytes([int(symbol, base=16) for symbol in re.findall(r'.{2}', encoded)])
encoded_utf8 = [int(byte) for byte in encoded_utf8][::2]
# encoded_utf8 = ngrams(encoded_utf8, 1)
#
# indexes = []
# for i in range(1, 15):
#     msg = encoded_utf8[::i]
#     frequency = calculate_frequency(msg)
#     indexes.append(coincidence_index(frequency, len(msg)))
#
# print(indexes)

ALPHABET_SIZE = 256
with open('decoded.txt', 'w') as file:
    for key in range(ALPHABET_SIZE):
        file.write(f'Key {key}: {vigenere_cipher(encoded.encode(), chr(key).encode())}\n')
# sns.distplot(list(enumerate(indexes)))
# plt.show()
