def M(prev_m, gen_ind):
    return 10

def P(gen_ind):
    return 1

def CF(cs):
    if cs[0]: return 4
    else: return 1

def F(agent, ref_gen_ind, A):
    return (
        agent.absolute_fitness +
        (ref_gen_ind - agent.gen_ind) ** A
    )

default_genealogy_parameters = {

    "name" : "Untitled",
    
    "M" : M,                # Nat        : members per generations 
                            #               (function of previous m and generation index)
    
    "N" : 10,               # Nat         : number of generations
    
    "P" : P,                # Nat -> Nat  : parents per member
    
    "A" : 0,                # Float       : age exponent
    
    "C" : 0,                # Float       : popularity exponent
    
    "G" : 1,                # Float       : fitness exponent
    
    "T" : 1,                # Int         : number of character traits
    
    "CF" : CF,              # CS -> Flt   : character set fitness function

    "F"  : F,               # ... -> Flt  : fitness functions
    
    "init_distribution" :   # [Float]     : fraction of first generation having
        [0.5],              #               each character

    "replacement" : False   # Bool        : do choose with replacment
                            #               when selecting parents?
}