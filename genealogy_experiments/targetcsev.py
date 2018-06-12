import genealogy_lib.genealogy as G
import genealogy_lib.graphviz as GV
import genealogy_lib.genealogy_analyzer as GA

experimentname = "experiemnt_targetcsev"

values = [
    0.10, 0.01,
    0.01, 1.00
]

init_distribution = [
    0.25,0.25,0.25,0.25
]

def CF(cs):
    cs = [ 1 if c else 0 for c in cs ]
    return values[ cs[1]*2 + cs[0] ]

def F(agent, ref_gen_ind, A):
    return agent.absolute_fitness * (ref_gen_ind - agent.gen_ind) ** A

gen_params = {
    "name" : experimentname,
    
    "M" : lambda m, i: 100,

    "A" : 0,
    "C" : 0,
    "G" : 1,
    
    "T" : 2,
    "CF" : CF,
    "F"  : F,
    # "init_distribution" : [0.25,0.25,0.25,0.25],
    "init_distribution": init_distribution,
    "replacement" : False
}

analyzer_params = {}

targetcs_ind = 3

meta = {
    "X-name"     : "Parent Number",
    "X-range"    : [i for i in range(1,50,2)],
    "Y-name"     : "Evolution Rate",
    "Z-names"    : [ "CS#"+str(targetcs_ind)  ],
    "Z-size"     : 1,
    "I-value"    : targetcs_ind,
    "iterations" : 10,
}

analyzer = GA.GenealogyAnalyzer(analyzer_params, gen_params)
analyzer.initResult(experimentname, meta)
analyzer.analyzeTargetCSEV(experimentname)

result = analyzer.getResult(experimentname)
result.setFigParameter("title", "Evolution Rate of CS#"+str(targetcs_ind))
result.setFigParameter("legend",True)
result.figPlot()
result.figShow()
result.figSave("tests/"+experimentname+".png")
