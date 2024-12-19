try:
    from util import logger
except ImportError:
    from .util import logger


class Help:
    COMMANDS = ["load", "save", "train", "clear", "reset",
                "check", "vasp", "random"]

    def __init__(self):
        self.COMMANDS = {
            "load": self.load,
            "save": self.save,
            "train": self.train,
            "clear": self.clear,
            "reset": self.reset,
            "check": self.check,
            "vasp": self.vasp,
            "random": self.random,
            "help": self.help
        }

    def get_help(self, cmd: str):
        cmd = cmd.strip().lower()
        logger.info("help", f"Giving help for command {cmd}", True)
        if cmd in self.COMMANDS.keys():
            print(self.COMMANDS.get(cmd)())
        else:
            logger.warn("help", f"the command {cmd} is not in the help\
                         documentation")

    def list_commands(self):
        cmd = self.COMMANDS.keys()
        cmd = list(cmd)
        cmd.append("stop")
        cmd.sort()
        out = "Available commands:\n\t- " + "\n\t- ".join(cmd)
        print(out)

    def help(self):
        out = "lists the functions or if given a command give a \
quick description of what it does"
        return out

    def load(self):
        out = "The load function is used to load OUTCAR files into memory\n\n\
When running the user will be prompted whether they would like\
for the program to recursively go through the folder and search\
for OUTCAR files\n\n\
The program will then prompt for the folder path that contains\
the OUTCAR files"

        return out

    def save(self):
        out = "The save function is used to save the data saved in memory\
and store it in the database\n\
The user will be prompted whether they wish to save locally\
which will create a copy of the OUTCAR files in the data\
folder\n\nThe VASP function is automatically called after\
this function"
        return out

    def train(self):
        out = "The train function will take a random OUTCAR file and use it\
to train a model\nThe user will be prompt for how many models\
 they would like to produce\n\nNew models will be saved in\
output/models\n\nIf you wish you can place a model into the\
folder data/chgnet/models to give the trainer a model to\
start from"
        return out

    def clear(self):
        out = "Unloads the data that load put into memory"
        return out

    def reset(self):
        out = "Clears the database of all data.\n This includes\
the json files that are required for CHGNet"
        return out

    def vasp(self):
        out = "Transforms the OUTCAR files and vasprun.xml into\
the necessary structure files for CHGNet and store\
in a .json file under data/chgnet/json"
        return out

    def check(self):
        out = "Uses CHGNet to predict the energy of the systems\
marked for testing\n\nThis function generates a graph\
and a stats file in the output folder\nThe files will be\
saved under the name of the model that it tests\n\
This function will go through all the models in\
out/models"
        return out

    def random(self):
        out = "This function will reassign which systems will be used\
for training or testing, the ration of which can be altered\
in config.json"
        return out


help = Help()
