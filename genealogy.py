import random
import numpy as np
import math
import copy
import pickle
import binary_utils
from utilities import *
from genealogy_defaults import *
random.seed()


# ----------------
# | Genealogy
# ----------------
# Notes:
#   'make-' functions will return objects
#   'add-' functions will not return objects, instead adding them to internal ledger
#

class Genealogy:

    population = []
    generation_sizes = []

    def __init__(self, params=default_genealogy_parameters):
        self.parameters = params
        self.population = []
        self.distribution = [
            [0 for i in range(self.parameters["N"])]
            for i in range(2**self.parameters["T"]) ]
        self.generation_sizes = []
        self.blank_cs = [ False for i in range(self.parameters["T"]) ]

    def setParameters(self, params):
        for k,v in params.items():
            self.parameters[k] = v

    def setParameter(self, k, v):
        self.parameters[k] = v

    def generate(self):
        # create blank genealogy
        self.addAllBlankAgents()
        # fill agents in first generation according to
        # parameters["init_distribution"]
        self.fillFirstGeneration()
        # fill agents in each subsequent generation
        for i in range(1,self.parameters["N"]):
            self.fillGeneration(i)

    def write(genealogy, name):
        with open(name+".rawgen", "wb+") as file:
            pickle.dump(genealogy, file, pickle.HIGHEST_PROTOCOL)

    def read(name):
        with open(name+".rawgen", "rb+") as file:
            return pickle.load(file)

    def addAllBlankAgents(self):
        # for each generation
        prev_m = 0
        for i in range(self.parameters["N"]):
            m = self.parameters["M"](prev_m, i)
            prev_m = m
            self.generation_sizes.append(m)
            # for each agent in generation
            for j in range(m):
                self.population.append( Agent(self.blank_cs, i,j) )

    def toAbsoluteIndex(self, gen_ind, agent_ind):
        ind = 0
        for i in range(gen_ind): ind += self.getGenerationSize(i)
        return ind + agent_ind

    def getPopulation(self):
        return self.population

    def getDistribution(self): # [cs_ind][gen_ind]
        return self.distribution

    def getGeneration(self, gen_ind):
        return self.population[
            self.toAbsoluteIndex(gen_ind,0):self.toAbsoluteIndex(gen_ind+1,0)]

    def getAllGenerations(self):
        return self.getGenerationRange(0,self.parameters["N"])

    def getGenerationRange(self, gen_ind_s, gen_ind_e):
        return self.population[
            self.toAbsoluteIndex(gen_ind_s,0):self.toAbsoluteIndex(gen_ind_e,0)]

    def updateDistributionEntry(self, agent):
        self.distribution[agent.cs_ind][agent.gen_ind] += 1

    def getGenerationSize(self, gen_ind):
        return self.generation_sizes[gen_ind]

    def getAgent(self, gen_ind, agent_ind):
        return self.population[self.toAbsoluteIndex(gen_ind, agent_ind)]

    def getAgentFitness(self, ref_gen_ind, gen_ind, agent_ind):
        agent = self.getAgent(gen_ind, agent_ind)
        return ( agent.getCharFitness() ** self.parameters["G"]
               + agent.getChildrenCount()    ** self.parameters["C"]
               + (ref_gen_ind - gen_ind)     ** self.parameters["A"] )

    def makeCSIterator(self):
        return binary_utils.makeBinaryIterator(len(self.blank_cs)**2)

    def fillFirstGeneration(self):
        generation_size = self.generation_sizes[0]
        init_distribution = self.parameters["init_distribution"]
        for char_ind in range(self.parameters["T"]):
            count = math.floor(init_distribution[char_ind] * generation_size)
            picks = random.sample(self.getGeneration(0),count)
            for a in picks: a.setChar(char_ind, True)
        for a in self.getGeneration(0):
            a.updateCharFitnessFactor(self.parameters["CF"], self.parameters["G"])
            a.updateAbsoluteFitness(self.parameters["C"])
            a.updateCSIndex()
            self.updateDistributionEntry(a)
            # print(a,a.getCS())

    def fillGeneration(self, gen_ind):
        generation_size = self.getGenerationSize(gen_ind)
        previous_agents = self.getGenerationRange(0,gen_ind) # all agents before this generation

        for agent_ind in range(generation_size):
            child = self.getAgent(gen_ind, agent_ind)
            parents = self.chooseParents(previous_agents, gen_ind)
            for parent in parents: parent.addChild(self.parameters["C"], child)
            self.inheritCS(child, parents)
            self.updateDistributionEntry(child)

    def chooseParents(self, previous_agents, ref_gen_ind):
        # with replacement
        if self.parameters["replacement"]:
            fitnesses = [ a.getFitness(self.parameters["F"], ref_gen_ind, self.parameters["A"]) for a in previous_agents ]
            fitnesses = normalize(fitnesses)
            return np.random.choice(
                previous_agents,
                p    = fitnesses,
                size = self.parameters["P"](ref_gen_ind))

        # without replacement
        else:
            previous_agents_count = 0
            fitnesses = []
            for a in previous_agents:
                fitnesses.append(a.getFitness(self.parameters["F"], ref_gen_ind, self.parameters["A"]))
                previous_agents_count += 1
            fitnesses = normalize(fitnesses)
            parents_count = min(self.parameters["P"](ref_gen_ind),previous_agents_count)
            return np.random.choice(
                previous_agents,
                p       = fitnesses,
                size    = parents_count,
                replace = self.parameters["replacement"])

    def inheritCS(self, child, parents):
        parents_count = len(parents)
        for i in range(self.parameters["T"]):
            pick = parents[random.randint(0,parents_count-1)]
            child.setChar(i, pick.getChar(i))
        child.updateCSIndex()
        child.updateCharFitnessFactor(self.parameters["CF"], self.parameters["G"])
        child.updateAbsoluteFitness(self.parameters["C"])


# ----------------
# | Agent
# ----------------
# Notes:
#

class Agent:

    def __init__(self, blank_cs, gen_ind, ind):
        self.children_count = 0
        self.children_inds = []
        self.char_fitness_factor = None
        self.absolute_fitness = None
        self.gen_ind = gen_ind
        self.agent_ind = ind
        self.cs = copy.copy(blank_cs)
        self.cs_ind = None

    def getChildrenCount(self): return self.children_count
    def getChildrenInds(self): return self.children_inds
    def addChild(self, C, child):
        self.children_inds.append([child.gen_ind,child.agent_ind])
        self.children_count += 1
        self.updateAbsoluteFitness(C)

    def getCS(self): return self.cs
    def getChar(self, char_ind): return self.cs[char_ind]
    def setCS(self, cs):
        self.cs = cs
        self.cs_ind = binary_utils.convertBinaryArrayToDecimal(self.cs)
    def setChar(self, char_ind, char_value):
        self.cs[char_ind] = char_value

    # does account for G (char fitness exponent)
    def getCharFitnessFactor(self): return self.char_fitness_factor

    def getFitness(self, F, ref_gen_ind, A): return F(self, ref_gen_ind, A)

    def updateAbsoluteFitness(self, C):
        self.absolute_fitness = ( self.getCharFitnessFactor()
                                + self.getChildrenCount()    ** C )
    def getAbsoluteFitness(self): return self.absolute_fitness

    def updateCharFitnessFactor(self, CF, G):
        self.char_fitness_factor = CF(self.cs) ** G

    def updateCSIndex(self):
        self.cs_ind = binary_utils.convertBinaryArrayToDecimal(self.cs)

    def tostring(self):
        return (
            "[ (" + str(self.gen_ind)+
            ","   + str(self.agent_ind)+") : "+
            str(self.getAbsoluteFitness())+" ]")

    __str__ = tostring
    __repr__ = tostring