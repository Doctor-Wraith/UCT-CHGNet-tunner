# region Imports
from dataclasses import dataclass
import os

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

        x = np.array(x)
        y = np.array(y)

        ax.scatter(x, y, marker="o")

        # Line of best fit
        a, b = np.polyfit(x, y, 1)
        print()
        print(a)
        print(b)
        plt.plot(x, a*x+b)

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
