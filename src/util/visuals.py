from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class GraphData:
    x: any
    y: any


class Graph:
    def __init__(self):
        self.data: list[GraphData] = []
        self.actual_data: list[GraphData] = []

    def add_data_point(self, x, y):
        self.data.append(GraphData(x, y))

    def add_actual(self, x, y):
        self.actual_data.append(GraphData(x, y))

    def show(self):
        plt.subplot(2, 1, 1)
        x = []
        y = []
        for g in self.data:
            x.append(g.x)
            y.append(g.y)
        plt.plot(np.array(x), np.array(y), label="predicted", marker="o")
        x = []
        y = []
        for g in self.actual_data:
            x.append(g.x)
            y.append(g.y)
        plt.plot(np.array(x), np.array(y), label="actual", marker="*")

        plt.xlabel("x - axis")
        plt.ylabel("y - label")
        plt.grid()

        y = []
        x = []
        plt.subplot(2, 1, 2)
        i = 0
        for actual, predicted in zip(self.actual_data, self.data):
            i += 1
            y.append(predicted.y - actual.y)
            x.append(i)
        plt.plot(np.array(x), np.array(y), marker=".")
        plt.show()


graph = Graph()
