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

    def add_data_point(self, x, y):
        self.data.append(GraphData(x, y))

    def show(self):
        # plt.subplot(2, 1, 1)
        x = []
        y = []
        for g in self.data:
            x.append(g.x)
            y.append(g.y)
        plt.scatter(np.array(x), np.array(y), marker="o")

        plt.xlabel("x - axis")
        plt.ylabel("y - label")
        plt.grid()

        y = []
        x = []
        # plt.subplot(2, 1, 2)
        # i = 0
        # for data in self.data:
        #     i += 1
        #     y.append(data.y - data.x)
        #     x.append(i)
        # plt.plot(np.array(x), np.array(y), marker=".")
        plt.show()


graph = Graph()
