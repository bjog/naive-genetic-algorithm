# Bhavish Jogeeah 2019-2020
# Naive Genetic Algorithm

import random

MAX_GENERATIONS = 1000
TARGET_VALUE = "11111111"
TARGET_GENERATION_FITNESS = 0.9
GENERATION_SIZE = 10
MUTATION_CHANCE = 0.2
PROPAGATION_CHANCE = 0.8

def fitness(x):
    score = 0.0
    for c in x:
        if c == "1":
            score += 1/len(TARGET_VALUE)
    return score

def initialise():
    generation = []
    for i in range(GENERATION_SIZE):
        x = ""
        for j in range(0,len(TARGET_VALUE)):
            if (random.random() > 0.5):
                x += "1"
            else:
                x += "0"
        generation.append(x)
    return generation

def mutate(x):
    m = ""
    for c in x:
        if(random.random() <= MUTATION_CHANCE):
            if c == "1":
                m += "0"
            else:
                m += "1"
        else:
            m += c
    return m

def reproduce(p,q):
    r = ""
    for i in range(0,len(TARGET_VALUE)):
        if(p[i] == q[i]):
            if(random.random() <= PROPAGATION_CHANCE):
                r += p[i]
            else:
                if random.random() <= 0.5:
                    r += "1"
                else:
                    r += "0"
        else:
            if random.random() <= 0.5:
                r += "1"
            else:
                r += "0"
    return r

# Use fitness as reproduction chance
def compatible(p,q):
    avgFitness = (p + q)/2
    if(random.random() <= avgFitness):
        return 1
    else:
        return 0

def select_parents(population, fitnesses):
    parents = []
    for f in fitnesses:
        fList = [f for i in range(len(fitnesses))]
        parents.append(list(map(compatible, fList, fitnesses)))

    # Remove duplicates in parents matrix
    for y in range(len(population)):
        for x in range(y + 1):
            parents[y][x] = 0

    return parents

def select_survivors(population, fitnesses):
    ranks = rank(fitnesses)
    survivors = []

    for i in range(len(population)):
        if(ranks[i] >= (len(population) - GENERATION_SIZE)):
            survivors.append(population[i])
    return survivors

def rank(fitnesses):
    indices = list(range(len(fitnesses)))
    indices.sort(key=lambda x: fitnesses[x])
    ranks = [0] * len(indices)
    for i, x in enumerate(indices):
        ranks[x] = i
    return ranks

def generate_offspring(population, parents):
    offspring = []
    for y in range(len(population)):
        for x in range(len(population)):
            if(parents[y][x] == 1):
                offspring.append(reproduce(population[x],population[y])) 
    return offspring

def main():
    population = initialise()
    print(population)
    
    for i in range(MAX_GENERATIONS):
        populationScores = list(map(fitness,population))
        print("Generation:{0}\tSize:{1}\tAvg.Fitness:{2}".format(i, len(population), sum(populationScores)/len(population)))
        
        parents = select_parents(population,populationScores)

        offspring = generate_offspring(population,parents)
        mutatedOffspring = list(map(mutate,offspring))

        offspringScores = list(map(fitness, mutatedOffspring))
        survivingOffspring = select_survivors( mutatedOffspring, offspringScores)

        population = survivingOffspring

    print("Generation:{0}\tSize:{1}\tAvg.Fitness:{2}".format(i + 1, len(population), sum(list(map(fitness,population)))/len(population)))
    print(population)

if __name__ == "__main__":
    main()