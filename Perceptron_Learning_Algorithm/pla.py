#####
# Jinho Lee (jl5027)
# COMS 4701
# Prof. Ansaf Salleb-Aouissi
# pla.py
#####

import pandas as pd
import sys
import numpy as np
from plot_db import visualize_scatter

def predict(data, weights):
    predicted = np.dot(data, weights)

    return 1.0 if predicted >= 0.0 else -1.0

def train(data, weights, epochs=10, lr=0.2):
    df = pd.DataFrame(data)
    ar = []
    for epoch in range(epochs):
        for i in range(len(data)):
            error = data[i][-1] - predict(data[i][:-1], weights[:-1])
            for j in [0, 1]:
                weights[j] = weights[j] + (lr*error*data[i][j])
                ar.append(weights[j])
            ar.append(weights[len(weights)-1])

    weights_array = np.array(ar)
    weights_array = np.reshape(weights_array, (-1, 3))
    visualize_scatter(df, weights=weights, title="Final Epoch")

    return weights_array

def main():
    data_csv = pd.read_csv(sys.argv[1], header=None)
    data = np.array(data_csv)
    weights = [-0.5, 0.2, -50.0]
    weights_array = train(data, weights)
    df = pd.DataFrame(weights_array)
    df.to_csv(sys.argv[2], header=None)

if __name__ == '__main__':
    main()
