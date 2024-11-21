import os
from . import util

def get_file(file_path:str)->list[str]:
    '''
    Gets the OUTCAR file

    Args:
        file_path (str): the path to the OUCAR file or the path to the directory of the OUTCAR file
    
    Returns:
        list: A list of file lines
    '''

    # Load OUTCAR file
    try:
        with open(file_path, "r") as outcar_file:
            outcar = outcar_file.readlines()
    except PermissionError:
        try: 
            with open(f"{file_path}\\OUTCAR", 'r') as outcar_file:
                outcar = outcar_file.readlines()
        except FileNotFoundError:
            util.file_not_found(f"{file_path}\\OUTCAR")
            return
    
    except FileNotFoundError:
        util.file_not_found(file_path)
        return

    return outcar


def get_data(outcar:list[str]) -> dict:
    def get_energy() -> float:
        for line in outcar[::-1]:
            if "energy(sigma->0)" in line.strip():
                break
        
        line = line.replace("=", "")
        list_line = line.split()
        return list_line[5]
    
    def get_atoms() -> dict[str, int]:

        for line in outcar:
            if "ions per type =" in line.strip():
                break

        number_of_atoms = line.split()[4::]

        for line in outcar:
            if "POSCAR:" in line.strip():
                break
        
        atoms = line.split()[1::]    
        
        result = {a:n for a,n in zip(atoms, number_of_atoms)}
        return result

    
    energy = get_energy()
    atoms = get_atoms()
    
    return {
        "energy": energy,
        "atoms": atoms
    }
    

 


# ------------------------------------------------
# TESTS
# ------------------------------------------------
# outcar_CO = get_file(r"D:\UCT Stuff\Projects\UCT\data\New_opt_p3x3\COgas")
# data_CO = get_data(outcar_CO)
# print(data_CO)

# outcar_Pt100_1xO = get_file(r"D:\UCT Stuff\Projects\UCT\data\New_opt_p3x3\Pt100_1xO\OUTCAR")
# data_Pt100_1xO = get_data(outcar_Pt100_1xO)
# print(data_Pt100_1xO)

# for folder in util.scandir("./data/New_opt_p3x3"):
#     outcar = get_file(folder)
#     if outcar is not None:
#         data = get_data(outcar)
#         print(data)