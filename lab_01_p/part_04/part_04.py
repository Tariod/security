import math
from functools import partial

import pandas as pd
import random
import string

from calculate_frequency import calculate_frequency
from ngrams import ngrams
from substitution_cipher import substitution_cipher

# ================ ALPHABET CONF ================
ALPHABET = string.ascii_uppercase
NGRAMS_SIZE = 3  # NGRAMS_SIZE > 1
NGRAMS_STAT = {string.ascii_uppercase: [None, 'trigrams_frequency.csv']}
# =================== GEN CONF ==================
POPULATION_SIZE = 200
NUMBER_OF_GENERATIONS = 600
CROSSOVER_COEFFICIENT = 0.6
MUTATION_PROBABILITY = 0.3

encoded = 'EFFPQLEKVTVPCPYFLMVHQLUEWCNVWFYGHYTCETHQEKLPVMSAKSPVPAPVYWMVHQLUSPQLYWLASLFVWPQLMVHQLUPLRPSQLULQESPBLWPCS' \
          'VRVWFLHLWFLWPUEWFYOTCMQYSLWOYWYETHQEKLPVMSAKSPVPAPVYWHEPPLUWSGYULEMQTLPPLUGUYOLWDTVSQETHQEKLPVPVSMTLEUPQE' \
          'PCYAMEWWYTYWDLUULTCYWPQLSEOLSVOHTLUYAPVWLYGDALSSVWDPQLNLCKCLRQEASPVILSLEUMQBQVMQCYAHUYKEKTCASLFPYFLMVHQLU' \
          'PQLHULIVYASHEUEDUEHQBVTTPQLVWFLRYGMYVWMVFLWMLSPVTTBYUNESESADDLSPVYWCYAMEWPUCPYFVIVFLPQLOLSSEDLVWHEUPSKCPQ' \
          'LWAOKLUYGMQEUEMPLUSVWENLCEWFEHHTCGULXALWMCEWETCSVSPYLEMQYGPQLOMEWCYAGVWFEBECPYASLQVDQLUYUFLUGULXALWMCSPEP' \
          'VSPVMSBVPQPQVSPCHLYGMVHQLUPQLWLRPOEDVMETBYUFBVTTPENLPYPQLWLRPTEKLWZYCKVPTCSTESQPQULLGYAUMEHVPETFWMEHVPETB' \
          'ZMEHVPETB'


def parse_ngram_stats(alphabet, ngrams_size):
    stat_filename = NGRAMS_STAT[alphabet][ngrams_size - 2]
    stats = pd.read_csv(stat_filename)
    stats['ngram'] = stats['ngram'].map(lambda ngram: tuple([s for s in ngram]))
    stats['frequency'] = stats['frequency'].map(lambda fr: math.log2(fr))
    stats = stats.set_index('ngram')
    return stats['frequency'].to_dict()


def substitution_score(msg, alphabet, ngram_size):
    eng_frequency = parse_ngram_stats(alphabet, ngram_size)

    def substitution_score_bind(substitution):
        decoded_msg = substitution_cipher(msg, dict(zip(substitution['alphabet'], alphabet)))
        decoded_msg = ngrams(decoded_msg, ngram_size)
        ngrams_frequency = calculate_frequency(decoded_msg)

        for ngram in ngrams_frequency:
            if substitution['score'] is None:
                substitution['score'] = 0
            substitution['score'] += eng_frequency.get(ngram, 0) * ngrams_frequency[ngram]

        return substitution

    return substitution_score_bind


def init_individual(gens):
    return random.sample(gens, len(gens))


def init_population(gens, size):
    return [{'alphabet': init_individual(gens), 'score': None} for _ in range(size)]


def natural_selection(population, fitness):
    return [fitness(individual) if individual['score'] is None else individual for individual in population]


def evolution(population):
    population = sorted(population, key=lambda ind: ind['score'], reverse=True)
    best_size = len(population) // 3
    return population[:best_size], population[best_size:]


def intercourse(gens, crossover_coefficient, x, y):
    chromosome_size = len(gens)
    x_indexes = random.sample(range(chromosome_size), k=int(crossover_coefficient * chromosome_size))

    chromosome_x = list(map(lambda val: val[1] if val[0] in x_indexes else None, enumerate(x['alphabet'])))
    chromosome_y = list(
        map(lambda val: None if val[0] in x_indexes or val[1] in chromosome_x else val[1], enumerate(y['alphabet'])))

    chromosome = [y_gens if x_gens is None else x_gens for x_gens, y_gens in zip(chromosome_x, chromosome_y)]

    def filter_gens(g):
        return g not in chromosome

    remaining_gens = list(filter(filter_gens, gens))
    random.shuffle(remaining_gens)

    chromosome = list(map(lambda val: remaining_gens.pop() if val is None else val, chromosome))

    return {'alphabet': chromosome, 'score': None}


def mutation(population, mutation_probability):
    new_population = []
    for ind in population:
        if random.random() < mutation_probability:
            ind['score'] = None
            gen1 = random.randrange(0, len(ind))
            gen2 = random.randrange(0, len(ind))
            ind['alphabet'][gen1], ind['alphabet'][gen2] = ind['alphabet'][gen2], ind['alphabet'][gen1]
        new_population.append(ind)
    return new_population


def main():
    best_keys = []
    calc_score = substitution_score(encoded, ALPHABET, NGRAMS_SIZE)
    intercourse_bind = partial(intercourse, ALPHABET, CROSSOVER_COEFFICIENT)
    # Initial population
    population = init_population(ALPHABET, POPULATION_SIZE)
    for gen in range(NUMBER_OF_GENERATIONS):
        if gen % 100 == 0: print("Generation " + str(gen))
        # Natural selection
        population = natural_selection(population, calc_score)
        best, others = evolution(population)

        best_keys.append(best[0].copy())
        # Breeding
        parents = random.sample(others, len(others) // 2)
        random.shuffle(parents)

        children = []
        for x in best:
            y = parents.pop()
            children.append(intercourse_bind(x, y))
            children.append(intercourse_bind(y, x))

        population = best + children
        population += init_population(ALPHABET, POPULATION_SIZE - len(population))

        # Mutation
        population = mutation(population, MUTATION_PROBABILITY)
    print("=" * 20 + " Finish " + "=" * 20)
    best_keys = sorted(best_keys, key=lambda ind: ind['score'], reverse=True)
    for i in range(5):
        key = best_keys[i]
        print("Key:" + str(i + 1))
        print("Fitness: " + str(key['score']))
        print("Substitution: " + ''.join(key['alphabet']))
        decoded_msg = substitution_cipher(encoded, dict(zip(key['alphabet'], ALPHABET)))
        print("Decoded message: " + decoded_msg)


if __name__ == '__main__':
    main()
