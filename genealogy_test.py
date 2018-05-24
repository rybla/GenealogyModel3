import genealogy_lib.genealogy as G
import genealogy_lib.graphviz as GV

# Knobs
NAME = "genealogy_test"
M = 20
N = 20
P = 2
V = [4,1]

def _M(prev_m, gen_ind): return M
def _P(gen_ind): return P
def CF(cs): return V[0] if cs[0] else V[1]
def F(agent, ref_gen_ind, A): return (agent.absolute_fitness*(ref_gen_ind - agent.gen_ind) ** A)

genealogy_parameters = {
    "name" : NAME,
    "M" : _M,                       # Nat         : members per generations (function of previous m and generation index)
    "N" : N,                        # Nat         : number of generations
    "P" : _P,                       # Nat -> Nat  : parents per member
    "A" : 0,                        # Float       : age exponent
    "C" : 0,                        # Float       : popularity exponent
    "G" : 1,                        # Float       : fitness exponent
    "T" : 1,                        # Int         : number of character traits (each is boolean)
    "CF" : CF,                      # CS -> Flt   : character set fitness function
    "F"  : F,                       # ... -> Flt  : fitness functions
    "init_distribution" : [0.5],    # [Float]     : fraction of first generation having each character
    "replacement" : False           # Bool        : do choose with replacment when selecting parents?
}

graphviz_parameters = {
    "graph-attributes" : [
        ("nodesep", "0.1"),
        ("ranksep", "1"),
        ("size", "5"),
        ("ratio", "fill")
    ],
    "node-attributes" : [
        ("style", "filled"),
        ("fontcolor", "white"),
        ("shape", "square"),
        ("width", "10"),
        ("height", "5"),
        ("fontsize", "20.0")
    ],
    "edge-attributes" : [ ("penwidth", "1") ],
    "cs-to-color" : (lambda cs: "#FF0000" if cs[0] else "#0000FF")
}

# Genealogy
genea = G.Genealogy(genealogy_parameters)
genea.generate()

# Graph
graph = GV.Graph(genea,graphviz_parameters)
graph.generate()
graph.makeDot("tests/"+NAME)
