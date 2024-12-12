# region Imports
# region chgnet imports
from chgnet.model import CHGNet
from chgnet.utils import parse_vasp_dir, read_json
from chgnet.data.dataset import StructureData, get_train_val_test_loader
from chgnet.trainer import Trainer
# endregion

import numpy as np
from pymatgen.core import Structure
from pathlib import Path
import glob # noqa
try:
    from database import db
except ImportError:
    from .database import db # noqa
import random
import os

# endregion


# Setup
np.set_printoptions(precision=4, suppress=True)


class CHGNET:
    def __init__(self) -> None:
        self.structures: list[Structure] = []
        self.energies = []
        self.forces = []
        self.stresses = None
        self.magmoms = None

        self.data_folder = "./data/chgnet"
        self.chgnet = None

    def load_structures(self, file) -> None:
        try:
            dataset_dict = read_json(file)

            self.structures = [Structure.from_dict(struct) for struct in
                               dataset_dict["structure"]]
            self.energies = dataset_dict["energy_per_atom"]
            self.forces = dataset_dict["force"]
            self.stresses = dataset_dict.get("stress") if dataset_dict.get(
                "stress") != [] else None
            self.magmoms = dataset_dict.get("magmom") if dataset_dict.get(
                "magmom") != [] else None
        except Exception as e:
            raise e

    def load_model(self):
        try:
            self.chgnet = CHGNet.from_file(
                glob.glob(r"./data/models/bestE*")[0]
            )
        except Exception:
            self.chgnet = CHGNet.load()

    def predict(self):
        self.load_model()
        struct = random.choice(self.structures)
        prediction = self.chgnet.predict_structure(struct)
        for key, unit in [
            ("energy", "eV/atom")
                ]:
            print(f"CHGNet-predicted {key} ({unit}):\n{prediction[key[0]]}\n")
            return prediction[key[0]]

    def save_vasp_to_json(self, directory: str, train: bool = True) -> None:
        name = directory.replace("\\", "/").split("/")[-1]
        path = f'{self.data_folder}/json/train/{name}.json' if train else f'{self.data_folder}/json/test/{name}.json' # noqa
        if not os.path.isfile(path):
            parse_vasp_dir(directory, save_path=path)

    def train(self):
        dataset = StructureData(
            structures=self.structures,
            energies=self.energies,
            forces=self.forces,
            stresses=self.stresses,
            magmoms=self.magmoms
        )

        train_loader, val_loader, test_loader = get_train_val_test_loader(
            dataset, batch_size=8, train_ratio=0.9, val_ratio=0.05
        )

        for layer in [
            self.chgnet.atom_embedding,
            self.chgnet.bond_embedding,
            self.chgnet.angle_embedding,
            self.chgnet.bond_basis_expansion,
            self.chgnet.angle_basis_expansion,
            self.chgnet.atom_conv_layers[:-1],
            self.chgnet.bond_conv_layers,
            self.chgnet.angle_layers
        ]:
            for param in layer.parameters():
                param.requires_grad = False

        self.trainer = Trainer(
            model=self.chgnet,
            targets="ef",
            optimizer="Adam",
            scheduler="CosLR",
            criterion="MSE",
            epochs=5,
            learning_rate=1e-3,
            use_device="cpu",
            print_freq=100,
        )
        self.trainer.train(train_loader, val_loader, test_loader,
                           save_dir="./output/models",
                           save_test_result=True)

    # region Properties
    @property
    def data_folder(self) -> str:
        return self._data_folder

    @data_folder.setter
    def data_folder(self, value: str) -> None:
        Path(value).mkdir(parents=True, exist_ok=True)
        Path(value + "/json").mkdir(parents=True, exist_ok=True)
        # Path(value + "/models").mkdir(parents=True, exist_ok=True)
        self._data_folder = value
    # endregion


charge_net = CHGNET()
