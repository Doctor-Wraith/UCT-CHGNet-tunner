# region Imports
from dataclasses import dataclass
import os
from io import TextIOWrapper
import statistics

try:
    from .logger import logger
except ImportError:
    from logger import logger

try:
    import matplotlib.pyplot as plt
except ImportError:
    logger.error("visuals", "matplotlib module not found")
    logger.info("visuals", "installing matplotlib")
    os.system("pip install matplotlib")
    import matplotlib.pyplot as plt

try:
    import numpy as np
except ImportError:
    logger.error("visuals", "numpy module not found")
    logger.info("visuals", "installing numpy")
    os.system("pip install numpy")
    import numpy as np

import datetime
from pathlib import Path
# endregion


@dataclass
class GraphData:
    x: any
    y: any
    name: str


class Graph:
    def __init__(self):
        self.data: list[GraphData] = []
        self.folder = "./output/graphs"
        self.name = "unnamed"

    def add_data_point(self, name, x, y):
        self.data.append(GraphData(x, y, name))

    def reset(self):
        self.data: list[GraphData] = []
        self.name = "unnamed"

    def set_model_name(self, name: str):
        self.name = name

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
        x = np.array(x)
        y = np.array(y)

        ax.scatter(x, y, marker="o")

        # Line of best fit
        a, b = np.polyfit(x, y, 1)
        plt.plot(x, a*x+b)

        dist = [abs(i-j) for i, j in zip(x, y)]
        p = "./output/stats/"
        Path(p).mkdir(parents=True, exist_ok=True)
        with open(f"{p}{self.name}.txt", "w") as output:
            self.save_to_file(output, dist)

        if True:
            for i, txt in enumerate(names):
                ax.annotate(txt, (x[i], y[i]))

        plt.xlabel("CHGNET")
        plt.ylabel("DFT")
        plt.grid()
        save = (f"{self.folder}/{datetime.date.today()}/").replace(
                    "-", "_"
                )
        Path(save).mkdir(parents=True, exist_ok=True)

        save += f"{self.name}.svg"
        plt.plot(
            np.array([minimum, maximum]),
            np.array([minimum, maximum]),
            color="red", ls="--")
        logger.info("Visuals", f"saving graph to {save}", False)
        plt.title(self.name)
        plt.savefig(
            (save)
            )
        # plt.show()
        plt.clf()

    def save_to_file(self, file: TextIOWrapper, dist: list):
        file.write(self.name + "\n")
        file.write("Distances from DFT:\n")
        for d in dist:
            file.write(f"\t{d}\n")
        file.write("\n")
        file.write("Summary:\n")
        file.write(f"\tMean:\t{sum(dist)/len(dist)}\n")
        file.write(f"\tMedian:\t{statistics.median(dist)}\n")
        file.write(f"\tMax dist:\t{max(dist)}\n")
        file.write(f"\tMin dist:\t{min(dist)}\n")


graph = Graph()
