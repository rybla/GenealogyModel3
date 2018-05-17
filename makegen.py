import genealogy as G
import graphviz as GV
import json
import sys

# import data

if len(sys.argv) != 2:
    print("[!] This progam accepts 1 argument, the path to a configuratory json file.")
    quit()

filepath = sys.argv[1]
data = ""
with open(filepath, "r") as f:
    data = json.load(f)
json_genparams = data["genealogy-parameters"]

# parameters

name = json_genparams["name"]

M_ = json_genparams["M"]
N  = json_genparams["N"]
P_ = json_genparams["P"]
V  = json_genparams["V"]

def M(prev_m, gen_ind): return M_
def P(gen_ind): return P_
def CF(cs): return V[0] if cs[0] else V[1]
def F(agent, ref_gen_ind, A): return (agent.absolute_fitness+(ref_gen_ind - agent.gen_ind) ** A)

genealogy_parameters = {
    "name" : name,
    "M" : M,
    "N" : N,
    "P" : P,
    "A" : json_genparams["A"],
    "C" : json_genparams["C"],
    "G" : json_genparams["G"],
    "T" : 1, # json_genparams["T"],
    "CF" : CF,
    "F"  : F,
    "init_distribution" : json_genparams["init-distribution"],
    "replacement" : json_genparams["replacement"]
}

graphviz_parameters = data["graphviz-parameters"]
graphviz_parameters["cs-to-color"] = lambda cs: "#FF0000" if cs[0] else "#0000FF"

# Genealogy
genea = G.Genealogy(genealogy_parameters)
genea.generate()

# Graph
graph = GV.Graph(genea,graphviz_parameters)
graph.generate()
graph.makeDot("makegen_output/"+name)
if data["graphviz-parameters"]["pdf"]:
    graph.makePDF("makegen_output/"+name)

if data["graphviz-parameters"]["svg"]:
    graph.makeSVG("makegen_output/"+name)
