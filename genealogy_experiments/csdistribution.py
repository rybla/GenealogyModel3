import genealogy_lib.genealogy as G
import genealogy_lib.graphviz as GV
import genealogy_lib.genealogy_analyzer as GA

experimentname = "csdistribution"

def CF(cs): return 4 if cs[0] else 1
def F(agent, ref_gen_ind, A):
    return agent.absolute_fitness + (ref_gen_ind - agent.gen_ind) ** A

gen_params = {
    "name" : experimentname,
    "M" : lambda m, i: 10,
    "N" : 10,
    "P" : lambda i: 1,
    "A" : 0,
    "C" : 0,
    "G" : 1,
    "T" : 1,
    "CF" : CF,
    "F"  : F,
    "init_distribution" : [0.5],
    "replacement" : False
}

analyzer_params = {}

metadata = {
    "title": "CS Distribution",
    "dependent": "CS Distribution",
    "variable": "Generation Index",
    "variable-space": range(10),
    "iterations": 100,
    "labels": [ str(i) for i in range(2**gen_params["T"])]
}

analyzer = GA.GenealogyAnalyzer(analyzer_params, gen_params)
analyzer.initResult(experimentname, metadata)
analyzer.analyzeCSDistributions(experimentname)

result = analyzer.getResult(experimentname)
result.setFigParameter("legend",True)
result.showFig()
