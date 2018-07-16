import pandas as pd
import numpy as np
import datetime as dt
import sys

import poloniex
import execution_model as em

def pick_random_time_period():
    pass

def construct_random_model(time_period)
    return False

def main():
    num_simulations = sys.argv[1]

    if type(num_simulations) != 'int':
        print('Second argument must be an integer')
    else:
        for i in range(num_simulations):
            try:
                time_period = pick_random_time_period()
                model = construct_random_model(time_period)
                model.execute()

