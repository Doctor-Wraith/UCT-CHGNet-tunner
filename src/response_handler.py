from . import data_extractor, util
import alive_progress
from .database import db
from .chargnet import charge_net, CHGNET
import glob
import random


class ResponseHandler:
    LOAD_DATA = ["load", "--l"]
    SAVE_LOCAL = ["save", '--s']
    TRAIN = ["train", '--t']
    UNLOAD = ["clear"]

    def __init__(self) -> None:
        self.data = []

    def handler(self, command: str, *args):

        if command in self.LOAD_DATA:
            self.load_data()
        elif command in self.SAVE_LOCAL:
            self.save_local()
        elif command in self.TRAIN:
            self.train()
        elif command in self.UNLOAD:
            del self.data
            self.data = []
        else:
            print(f"The command {command} does not exists")

    def load_data(self):
        multiple = util.get_input(
            "Recursively Search directory [Y/n]> "
            ).lower()

        if multiple == "y":
            path = util.get_input("Path> ")
            self.data = []
            folders = util.scandir(path)
            with alive_progress.alive_bar(len(folders)) as bar:
                for folder in folders:
                    try:
                        print(folder)
                        outcar = data_extractor.Data()
                        outcar.folder = folder

                    except FileNotFoundError:
                        bar()
                        continue
                    except ValueError:
                        bar()
                        continue
                    else:
                        self.data.append(outcar)
                        bar()
        else:
            path = util.get_input("Path> ")
            outcar = data_extractor.Data()
            outcar.folder = path
            self.data = [outcar]

    def save(self, bar):
        if self.data is not None:
            for dat in self.data:
                data_extractor.save_to_data_base(dat)
                bar()
        else:
            print("Please load data")

    def save_local(self):
        local_save = util.get_input("Save local [Y/n]> ").strip().lower()

        if local_save == "y":
            with alive_progress.alive_bar(len(self.data)) as bar:
                for dat in self.data:
                    try:
                        dat.save_dir_local()
                    except Exception:
                        bar()
                    else:
                        self.save(bar)
        else:
            with alive_progress.alive_bar(len(self.data)) as bar:
                self.save(bar)

    def train(self):
        train_amount = int(util.get_input("Number of training data> "))
        testing_amount = int(util.get_input("Number of testing data> "))

        data_training = db.search_outcar_file_train(True)
        num = random.randint(0, len(data_training) - 1 - train_amount)
        training_data = data_training[
            num:
            num + train_amount]

        data_testing = db.search_outcar_energy(False)
        num_2 = random.randint(0, len(data_testing) - 1 - testing_amount)
        testing_data = data_testing[
            num_2:
            num_2 + testing_amount]

        charge_net.load_model()

        print("Turning to vasp to json")
        with alive_progress.alive_bar(train_amount) as bar:
            for data in training_data:
                print(data)
                charge_net.save_vasp_to_json(data[0])
                bar()

        print("Turing testing vasp to json")
        with alive_progress.alive_bar(testing_amount) as bar:
            for data in testing_data:
                print(data)
                charge_net.save_vasp_to_json(data[1], False)
                bar()

        print("\n\nTraining\n\n")

        with alive_progress.alive_bar(train_amount) as bar:
            # TODO: Add logging here
            files = glob.glob(charge_net.data_folder +
                              "/json/train/*.json")
            files = self.get_files(files, train_amount)
            for file in files:
                print(f"\n\n{file}\n\n")
                charge_net.load_structures(file)
                charge_net.train()

                testing_model = CHGNET()
                testing_files = self.get_files(
                    glob.glob(testing_model.data_folder +
                              "/json/test/*.json")[:testing_amount])
                for test in testing_files:
                    print(f"\n\n{test}\n\n")
                    testing_model.load_structures(test)
                    testing_model.predict()

                del testing_model

                bar()

    def get_files(self, files: list, amount: int) -> list:
        """
        Gets a random assortment of files from a list
        Args:
            files (list): a list of folders
            amount (int): the amount of files wanted
        Returns:
            list: a random assortment of files
        Raises:
            ValueError: Raises a value Error
        """
        if len(files) < amount:
            raise ValueError(f"Amount: {amount} < File: {len(files)}")
        if len(files) == amount:
            return files
        else:
            out = []
            for _ in range(amount):
                file = random.choice(files)
                out.append(file)
                files.remove(file)
                del file
