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
import alive_progress # noqa

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
        dataset_dict = read_json(file)

        self.structures = [Structure.from_dict(struct) for struct in
                           dataset_dict["structure"]]
        self.energies = dataset_dict["energy_per_atom"]
        self.forces = dataset_dict["force"]
        self.stresses = dataset_dict.get("stress") if dataset_dict.get(
            "stress") != [] else None
        self.magmoms = dataset_dict.get("magmom") if dataset_dict.get(
            "magmom") != [] else None

    def load_model(self):
        print(glob.glob(r"./data/chgnet/models/bestE*")[0])
        try:
            self.chgnet = CHGNet.from_file(
                glob.glob(r"./data/chgnet/models/bestE*")[0]
            )
        except Exception:
            self.chgnet = CHGNet.load()

    def predict(self):
        self.load_model()
        struct = random.choice(self.structures)
        prediction = self.chgnet.predict_structure(struct)
        for key, unit in [
            ("energy", "eV/atom"),
            ("forces", "eV/A"),
            ("stress", "GPa"),
            ("magmom", "mu_B"),
                ]:
            print(f"CHGNet-predicted {key} ({unit}):\n{prediction[key[0]]}\n")

    def save_vasp_to_json(self, directory: str) -> None:
        name = directory.replace("\\", "/").split("/")[-1]
        parse_vasp_dir(directory,
                       save_path=f'{self.data_folder}/json/{name}.json')

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
            epochs=50,
            learning_rate=1e-3,
            use_device="cpu",
            print_freq=6,
        )
        self.trainer.train(train_loader, val_loader, test_loader,
                           save_dir=self.data_folder + "/models", 
                           save_test_result=True)

    # region Properties
    @property
    def data_folder(self) -> str:
        return self._data_folder

    @data_folder.setter
    def data_folder(self, value: str) -> None:
        Path(value).mkdir(parents=True, exist_ok=True)
        Path(value + "/json").mkdir(parents=True, exist_ok=True)
        Path(value + "/models").mkdir(parents=True, exist_ok=True)
        self._data_folder = value
    # endregion


# Test
chargnet = CHGNET()
chargnet.load_model()

# dirs = db.search_outcar_file_train(True)

# with alive_progress.alive_bar(len(dirs)) as bar:
#     for directory in dirs:
#         chargnet.save_vasp_to_json(directory[0])
#         bar()

index = 50
with alive_progress.alive_bar(len(glob.glob(chargnet.data_folder +
                                            "/json/*.json")[:index])) as bar:
    for file in glob.glob(chargnet.data_folder + "/json/*.json")[:index]:
        print(f"\n\n{file}\n")
        chargnet.load_structures(file)
        chargnet.train()

        bar()


print(glob.glob(chargnet.data_folder + "/json/*.json")[60])
chargnet.load_structures(glob.glob(chargnet.data_folder +
                                   "/json/*.json")[60])

chargnet.predict()
