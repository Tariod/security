from functools import reduce


def count_grams(acc, ngram):
    acc[ngram] += 1
    return acc


def calculate_frequency(ngrams):
    unique = list(set(ngrams))
    ngrams_amount = reduce(count_grams, ngrams, dict(zip(unique, [0] * len(unique))))

    ngrams_len = len(ngrams)
    for ngram in ngrams_amount:
        ngrams_amount[ngram] /= ngrams_len
        ngrams_amount[ngram] *= 100

    return ngrams_amount
