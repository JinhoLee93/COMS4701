#####
# Jinho Lee (jl5027)
# COMS 4701
# Prof. Ansaf Salleb-Aouissi
# lr.py
#####

import pandas as pd
import matplotlib
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import sys
import numpy as np
from plot_db import visualize_scatter, visualize_3d

def error(data, height, w):

    return (np.dot(data, w) - height)

def gradient_descent(data, height, w, a):
    num = len(w)
    for i, xi in enumerate(data):
        for j in range(num):
            err = error(xi, height[i], w)
            w[j] = w[j] - a * err * xi[j]

def fit(data, height, w, a, iterations=100):
    ar = []
    ar.append(a)
    ar.append(iterations)
    for iteration in range(iterations):
        gradient_descent(data, height, w, a)

    for i in range(len(w)):
        ar.append(w[i])

    """csv = np.array(ar)
    csv = np.reshape(csv, (-1, 5))"""

    df = pd.DataFrame(data)
    #visualize_3d(df, lin_reg_weights=w, title="a = %.3f"%a)

    return ar

def normalize():
    data_csv = pd.read_csv(sys.argv[1], header=None)
    data = np.array(data_csv)

    rows = data.shape[0]
    intercepts = np.ones(rows)
    intercepts.shape = (rows, 1)

    age    = scale(data[:,[0]])
    weight = scale(data[:,[1]])
    height = scale(data[:,[2]])

    data = np.hstack((intercepts, age, weight))

    return data, height

def scale(feature):
    mean = np.mean(feature)
    st = np.std(feature)

    for i in range(len(feature)):
        holder = feature[i]
        feature[i] = (holder - mean) / (st)

    return feature

def main():
    ar = []
    data, height = normalize()
    alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.45]
    for a in alphas:
        B = np.zeros(3)
        out = fit(data, height, B, a)
        ar.append(out)

    csv = np.array(ar)
    df = pd.DataFrame(csv)
    df.to_csv(sys.argv[2], header=None)

if __name__ == '__main__':
    main()