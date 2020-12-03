import math
from functools import partial

import pandas as pd
import random
import string

from calculate_frequency import calculate_frequency_norm
from index_of_coincidence import key_len
from ngrams import ngrams
from substitution_cipher import substitution_cipher

# ================ ALPHABET CONF ================
ALPHABET = string.ascii_uppercase
NGRAMS_SIZE = 3  # NGRAMS_SIZE > 1
NGRAMS_STAT = {string.ascii_uppercase: [None, '../ngrams-frequency/trigrams_frequency.csv']}
# =================== GEN CONF ==================
POPULATION_SIZE = 200
NUMBER_OF_GENERATIONS = 400
CROSSOVER_COEFFICIENT = 0.6
MUTATION_PROBABILITY = 0.3

encoded = 'KZBWPFHRAFHMFSNYSMNOZYBYLLLYJFBGZYYYZYEKCJVSACAEFLMAJZQAZYHIJFUNHLCGCINWFIHHHTLNVZLSHSVOZDPYSMNYJXHMNODNH' \
          'PATXFWGHZPGHCVRWYSNFUSPPETRJSIIZSAAOYLNEENGHYAMAZBYSMNSJRNGZGSEZLNGHTSTJMNSJRESFRPGQPSYFGSWZMBGQFBCCEZTTP' \
          'OYNIVUJRVSZSCYSEYJWYHUJRVSZSCRNECPFHHZJBUHDHSNNZQKADMGFBPGBZUNVFIGNWLGCWSATVSSWWPGZHNETEBEJFBCZDPYJWOSFDV' \
          'WOTANCZIHCYIMJSIGFQLYNZZSETSYSEUMHRLAAGSEFUSKBZUEJQVTDZVCFHLAAJSFJSCNFSJKCFBCFSPITQHZJLBMHECNHFHGNZIEWBLG' \
          'NFMHNMHMFSVPVHSGGMBGCWSEZSZGSEPFQEIMQEZZJIOGPIOMNSSOFWSKCRLAAGSKNEAHBBSKKEVTZSSOHEUTTQYMCPHZJFHGPZQOZHLCF' \
          'SVYNFYYSEZGNTVRAJVTEMPADZDSVHVYJWHGQFWKTSNYHTSZFYHMAEJMNLNGFQNFZWSKCCJHPEHZZSZGDZDSVHVYJWHGQFWKTSNYHTSZFY' \
          'HMAEDNJZQAZSCHPYSKXLHMQZNKOIOKHYMKKEIKCGSGYBPHPECKCJJKNISTJJZMHTVRHQSGQMBWHTSPTHSNFQZKPRLYSZDYPEMGZILSDIO' \
          'GGMNYZVSNHTAYGFBZZYJKQELSJXHGCJLSDTLNEHLYZHVRCJHZTYWAFGSHBZDTNRSESZVNJIVWFIVYSEJHFSLSHTLNQEIKQEASQJVYSEVY' \
          'SEUYSMBWNSVYXEIKWYSYSEYKPESKNCGRHGSEZLNGHTSIZHSZZHCUJWARNEHZZIWHZDZMADNGPNSYFZUWZSLXJFBCGEANWHSYSEGGNIVPF' \
          'LUGCEUWTENKCJNVTDPNXEIKWYSYSFHESFPAJSWGTYVSJIOKHRSKPEZMADLSDIVKKWSFHZBGEEATJLBOTDPMCPHHVZNYVZBGZSCHCEZZTW' \
          'OOJMBYJSCYFRLSZSCYSEVYSEUNHZVHRFBCCZZYSEUGZDCGZDGMHDYNAFNZHTUGJJOEZBLYZDHYSHSGJMWZHWAFTIAAY'


def parse_ngram_stats(alphabet, ngrams_size):
    stat_filename = NGRAMS_STAT[alphabet][ngrams_size - 2]
    stats = pd.read_csv(stat_filename)
    stats['ngram'] = stats['ngram'].map(lambda ngram: tuple([s for s in ngram]))
    stats['frequency'] = stats['frequency'].map(lambda fr: math.log2(fr))
    stats = stats.set_index('ngram')
    return stats['frequency'].to_dict()


def permutations(population):
    if len(population) == 0:
        return [[]]

    curr = population[:1][0]
    others = permutations(population[1:])
    result = []
    for c_curr in curr:
        for c_others in others:
            result.append([c_curr] + c_others)
    return result


def substitution_score(msg, alphabet, ngram_size):
    eng_frequency = parse_ngram_stats(alphabet, ngram_size)

    def memoize(f):
        memo = {}

        def helper(x):
            x_key = str(x)
            if x_key not in memo:
                memo[x_key] = f(x)
            return memo[x_key]

        return helper

    def substitution_score_bind(individual):
        decoded_msg = substitution_cipher(msg, [dict(zip(substitution, alphabet)) for substitution in individual])
        decoded_msg = ngrams(decoded_msg, ngram_size)
        ngrams_frequency = calculate_frequency_norm(decoded_msg)

        score = 0
        for ngram in ngrams_frequency:
            score += eng_frequency.get(ngram, 0) * ngrams_frequency[ngram]

        return score

    return memoize(substitution_score_bind)


def init_chromosome(gens):
    return random.sample(gens, len(gens))


def init_population(gens, number_of_chromosomes, size):
    return [[init_chromosome(gens) for _ in range(size)] for _ in range(number_of_chromosomes)]


def natural_selection(population, fitness):
    return [{'score': fitness(individual), 'key': individual} for individual in population]


def evolution(population):
    population = sorted(population, key=lambda ind: ind['score'], reverse=True)
    best_size = len(population) // 3
    return population[:best_size], population[best_size:]


def intercourse(gens, crossover_coefficient, x, y):
    chromosome_size = len(gens)
    x_indexes = random.sample(range(chromosome_size), k=int(crossover_coefficient * chromosome_size))

    chromosome_x = list(map(lambda val: val[1] if val[0] in x_indexes else None, enumerate(x)))
    chromosome_y = list(
        map(lambda val: None if val[0] in x_indexes or val[1] in chromosome_x else val[1], enumerate(y)))

    chromosome = [y_gens if x_gens is None else x_gens for x_gens, y_gens in zip(chromosome_x, chromosome_y)]

    def filter_gens(g):
        return g not in chromosome

    remaining_gens = list(filter(filter_gens, gens))
    random.shuffle(remaining_gens)

    chromosome = list(map(lambda val: remaining_gens.pop() if val is None else val, chromosome))

    return chromosome


def mutation(population, mutation_probability):
    new_population = []
    for ind in population:
        if random.random() < mutation_probability:
            gen1 = random.randrange(0, len(ind))
            gen2 = random.randrange(0, len(ind))
            ind[gen1], ind[gen2] = ind[gen2], ind[gen1]
        new_population.append(ind)
    return new_population


def main():
    KEY_LEN = key_len(encoded)
    print('Key length: ' + str(KEY_LEN))
    result = []
    calc_score = substitution_score(encoded, ALPHABET, NGRAMS_SIZE)
    intercourse_bind = partial(intercourse, ALPHABET, CROSSOVER_COEFFICIENT)
    # Initial population
    population = init_population(ALPHABET, KEY_LEN, POPULATION_SIZE)
    for gen in range(NUMBER_OF_GENERATIONS):
        if (gen + 1) % 50 == 0:
            print("Generation " + str(gen + 1))

        new_population = []
        local_best = []
        for index in range(KEY_LEN):
            test_population = [c if i == index else [c[0]] for i, c in enumerate(population)]
            test_population = permutations(test_population)[:-1]

            # Natural selection
            test_population = natural_selection(test_population, calc_score)
            best, others = evolution(test_population)
            best, others = [obj['key'][index] for obj in best], [obj['key'][index] for obj in others]

            local_best.append(best[:POPULATION_SIZE // 50])

            # Breeding
            parents = random.sample(others, len(others) // 2)
            random.shuffle(parents)

            children = []
            for x in best:
                y = parents.pop()
                children.append(intercourse_bind(x, y))
                children.append(intercourse_bind(y, x))

            test_population = best + children
            test_population += [init_chromosome(ALPHABET) for _ in range(POPULATION_SIZE - len(test_population))]

            # Mutation
            test_population = mutation(test_population, MUTATION_PROBABILITY)
            new_population.append(test_population)

        population = new_population

        local_best = permutations(local_best)[:-1]
        local_best = natural_selection(local_best, calc_score) + result
        local_best = sorted(local_best, key=lambda k: k['score'], reverse=True)
        temp = []
        for key in local_best:
            if len(temp) == (POPULATION_SIZE // 50):
                break
            if key in local_best:
                temp.append(key.copy())
        result = temp

    print("=" * 20 + " Finish " + "=" * 20)
    result = sorted(result, key=lambda ind: ind['score'], reverse=True)
    for i, key in enumerate(result):
        print("Key:" + str(i + 1))
        print("Fitness: " + str(key['score']))
        print("Substitution: [" + ",".join(["'" + "".join(s) + "'" for s in key['key']]) + "]")
        decoded_msg = substitution_cipher(encoded, [dict(zip(s, ALPHABET)) for s in key['key']])
        print("Decoded message: " + decoded_msg)


if __name__ == '__main__':
    import time

    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
