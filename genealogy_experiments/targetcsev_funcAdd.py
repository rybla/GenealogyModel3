import genealogy_lib.genealogy as G
import genealogy_lib.graphviz as GV
import genealogy_lib.genealogy_analyzer as GA

experimentname = "exp_targetcsev_funcAdd"

A,B = 10, 20

values = [
    1 , A,
    B , A+B ]

init_distribution = [ 0.25,0.25,0.25,0.25 ]

def CF(cs):
    csA, csB = cs[0], cs[1]
    i = 0
    if (not csA) and (not csB): i = 0
    elif csA and (not csB):     i = 1
    elif (not csA) and csB:     i = 2
    elif csA and csB:           i = 3
    return values[i]

def F(agent, ref_gen_ind, A):
    return agent.absolute_fitness * (ref_gen_ind - agent.gen_ind) ** A

gen_params = {
    "name" : experimentname,
    
    "M" : lambda m, i: 500,

    "A" : 0,
    "C" : 0,
    "G" : 1,
    
    "T" : 2,
    "CF" : CF,
    "F"  : F,
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
    "iterations" : 1000,
}

analyzer = GA.GenealogyAnalyzer(analyzer_params, gen_params)
analyzer.initResult(experimentname, meta)
analyzer.analyzeTargetCSEV(experimentname)

result = analyzer.getResult(experimentname)
result.setFigParameter("title", "Evolution Rate of CS#"+str(targetcs_ind)+" varying with Parent Number")
result.setFigParameter("legend",True)
result.figPlot()
result.figShow()
result.figSave("outputs/"+experimentname+str(meta["iterations"])+".png")
