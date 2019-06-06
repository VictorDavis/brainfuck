# bloody dependencies
import numpy as np

from brainfuck import run

ALPHABET = "><+-.[]" # intentionally ignore comma
CODESIZE = 40
MUTATION_RATE = 0.05 # probability of random change per letter per generation
POPSIZE = 256
GENERATIONS = 1024

# produce a random code
def _code():
    code_ = np.random.choice(list(ALPHABET), CODESIZE)
    code_ = "".join(code_)
    return code_

# mutate a piece of code
def _mutate(code_):
    lexicon = list(ALPHABET)
    mutate = np.random.choice([True, False], size = len(code_), p = [MUTATION_RATE, 1-MUTATION_RATE])
    code_ = np.array(list(code_))
    code_[mutate] = np.random.choice(lexicon, size = sum(mutate))
    code_ = "".join(code_)
    return code_

# measure the fitness of an output
def _fitness(output):
    target = "@"
    fitness = sum([abs(ord(a) - ord(b)) for a,b in zip(output, target)])
    return fitness

# best fitness score
def _winner(scores):
    winner = min(scores, key=scores.get)
    return winner

# cross a child from two parents
def _cross(parent1, parent2):
    crossover_point = np.random.randint(0, CODESIZE)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# select and breed pairs of parents based on fitness scores
def _select_and_breed(scores):

    # selection probability
    prob = np.array(list(scores.values()))
    prob -= (min(prob) - 1) # shift
    prob = 1./prob # invert
    prob /= prob.sum() # normalize

    # select
    individuals = list(scores.keys())
    select1 = np.random.choice(individuals, POPSIZE, p = prob)
    select2 = np.random.choice(individuals, POPSIZE, p = prob)

    # breed
    children = [ _cross(parent1, parent2) for parent1, parent2 in zip(select1, select2) ]
    return children

# send a population of individuals into life's gaping maw
def _crucible(population):

    # filter out errors & empties
    errors, empties, successes, survivors = 0, 0, 0, {}
    for individual in population:
        try:
            output = run(individual)
            if len(output) > 0:
                survivors[individual] = output
                successes += 1
            else:
                empties += 1
        except Exception as e:
            errors += 1

    # # report/summary
    # print("\nResults:")
    # print("Errors:", errors)
    # print("Empties:", empties)
    # print("Successes:", successes)

    # return
    return survivors

# start here
def main():

    # randomize initial population
    population = [ _code() for _ in range(POPSIZE) ]

    # loop over generations
    bestscore = []
    for gen in range(GENERATIONS):

        # subject population to the crucible that is life
        survivors = _crucible(population)

        # nothing survived
        if len(survivors) <= 0:
            print("You have gone extinct. Rebooting...")
            population = [ _code() for _ in range(POPSIZE) ]
            continue

        # fitness scores
        scores = { individual:_fitness(output) for individual, output in survivors.items()}

        # best score
        winner = _winner(scores)
        score  = scores[winner]
        bestscore.append(score)
        output = survivors[winner]
        print(winner, gen, len(survivors), score, output)
        if score <= 0:
            break

        # reproduction
        children = _select_and_breed(scores)

        # mutation
        children = [ _mutate(child) for child in children ]

        # next generation
        population = children

if __name__ == "__main__": main()
