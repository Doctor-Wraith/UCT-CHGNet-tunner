from src import data_extractor, util
from .util import logger
from src.database import db
from src.chargnet import charge_net, CHGNET
import glob
import random
import os
from .surface_update import update_db
try:
    import alive_progress
except ImportError:
    logger.error("response", "alive_progress module not found")
    logger.info("response", "installing alive_progress")
    os.system("pip install alive_progress")
    import alive_progress


class ResponseHandler:
    LOAD_DATA = ["load", "--l"]
    SAVE_LOCAL = ["save", '--s']
    TRAIN = ["train", '--t']
    UNLOAD = ["clear"]
    DB_RESET = ["reset", "--dbr"]
    CHECK = ["check"]
    VASP = ["vasp", "--v"]
    RANDO = ["random", '--r']

    def __init__(self) -> None:
        self.data = []

    def handler(self, command: str, *args):

        if command in self.LOAD_DATA:
            self.load_data()
        elif command in self.SAVE_LOCAL:
            self.save_local()
            self.to_json_from_vasp()
        elif command in self.TRAIN:
            self.train()
        elif command in self.UNLOAD:
            self.clear()
        elif command in self.DB_RESET:
            db.clear_database()
            self.clear_vasp()
        elif command in self.CHECK:
            self.check()
        elif command in self.VASP:
            self.to_json_from_vasp()
        elif command in self.RANDO:
            self.clear_vasp()
            db.randomize_tunning()
            self.to_json_from_vasp()
        else:
            print(f"The command {command} does not exists")

    def clear_vasp(self):
        folders = glob.glob("./data/chgnet/json/*")
        for folder in folders:
            files = glob.glob(f"{folder}/*.json")
            for file in files:
                os.remove(file)

    def clear(self):
        del self.data
        self.data = []

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
                        # TODO: Add logging here
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
                        self.clear()
        else:
            with alive_progress.alive_bar(len(self.data)) as bar:
                self.save(bar)
                self.clear()

        update_db()

    def check(self):
        i = 0
        while True:
            try:
                testing_model = CHGNET()
                print("max number of files: " +
                      str(len(glob.glob(testing_model.data_folder +
                                        "/json/test/*.json"))))
                testing_amount = int(util.get_input('testing amount> '))

                testing_files = util.get_files(
                    glob.glob(testing_model.data_folder +
                              "/json/test/*.json"), testing_amount)
            except ValueError:
                continue
            else:
                break

        models = glob.glob("./output/models/*")
        print(models)
        with alive_progress.alive_bar(len(models) * len(testing_files)) as bar:
            for model in models:
                testing_model.load_model(model.replace("\\", "/"))
                util.graph.set_model_name(model.replace("\\", "/").split("/")[-1]) # noqa
                for test in testing_files:
                    try:
                        name = test.replace("\\", "/").split("/")[-1].replace(
                            ".json", ""
                            )
                        i += 1
                        print(f"\n\n{test}\n\n")
                        testing_model.load_structures(test)
                        e = testing_model.predict()
                        e_actual = db.get_energy(name)[0]
                        util.graph.add_data_point(
                            name, e_actual, e * db.get_atom_count(name)
                            )
                    except Exception:
                        bar()
                    else:
                        bar()

                util.graph.show(max=-50)
                util.graph.reset()
        del testing_model

    def train(self):
        train_amount = int(util.get_input("Number of models to be made> "))

        data_training = db.search_outcar_file_train(True)
        num = random.randint(0, len(data_training) - 1 - train_amount)
        training_data = data_training[
            num:
            num + train_amount]

        charge_net.load_model()

        print("Turning to vasp to json")
        with alive_progress.alive_bar(train_amount) as bar:
            for data in training_data:
                print(data)
                charge_net.save_vasp_to_json(data[0])
                bar()

        with alive_progress.alive_bar(train_amount) as bar:
            # TODO: Add logging here
            files = glob.glob(charge_net.data_folder +
                              "/json/train/*.json")
            files = util.get_files(files, train_amount)
            for file in files:
                print(f"\n\n{file}\n\n")
                charge_net.load_structures(file)
                charge_net.train()

                bar()

    def to_json_from_vasp(self):
        data_training = db.search_outcar_file_train(True)
        data_testing = db.search_outcar_file_train(False)
        with alive_progress.alive_bar(len(data_training)) as bar:
            for data in data_training:
                print(data)
                charge_net.save_vasp_to_json(data[0])
                bar()

        with alive_progress.alive_bar(len(data_testing)) as bar:
            for data in data_testing:
                print(data)
                charge_net.save_vasp_to_json(data[0], False)
                bar()
