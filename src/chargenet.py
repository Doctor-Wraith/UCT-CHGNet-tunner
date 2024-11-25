from chgnet.model import CHGNet
from chgnet.trainer import Trainer

import numpy as np
from pymatgen.core import Structure
from chgnet.utils import parse_vasp_dir
from chgnet.utils import read_json
from chgnet.data.dataset import StructureData, get_train_val_test_loader

import glob
import alive_progress
try:
    from .database import db
except ImportError:
    from database import db


def parse_data():
    vasp_dirs:list[str] = db.search_outcar_file_train(True)
    dataset_dicts = []
    with alive_progress.alive_bar(len(vasp_dirs)) as bar:
        for vasp_dir in vasp_dirs:
            name = vasp_dir[0].replace("\\","/").split("/")[-1]
            print(name)
            dataset_dict = parse_vasp_dir(
                base_dir=vasp_dir[0], save_path=f"./data/chgnet/{name}.json"
            )

            dataset_dicts.append(dataset_dict)
            bar()
    
    return dataset_dicts

def prep_train_data(file):
        dataset_dict = read_json(file)
        structures = [Structure.from_dict(struct) for struct in dataset_dict["structure"]]
        energies = dataset_dict["energy_per_atom"]
        forces = dataset_dict["force"]
        stresses = dataset_dict.get("stress", None)
        magnoms = dataset_dict.get("magnom", None)

        # Define dataset
        dataset = StructureData(
            structures=structures,
            energies=energies,
            forces=forces,
            stresses=stresses,
            magmoms=magnoms
        )

        train_loader, val_loader, test_loader = get_train_val_test_loader(
            dataset, batch_size=8, train_ratio=0.9, val_ratio=0.05
        )

        return datasets, train_loader, val_loader, test_loader



datasets = []
for file in glob.glob("./data/chgnet/*.json"):
    datasets.append(prep_train_data(file))


chgnet = CHGNet.load()

trainer = Trainer(
    model=chgnet,
    targets="efs",
    optimizer="Adam",
    scheduler="CosLR",
    criterion="MSE",
    epochs=5,
    learning_rate=1e-2,
    use_device="cpu",
    print_freq=6
)


with alive_progress.alive_bar(len(datasets)) as bar:
    for dataset, train_loader, val_loader, test_loader in datasets:
        trainer.train(train_loader, val_loader, test_loader)
        bar()
        break

print("\n\n")

model = trainer.model
print(model)
best_model = trainer.best_model
print("\n")
with open("out.txt", 'w') as f:
     f.write(str(best_model.todict()))

trainer.save()
