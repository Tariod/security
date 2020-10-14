def ngrams(sequence, n):
    return list(zip(*[sequence[i:(len(sequence) - (n - 1) + i)] for i in range(n)]))
