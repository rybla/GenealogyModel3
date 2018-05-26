import random
import numpy as np
import math
import copy
import pickle
from genealogy_lib import binary_utils
from genealogy_lib.utilities import *
from genealogy_lib.genealogy_defaults import *
random.seed()


# ----------------
# | Genealogy
# ----------------
# Notes:
#

class Genealogy:

    def __init__(self, params=default_genealogy_parameters):
        self.parameters = params
        self.population = None
        self.distribution = np.zeros([2**self.parameters["T"],self.parameters["N"]], int)
        self.generation_sizes = np.empty(self.parameters["N"],int)
        self.blank_cs = np.zeros(self.parameters["T"],bool)

    def setParameters(self, params):
        for k,v in params.items():
            self.parameters[k] = v

    def setParameter(self, k, v):
        self.parameters[k] = v

    def generate(self):
        # init arrays for population
        # and generation sizes
        self.initPopulation()
        # fill agents in first generation according to
        # parameters["init_distribution"]
        self.fillFirstGeneration()
        # fill agents in each subsequent generation
        for i in range(1,self.parameters["N"]):
            self.fillGeneration(i)

    def initPopulation(self):
        # for each generation
        prev_m = 0
        total = 0
        for i in range(self.parameters["N"]):
            m = self.parameters["M"](prev_m, i)
            prev_m = m
            self.generation_sizes[i] = m
            total += m
        self.population = np.empty(total,object)

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
            self.toAbsoluteIndex(gen_ind,0):
            self.toAbsoluteIndex(gen_ind+1,0)]

    def getAllGenerations(self):
        return self.getGenerationRange(0,self.parameters["N"])

    def getGenerationRange(self, gen_ind_s, gen_ind_e):
        return self.population[
            self.toAbsoluteIndex(gen_ind_s,0):
            self.toAbsoluteIndex(gen_ind_e,0)]

    def updateDistributionEntry(self, agent):
        self.distribution[agent.cs_ind][agent.gen_ind] += 1

    def getGenerationSize(self, gen_ind):
        return self.generation_sizes[gen_ind]

    def initAgent(self, gen_ind, agent_ind):
        a = Agent(self.blank_cs, gen_ind, agent_ind)
        self.population[self.toAbsoluteIndex(gen_ind, agent_ind)] = a
        return a

    def getAgent(self, gen_ind, agent_ind):
        return self.population[self.toAbsoluteIndex(gen_ind, agent_ind)]

    def getAgentFitness(self, ref_gen_ind, gen_ind, agent_ind):
        agent = self.getAgent(gen_ind, agent_ind)
        return ( agent.getCharFitness() ** self.parameters["G"]
               * (1+agent.getChildrenCount())    ** self.parameters["C"]
               * (ref_gen_ind - gen_ind)     ** self.parameters["A"] )

    def makeCSIterator(self):
        return binary_utils.makeBinaryIterator(len(self.blank_cs)**2)

    def fillFirstGeneration(self):
        generation_size = self.generation_sizes[0]
        init_distribution = self.parameters["init_distribution"]
        # initialize agents in first generation
        for agent_ind in range(generation_size):
            self.initAgent(0,agent_ind)
        # set agents' character sets
        for char_ind in range(self.parameters["T"]):
            count = math.floor(init_distribution[char_ind] * generation_size)
            picks = np.random.choice(self.getGeneration(0),size=count,replace=False)
            # picks = random.sample(self.getGeneration(0),count)
            for a in picks: a.setChar(char_ind, True)
        # update agents'
        for a in self.getGeneration(0):
            a.updateCharFitnessFactor(self.parameters["CF"], self.parameters["G"])
            a.updateAbsoluteFitness(self.parameters["C"])
            a.updateCSIndex()
            self.updateDistributionEntry(a)

    def fillGeneration(self, gen_ind):
        generation_size = self.getGenerationSize(gen_ind)
        # all agents before this generation
        previous_agents = self.getGenerationRange(0,gen_ind)
        # fill all this generation's agents
        for agent_ind in range(generation_size):
            child = self.initAgent(gen_ind, agent_ind)
            self.getAgent(gen_ind, agent_ind)
            parents = self.chooseParents(previous_agents, gen_ind)
            for parent in parents: parent.addChild(self.parameters["C"], child)
            self.inheritCS(child, parents)
            self.updateDistributionEntry(child)

    def chooseParents(self, previous_agents, ref_gen_ind):
        # calculate the fitnesses of the previous_agents
        previous_agents_length = len(previous_agents)
        fitnesses = np.empty(previous_agents_length,float)
        for i in range(previous_agents_length):
            fitnesses[i] = previous_agents[i].getFitness(
                self.parameters["F"], ref_gen_ind, self.parameters["A"])
        fitnesses = normalize(fitnesses)

        size = self.parameters["P"](ref_gen_ind)
        # if not replacement, can't have too many parents
        if not self.parameters["replacement"]:
            size = min(size,previous_agents_length)

        return np.random.choice(
            previous_agents,
            p       = fitnesses,
            size    = size,
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
                                * (1+self.getChildrenCount())    ** C )
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
