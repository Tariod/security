import random
import string

from calculate_frequency import calculate_frequency
from ngrams import ngrams
from substitution_cipher import substitution_cipher

encoded = 'EFFPQLEKVTVPCPYFLMVHQLUEWCNVWFYGHYTCETHQEKLPVMSAKSPVPAPVYWMVHQLUSPQLYWLASLFVWPQLMVHQLUPLRPSQLULQESPBLWPCS' \
          'VRVWFLHLWFLWPUEWFYOTCMQYSLWOYWYETHQEKLPVMSAKSPVPAPVYWHEPPLUWSGYULEMQTLPPLUGUYOLWDTVSQETHQEKLPVPVSMTLEUPQE' \
          'PCYAMEWWYTYWDLUULTCYWPQLSEOLSVOHTLUYAPVWLYGDALSSVWDPQLNLCKCLRQEASPVILSLEUMQBQVMQCYAHUYKEKTCASLFPYFLMVHQLU' \
          'PQLHULIVYASHEUEDUEHQBVTTPQLVWFLRYGMYVWMVFLWMLSPVTTBYUNESESADDLSPVYWCYAMEWPUCPYFVIVFLPQLOLSSEDLVWHEUPSKCPQ' \
          'LWAOKLUYGMQEUEMPLUSVWENLCEWFEHHTCGULXALWMCEWETCSVSPYLEMQYGPQLOMEWCYAGVWFEBECPYASLQVDQLUYUFLUGULXALWMCSPEP' \
          'VSPVMSBVPQPQVSPCHLYGMVHQLUPQLWLRPOEDVMETBYUFBVTTPENLPYPQLWLRPTEKLWZYCKVPTCSTESQPQULLGYAUMEHVPETFWMEHVPETB' \
          'ZMEHVPETB'

ALPHABET = [letter for letter in string.ascii_uppercase]
POPULATION_SIZE = 5
NUMBER_OF_GENERATIONS = 1


def init_individual(gens):
    return random.sample(gens, len(gens))


def init_population(gens, size):
    return [init_individual(gens) for _ in range(size)]


def natural_selection(population, fitness):
    return [[individual, fitness(individual)] for individual in population]


def substitution_score(msg, alphabet):
    def substitution_score_bind(substitution):
        decoded_msg = substitution_cipher(msg, dict(zip(substitution, alphabet)))
        decoded_msg = ngrams(decoded_msg, 1)
        ngrams_frequency = calculate_frequency(decoded_msg)
        return ngrams_frequency

    return substitution_score_bind


def main():
    # Initial population
    population = init_population(ALPHABET, POPULATION_SIZE)
    for _ in range(NUMBER_OF_GENERATIONS):
        # Natural selection
        scores = natural_selection(population, substitution_score(encoded, ALPHABET))
        print(scores)


if __name__ == '__main__':
    main()
# Breeding
# Mutation
# New Population
