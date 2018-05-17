import genealogy as G
import graphviz as GV
import genealogy_analyzer as GA
import sys
import json

def CF(cs): return 4 if cs[0] else 1
def F(agent, ref_gen_ind, A):
    return agent.absolute_fitness + (ref_gen_ind - agent.gen_ind) ** A

experimentname = "default"

if len(sys.argv) != 3:
    print("[!] This progam accepts 2 arguments, the path to a configuratory json file, and the path to an output file.")
    quit()

json_filepath = sys.argv[1]
output_filepath = sys.argv[2]
with open(json_filepath, "r") as f:
    data = json.load(f)
json_genparams = data["genealogy-parameters"]

gen_params = {
    "name" : experimentname,
    "M" : lambda m, i: json_genparams["M"],
    "N" : json_genparams["N"],
    "P" : lambda i: json_genparams["P"],
    "A" : json_genparams["A"],
    "C" : json_genparams["C"],
    "G" : json_genparams["G"],
    "T" : json_genparams["T"],
    "CF" : CF,
    "F"  : F,
    "init_distribution" : json_genparams["init_distribution"],
    "replacement" : False
}

analyzer_params = {}

meta = {
    "X-name": "Generation Index",
    "Y-name": "CS Distribution (%)",
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
result.figSave(output_filepath)
