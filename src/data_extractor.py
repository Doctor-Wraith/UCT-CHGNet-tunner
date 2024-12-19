# region Imports
try:
    from . import util
    from .database import data_classes, db
except ImportError:
    import util
    from database import data_classes, db

import uuid
import random
import os
import shutil
from pathlib import Path
from typing import Optional
# endregion


VALID_SURFACES = ["Pt"]


class Data:
    def __init__(self) -> None:
        self.outcar = None
        self.energy = None
        self.atoms: list[util.Atom] = None

    def set_energy(self):
        if self.outcar is None:
            raise FileNotFoundError("Please load the file path")

        for line in self.outcar[::-1]:
            if "energy(sigma->0)" in line.strip():
                list_line = line.replace("=", '').split()
                self.energy = list_line[5]
                break

    def check_surface(self, atom_name: str) -> tuple[bool, Optional[str]]:
        if atom_name in VALID_SURFACES:
            return (True, atom_name)

        return (False, None)

    def set_atoms(self):
        for line in self.outcar:
            if "ions per type =" in line.strip():
                number_atoms = line.split()[4::]
                break

        atoms = []
        for line in self.outcar:
            if "PAW_PBE" in line.strip():
                atom = line.split()[2]

                if atom not in atoms:
                    atoms.append(atom)
                else:
                    break

        self.atoms = []
        for atom, number in zip(atoms, number_atoms):
            surface = self.check_surface(atom)
            if surface[0]:
                self.atoms.append(util.Atom(surface[1], int(number),
                                            True, None, None))
            else:
                self.atoms.append(util.Atom(atom, int(number),
                                            False, None, None))

    def check_if_complete(self):
        found = False

        for line in self.outcar[::-1]:
            if "aborting loop because EDIFF is reached" in line:
                found = True
                break

        if not found:
            raise ValueError("File incomplete")

    def get_position_type(self) -> str:
        for line in self.outcar:
            if "positions in" in line:
                line = line.split()
                return line[2]

    def get_positions_forces(self) -> list:
        for index, line in enumerate(self.outcar[::-1]):
            if "POSITION" in line:
                break

        line_number = len(self.outcar) - index
        lines = []
        forces = []
        positions = []

        while "---" not in line:
            line_number += 1
            line = self.outcar[line_number]
            lines.append(line.split())

        lines.pop(len(lines) - 1)

        for line in lines:
            pos = util.Position()
            pos.x = line[0]
            pos.y = line[1]
            pos.z = line[2]
            pos.position_type = self.get_position_type()

            force = util.Force()
            force.x = line[3]
            force.y = line[4]
            force.z = line[5]

            positions.append(pos)
            forces.append(force)

        return [positions, forces]

    def set_positions_forces(self):
        atoms = []
        atom_forces = {x.name: [] for x in self.atoms}
        atoms_pos = {x.name: [] for x in self.atoms}
        for atom in self.atoms:
            for i in range(atom.count):
                atoms.append(atom.name)
        positions, forces = self.get_positions_forces()
        for index, pos_force in enumerate(zip(positions, forces)):
            pos = pos_force[0]
            force = pos_force[1]

            atom_forces[atoms[index]].append(force)
            atoms_pos[atoms[index]].append(pos)

        for atom in self.atoms:
            atom.forces = atom_forces[atom.name]
            atom.locations = atoms_pos[atom.name]

    def save_dir_local(self, directory="./data/OUTCAR"):
        def copy_tree(src, dst, symlinks=False, ignore=None):
            Path(dst).mkdir(parents=True, exist_ok=True)
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks, ignore)
                else:
                    shutil.copy2(s, d)

        name = self.folder.replace("\\", "/").split("/")[-1]
        copy_tree(self.folder, f"{directory}/{name}")

    # region Folder
    @property
    def folder(self) -> str:
        return self._folder

    @folder.setter
    def folder(self, value: str):
        value = value.replace("/OUTCAR", "")
        try:
            with open(f"{value}/OUTCAR", 'r') as outcar_file:
                self.outcar = outcar_file.readlines()
        except FileNotFoundError:
            self.outcar = None
            raise FileNotFoundError(f"Could not find Outcar at {value} or \
                                        at {value}/OUTCAR")

        self.check_if_complete()
        self._folder = value.replace("\\", "/")
        self.set_energy()
        self.set_atoms()
        self.set_positions_forces()

    # endregion
    # region Data extraction
    def to_dict(self) -> dict:
        atoms = {}
        for atom in self.atoms:
            positions = atom.locations
            forces = atom.forces

            list_pos = []
            for pos in positions:
                list_pos.append([pos.x, pos.y, pos.z])

            list_forces = []
            for force in forces:
                list_forces.append([force.x, force.y, force.z])

            atoms[atom.name] = {
                "surface": atom.surface,
                "positions": list_pos,
                "position_types": atom.locations[0].position_type,
                "forces": list_forces,
                "count": atom.count
            }

        out = {
            "atoms": atoms,
            "energy": self.energy,
            "folder": self.folder
        }
        return out

    # endregion


# region Database
def get_adsorbates(atoms: dict[str, data_classes.Atom]) -> list[
        Optional[data_classes.Atom]]:
    atoms = list(atoms.values())
    try:
        adsorbate_1 = atoms[0]
    except (TypeError, IndexError):
        adsorbate_1 = None
    try:
        adsorbate_2 = atoms[1]
    except (TypeError, IndexError):
        adsorbate_2 = None
    try:
        adsorbate_3 = atoms[2]
    except (TypeError, IndexError):
        adsorbate_3 = None

    return adsorbate_1, adsorbate_2, adsorbate_3


def save_to_data_base(data: Data):
    def check_db_path(path: str) -> bool:
        result = db.search_outcar_file(path)
        return True if result != [] else False

    if check_db_path(data.folder):
        return

    atoms = {}
    positions: list[data_classes.Position] = []
    forces: list[data_classes.Force] = []
    surface = None

    # data_dict = self.to_dict()
    # dict_atoms = data_dict["atoms"] # noqa
    for atom in data.atoms:
        atom_id = db.search_atom_id(atom.name)
        atom_uid = atom_id[0] if atom_id is not None else uuid.uuid4().hex
        atom_db = data_classes.Atom(atom_uid, atom.name)
        if not atom.surface:
            atoms[atom.name] = atom_db
        else:
            surface = atom_db

        for pos in atom.locations:
            position = data_classes.Position(
                uuid.uuid4().hex,
                atom_db,
                None,
                pos.position_type,
                pos.x,
                pos.y,
                pos.z
            )
            positions.append(position)

        for force in atom.forces:
            f = data_classes.Force(
                uuid.uuid4().hex,
                atom_db,
                None,
                force.x,
                force.y,
                force.z
            )
            forces.append(f)

    adsorbate_1, adsorbate_2, adsorbate_3 = get_adsorbates(atoms)
    tune = data_classes.Tunning(
        uuid.uuid4().hex,
        surface,
        adsorbate_1,
        adsorbate_2,
        adsorbate_3,
        data.energy,
        data.folder,
        random.choices([True, False], util.configuration["ratio"])[0]
    )

    if (surface is not None) and (
            db.search_atom_id(surface.atom_name) is None):
        db.add_atom(surface)

    for atom in atoms.values():
        if db.search_atom_id(atom.atom_name) is None:
            db.add_atom(atom)

    for pos in positions:
        pos.tunning = tune
        db.add_position(pos)
    for force in forces:
        force.tunning = tune
        db.add_force(force)

    db.add_tuning(tune)
# endregion
