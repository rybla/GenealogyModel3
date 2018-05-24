
def normalize(probs):
    prob_factor = 1.0 / sum(probs)
    return [prob_factor * p for p in probs]
