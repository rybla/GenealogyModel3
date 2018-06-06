import genealogy_lib.genealogy as G
import genealogy_lib.graphviz as GV
import genealogy_lib.genealogy_analyzer as GA

experimentname = "experiment_absolute-cs-distributions"

def CF(cs): return 4 if cs[0] else 1
def F(agent, ref_gen_ind, A):
    return agent.absolute_fitness + (ref_gen_ind - agent.gen_ind) ** A

gen_params = {
    "name" : experimentname,
    "M" : lambda m, i: 10,
    "N" : 5,
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

meta = {
    "X-name": "Generation Index",
    "Y-name": "CS Distribution",
    "Z-names": [ "CS#: " + str(i) for i in range(2**gen_params["T"])],
    "Z-size": 2**gen_params["T"],
    "iterations": 200,
}

analyzer = GA.GenealogyAnalyzer(analyzer_params, gen_params)
analyzer.initResult(experimentname, meta)
analyzer.analyzeAbsoluteCSDistributions(experimentname)

result = analyzer.getResult(experimentname)
result.setFigParameter("title", "Absolute CS Distribution evolution over Time")
result.setFigParameter("legend",True)
result.figPlot()
result.figShow()
