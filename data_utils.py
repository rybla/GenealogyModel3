import math
import numpy as np

def normalize(data_list):
    m = max(data_list)
    for i in range(len(data_list)):
        data_list[i] /= m
    return data_list