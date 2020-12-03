from calculate_frequency import calculate_frequency_norm
from functools import reduce
from ngrams import ngrams
import numpy as np
from scipy.signal import argrelextrema


def index_of_coincidence(sequence):
    sequence = ngrams(sequence, 1)
    ngrams_frequency = calculate_frequency_norm(sequence)
    return reduce(lambda acc, symbol: acc + (ngrams_frequency[symbol] / 100) ** 2, ngrams_frequency, 0)


def key_len(sequence):
    keys_IC = []
    for key_len in range(1, 27):
        ic = 0
        for i in range(key_len):
            ic += index_of_coincidence(sequence[i::key_len])
        ic /= key_len
        keys_IC.append(ic)

    def helper(ic):
        keys, = argrelextrema(ic, np.greater)
        if len(keys) == 0:
            return 1

        key = helper(ic[keys])
        return keys[key - 1] + 1

    keys_IC = np.array(keys_IC)
    if np.all(keys_IC > 0.06):
        return -1

    return helper(keys_IC)
