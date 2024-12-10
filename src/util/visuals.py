from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import datetime
from pathlib import Path


@dataclass
class GraphData:
    x: any
    y: any


class Graph:
    def __init__(self):
        self.data: list[GraphData] = []
        self.folder = "./data/graphs"

    def add_data_point(self, x, y):
        self.data.append(GraphData(x, y))

    def show(self):
        # plt.subplot(2, 1, 1)
        min = np.inf
        max = -np.inf
        x = []
        y = []
        for g in self.data:
            if g.x > max:
                max = g.x

            if g.x < min:
                min = g.x

            x.append(g.x)
            y.append(g.y)
        min, max = min - 50, max + 50
        plt.scatter(np.array(x), np.array(y), marker="o")

        plt.xlabel("CHGNET")
        plt.ylabel("DFT")
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
        save = (f"{self.folder}/{datetime.date.today()}/").replace(
                    "-", "_"
                )
        Path(save).mkdir(parents=True, exist_ok=True)
        save += f"{datetime.datetime.now()}.svg".replace("-", "_"
                                                         ).replace(":", "_")
        plt.plot(
            np.array([min, max]),
            np.array([min, max]),
            color="red", ls="--")
        plt.savefig(
            (save)
            )
        plt.show()


graph = Graph()
