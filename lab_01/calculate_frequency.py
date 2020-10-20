from functools import reduce


def calculate_frequency(ngrams):
    unique = list(set(ngrams))

    def count_grams(acc, ngram):
        acc[ngram] += 1
        return acc

    return reduce(count_grams, ngrams, dict(zip(unique, [0] * len(unique))))


def calculate_frequency_norm(ngrams):
    ngrams_amount = calculate_frequency(ngrams)

    ngrams_len = len(ngrams)
    for ngram in ngrams_amount:
        ngrams_amount[ngram] /= ngrams_len
        ngrams_amount[ngram] *= 100

    return ngrams_amount
