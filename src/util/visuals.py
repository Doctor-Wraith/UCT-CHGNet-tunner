from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import datetime
from pathlib import Path
from .logger import logger


@dataclass
class GraphData:
    x: any
    y: any
    name: str


class Graph:
    def __init__(self):
        self.data: list[GraphData] = []
        self.folder = "./data/graphs"

    def add_data_point(self, name, x, y):
        self.data.append(GraphData(x, y, name))

    def show(self, labeled: bool = False, min: int = None, max: int = None):
        """
        Displays a graph of data points of DFT vs CHGNET

        Args:
            Labeled (bool): display the labels of points
            min (int): minimum data point to be shown
            max (int): maximin data point to be shown
        """
        minimum = np.inf
        maximum = -np.inf
        x = []
        y = []
        names = []
        for g in self.data:
            if min is not None:
                if g.x < min:
                    continue
            if max is not None:
                if g.x > max:
                    continue

            if g.x > maximum:
                maximum = g.x

            if g.x < minimum:
                minimum = g.x

            x.append(g.x)
            y.append(g.y)
            names.append(g.name)

        minimum, maximum = minimum - 10, maximum + 10
        ax = plt.subplot()
        ax.scatter(np.array(x), np.array(y), marker="o")

        if labeled:
            for i, txt in enumerate(names):
                ax.annotate(txt, (x[i], y[i]))

        plt.xlabel("CHGNET")
        plt.ylabel("DFT")
        plt.grid()
        save = (f"{self.folder}/{datetime.date.today()}/").replace(
                    "-", "_"
                )
        Path(save).mkdir(parents=True, exist_ok=True)
        save += f"{datetime.datetime.now()}.svg".replace("-", "_"
                                                         ).replace(":", "_")
        plt.plot(
            np.array([minimum, maximum]),
            np.array([minimum, maximum]),
            color="red", ls="--")
        logger.info("Visuals", f"saving graph to {save}", False)
        plt.savefig(
            (save)
            )
        plt.show()


graph = Graph()
