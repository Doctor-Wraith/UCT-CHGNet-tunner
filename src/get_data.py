try:
    from . import util
    from .database import data_classes, db
except ImportError:
    import util
    from database import data_classes, db

from typing import Literal
import re, uuid, random


class DataExtracter:
    def __init__(self, folder:str) -> None:
        self.folder = folder
        self.outcar = None
        self.energy = None
        self.atoms = None
        self.positions = None
        self.forces = None
        self.surface = None
        self.position_type: Literal["cartesian", "direct"]

        self.get_file()
        self.check_if_complete()
        self.get_energy()
        self.get_atoms()
        self.check_for_surface()
        self.set_position_type()
        self.asign_positions_forces()

    def get_file(self)->None:
        '''
        Gets the OUTCAR file

        Args:
            file_path (str): the path to the OUCAR file or the path to the directory of the OUTCAR file
        
        '''

        # Load OUTCAR file
        try:
            with open(self.folder, "r") as outcar_file:
                self.outcar = outcar_file.readlines()
        except PermissionError:
            try: 
                with open(f"{self.folder}\\OUTCAR", 'r') as outcar_file:
                    self.outcar = outcar_file.readlines()
            except FileNotFoundError:
                self.outcar = None
                util.file_not_found(f"{self.folder}\\OUTCAR")
        
        except FileNotFoundError:
            self.outcar = None
            util.file_not_found(self.folder)


    def get_energy(self):
            for line in self.outcar[::-1]:
                if "energy(sigma->0)" in line.strip():
                    break
            
            line = line.replace("=", "")
            list_line = line.split()
            self.energy = list_line[5]
    
    
    def get_atoms(self):

        for line in self.outcar:
            if "ions per type =" in line.strip():
                break

        number_of_atoms = line.split()[4::]


        atoms = []
        for line in self.outcar:
            if "PAW_PBE" in line.strip():
                atom = line.split()[2]

                if atom not in atoms:
                    atoms.append(atom)
                else:
                    break
        
        self.atoms = {a:int(n) for a,n in zip(atoms, number_of_atoms)}
    
    def check_if_complete(self):
        found = False
        for line in self.outcar[::-1]:
            if "aborting loop because EDIFF is reached" in line:
                found = True
                break
        
        if not found:
            raise util.exceptions.NotCompleteOUTCAR(self.folder)

    def _get_atom_possitions_and_force(self):
        if self.atoms is not None:
            for index, line in enumerate(self.outcar[::-1]):
                if "POSITION" in line:
                    break
            
            line_number = len(self.outcar) - index
            lines = []
            forces = []
            positions = []

            while "---" not in line:
                line_number += 1
                line = self.outcar[line_number].replace("\n", "")
                lines.append(line.split())
            
            lines.pop(len(lines) - 1)

            for line in lines:
                p = util.Position()
                p.x = line[0]
                p.y = line[1]
                p.z = line[2]

                f = util.Force()
                f.x = line[3]
                f.y = line[4]
                f.z = line[5]
                positions.append(p)
                forces.append(f)
            
            return positions, forces
                

    def set_position_type(self):
        for line in self.outcar:
            if "positions in" in line:
                break

        line = line.split()
        self.position_type = line[3]

    def asign_positions_forces(self):
        atoms = []
        for atom in self.atoms.keys():
            for i in range(self.atoms[atom]):
                atoms.append(atom)
        atom_forces = {x: [] for x in self.atoms.keys()}
        atom_positions = {x: [] for x in self.atoms.keys()}

        positions, forces = self._get_atom_possitions_and_force()

        for index, pos_force in enumerate(zip(positions, forces)):
            pos = pos_force[0]
            force = pos_force[1]
            atom_forces[atoms[index]].append(force)
            atom_positions[atoms[index]].append(pos)
        
        self.forces = atom_forces
        self.positions = atom_positions
    
    def save_outcar_file(self, directory="./data/OUTCAR"):
        with open(f"{directory}\\{self.folder.split("\\")[-1]}", 'w') as output_file:
            output_file.writelines(self.outcar)
        
        self.folder = f"{directory}\\{self.folder.split("\\")[-1]}"
    
    def check_for_surface(self):
        # if "Pt" in self.atoms.keys():
        #     name = self.folder.replace("\\", "/").split("/")[-1].split("_")[0]
        #     count = self.atoms["Pt"]
        #     del self.atoms["Pt"]
        #     self.atoms = {name:count} | self.atoms

        names = self.folder.replace("\\", "/").split("/")
        for name in names:
            for i in name.split("_"):
                element = "".join(re.findall('([a-zA-z])', i))
                if element in self.atoms.keys():
                    count = self.atoms[element]
                    del self.atoms[element]
                    self.atoms = {i:count} | self.atoms
                    self.surface = i

    def to_dict(self):
        atoms = {}
        for atom in self.atoms.keys():
            positions = self.positions[atom]
            forces = self.forces[atom]
            
            posses = []
            for pos in positions:
                posses = [pos.x, pos.y, pos.z]
            
            forces_2 = []
            for force in forces:
                forces_2 = [force.x, force.y, force.z]
            
            atoms[atom] = {
                "positions": posses,
                "forces": forces_2,
                "count": self.atoms[atom]
            }
        
        out = {
            "atoms": atoms,
            "energy": self.energy,
            "file": self.folder
        }
        
        return out


    def calc_distance(self):
        positions = []
        out = []
        for i in self.positions.items():
            for j in i[1]:
                positions.append([i[0],j])
        
        n = len(positions)
        for i in range(n-1):
            for j in range(i+1, n):
                out.append([positions[i], positions[j]])
        
        distances = {}

        for k in out:
            atom_1, atom_2 = k
            distances[f"{atom_1[0]}_{atom_2[0]}"] = util.distance.distance(atom_1[1], atom_2[1])

        return distances

def prep_data(data: DataExtracter) -> dict:
    def get_adsorbates(atoms: dict[str, data_classes.Atom]) -> list[data_classes.Atom|None]:
        atoms = list(atoms.values())
        try:
            adsorbate_1 = atoms[0]
        except:
            adsorbate_1 = None
        try:
            adsorbate_2 = atoms[1]
        except:
            adsorbate_2 = None
        try:
            adsorbate_3 = atoms[2]
        except:
            adsorbate_3 = None

        return adsorbate_1, adsorbate_2, adsorbate_3

    data_dict = data.to_dict()


    dict_atoms = data_dict.get("atoms")
    atoms = {}
    positions: list[data_classes.Position] = []
    forces: list[data_classes.Force] = []

    for atom in dict_atoms.keys():
        atom_id = db.search_atom_id(atom)
        atom_uid =  atom_id[0] if atom_id is not None else uuid.uuid4().hex 
        a = data_classes.Atom(atom_uid, atom)
        atoms[atom] = a

        pos = data_classes.Position(uuid.uuid4().hex, a, None, data.position_type, 
                                    data_dict["atoms"][atom]["positions"][0],
                                    data_dict["atoms"][atom]["positions"][1],
                                    data_dict["atoms"][atom]["positions"][2])
        positions.append(pos)

        force = data_classes.Force(uuid.uuid4().hex, a, None, 
                                   data_dict["atoms"][atom]["forces"][0],
                                   data_dict["atoms"][atom]["forces"][1],
                                   data_dict["atoms"][atom]["forces"][2])
        forces.append(force)

    print(atoms)
    # print(positions)
    # print(forces)

    surface:data_classes.Atom = atoms.get(data.surface, None)

    try:
        del atoms[surface.atom_name]
    except AttributeError:
        pass

    adsorbate_1, adsorbate_2, adsorbate_3 = get_adsorbates(atoms)
    
    tune = data_classes.Tunning(uuid.uuid4().hex, surface, 
                                adsorbate_1, adsorbate_2, adsorbate_3,
                                data.energy, data.folder, random.choices([True, False], [80, 20])[0])
    
    for pos in positions:
        pos.tunning = tune
    
    for force in forces:
        force.tunning = tune

    # Add to db
    for atom in atoms.values():
        db.add_atom(atom)
    

    for pos in positions:
        db.add_position(pos)
    
    for force in forces:
        db.add_force(force)
        
    db.add_tuning(tune)
