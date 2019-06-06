# bloody dependencies
import numpy as np
import pandas as pd

from brainfuck import run

ALPHABET = "><+-.[]" # intentionally ignore comma
CODESIZE = 64
MUTATION_RATE = 0.02 # probability of random change per letter
POPSIZE = 64
GENERATIONS = 4096

# produce a random code
def _bfcode():
    bfcode = np.random.choice(list(ALPHABET), CODESIZE)
    bfcode = "".join(bfcode)
    return bfcode

# mutate a piece of code
def _mutate(bfcode):
    lexicon = list(ALPHABET)
    mutate = np.random.choice([True, False], size = len(bfcode), p = [MUTATION_RATE, 1-MUTATION_RATE])
    bfcode = np.array(list(bfcode))
    bfcode[mutate] = np.random.choice(lexicon, size = sum(mutate))
    bfcode = "".join(bfcode)
    return bfcode

# measure the fitness of an output
def _fitness(output):
    target = "hello"
    output = output.ljust(len(target), chr(0))
    fitness = sum([abs(ord(a) - ord(b)) for a,b in zip(output, target)])
    fitness += len(output) - len(target) # penalize overrun
    return fitness

# cross a child from two parents
def _cross(parent1, parent2):
    crossover_point = np.random.randint(0, CODESIZE)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# select and breed pairs of parents based on fitness scores
def _select_and_breed(data):

    # selection probability
    prob = data.score.values
    prob -= (min(prob) - 1) # shift
    prob = 1./prob # invert
    prob /= prob.sum() # normalize

    # select
    individuals = data.bfcode.values
    select1 = np.random.choice(individuals, POPSIZE, p = prob)
    select2 = np.random.choice(individuals, POPSIZE, p = prob)

    # breed
    children = [ _cross(parent1, parent2) for parent1, parent2 in zip(select1, select2) ]
    return children

# run code
def _run(bfcode):
    try:
        output = run(bfcode)
        return output
    except Exception as e:
        return None

# start here
def main():

    # randomize initial population
    bfcode = [ _bfcode() for _ in range(POPSIZE) ]
    data = pd.DataFrame(dict(bfcode = bfcode))

    # loop over generations
    metadata = []
    for gen in range(GENERATIONS):

        # run all individual codes
        data["output"] = [ _run(bfcode) for bfcode in data.bfcode ]

        # filter survivors
        data["error"] = data.output.isnull()
        data = data[~data.error]

        # (optional) filter no output
        data = data[data.output.str.len() > 0]

        # nothing survived
        if len(data) <= 0:
            print("Extinction level event. Restarting...")
            bfcode = [ _bfcode() for _ in range(POPSIZE) ]
            data = pd.DataFrame(dict(bfcode = bfcode))
            continue

        # fitness scores
        data["score"] = [ _fitness(output) for output in data.output ]

        # best score
        winner = data.loc[data.score.idxmin()]
        print(gen, winner.bfcode, winner.score, winner.output)
        metadata.append(tuple(winner))
        if winner.score <= 0:
            print("\n", winner.output)
            break

        # reproduction
        children = _select_and_breed(data)

        # mutation
        children = [ _mutate(child) for child in children ]

        # next generation
        data = pd.DataFrame(dict(bfcode = children))

    # done
    cols = ['bfcode', 'output', 'error', 'score']
    metadata = pd.DataFrame(metadata, columns = cols)

    # analyze
    import matplotlib.pyplot as plt
    plt.plot(metadata.index, metadata.score)
    plt.show()

if __name__ == "__main__": main()
