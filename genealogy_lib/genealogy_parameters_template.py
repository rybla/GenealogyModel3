def CF(cs): 4 if cs[0] else 1
def F(agent, ref_gen_ind, A):
    return agent.absolute_fitness + (ref_gen_ind - agent.gen_ind) ** A

gen_params = {
    "name" : "test",
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