import data_utils
import genealogy as G
import graphviz as GV

from figure_defaults import default_fig_parameters
from genealogy_defaults import default_genealogy_parameters
from genealogy_analyzer_defaults import default_genealogy_analyzer_parameters

import matplotlib.pyplot as plt
import copy
import math
import numpy as np
from tqdm import tqdm

class GenealogyAnalyzer:

    def __init__(self, params, gen_params):
        self.parameters = params
        self.gen_params = gen_params
        self.results = {}

    def setParameters(self, params):
        for k,v in params.items():
            self.parameters[k] = v

    def setParameter(self, k, v):
        self.parameters[k] = v

    def initResult(self, resultname, metadata):
        self.results[resultname] = Result(resultname, metadata)

    def getResult(self, resultname):
        return self.results[resultname]

    def analyzeCSDistributions(self, resultname):
        result = self.getResult(resultname)
        iterations = result.metadata["iterations"]
        raw = [ # [char_ind][gen_ind] -> array with entry for each iteration
            [ [] for _ in range(self.gen_params["N"]) ]
                for _ in range(2**self.gen_params["T"]) ] 
        avg = [] # [char_ind][gen_ind] -> average
        # std = [] # [char_ind][gen_ind] -> standard deviation

        print("running iterations...")
        for i in tqdm(range(iterations)):
            g = G.Genealogy(self.gen_params)
            g.generate()
            d = g.getDistribution()
            for cs_ind in range(len(d)):
                d_cs = d[cs_ind]
                for gen_ind in range(len(d_cs)):
                    raw_cs_gen = raw[cs_ind][gen_ind]
                    if gen_ind == 0: raw_cs_gen.append(d_cs[gen_ind])
                    else:            raw_cs_gen.append(d_cs[gen_ind] + d_cs[gen_ind-1])

        for cs_ind in range(len(raw)):
            avg.append([])
            # std.append([])
            for gen_ind in range(len(raw[cs_ind])):
                avg[cs_ind].append(None)
                # std[cs_ind].append(None)
                avg[cs_ind][gen_ind] = np.mean(raw[cs_ind][gen_ind])
                # std[cs_ind][gen_ind] = np.std(raw[cs_ind][gen_ind])

        for avg_cs in avg:
            result.addData(avg_cs)
        
class Result:

    def __init__(self, name, metadata):
        self.name = name
        self.data = []
        self.metadata = metadata
        self.fig_parameters = default_fig_parameters

    def addData(self, data):
        self.data.append(data)

    def setFigParameters(self, params):
        for k,v in params.items():
            self.fig_parameters[k] = v

    def setFigParameter(self,k,v):
        self.fig_parameters[k] = v

    def showFig(self):
        fp = self.fig_parameters
        plt.figure(figsize=fp["figsize"])
        plt.title(self.metadata["title"])
        if fp["legend"]: plt.legend()
        plt.ylabel(self.metadata["dependent"])
        plt.xlabel(self.metadata["variable"])

        for i in range(len(self.data)):
            color = None
            if "colors" in fp: color = fp["colors"][i%len(fp["colors"])]
            plt.plot(
                self.metadata["variable-space"],
                self.data[i],
                fp["point"],
                label = self.metadata["labels"][i],
                c = color
            )
        plt.plot()
        plt.show()


    def saveFig(self):
        pass