import glob
import os
import json

def find_file(file_name:str, folder:str) -> list:
    result = []
    for root, dirs, files, in os.walk(folder):
        for file in files:
            if file_name in file:
                result.append(file)
    
    return result

def get_data(folder:str) -> list:
    try:
        # OUTCAR FILE
        with open(fr"{folder}\OUTCAR", 'r') as outcar_file:
            outcar = outcar_file.readlines()
        index = 1
        for line in outcar[::-1]:
            index += 1
            if line.strip() == "FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)":
                break
        
        # print(len(outcar) - index)

        energy = {}
        line_number = len(outcar) - index

        # Energy Toten
        line = outcar[line_number+3].split()
        # print(line)
        energy["toten"] = line[4]

        # Energy without entropy & energy sigma->0
        line = outcar[line_number+5].split()
        # print(line)
        energy["without_entropy"] = line[3]
        energy["sigma_0"] = line[6]

        # print(energy)        

    except FileNotFoundError:
        raise Exception(f"There was no OUTCAR file found in {folder}")
    

    # POSCAR FILES
    elements = {}
    poscar_file_names = find_file("POSCAR", folder)
    for poscar_file_name in poscar_file_names:
        # print(poscar_file)
        try:       
            with open(fr'{folder}\{poscar_file_name}', 'r') as poscar_file:
                poscar = poscar_file.readlines()
            
            if len(poscar_file_names) > 1:

                # elements[poscar_file_name.replace('POSCAR_', '')] = ({k:j for k, j in zip(poscar[5].split(), poscar[6].split())})
                elements[poscar_file_name.replace('POSCAR_', '')] = {k for k in poscar[5].split()}
            else:
                # elements["POSCAR"] = ({k:j for k, j in zip(poscar[5].split(), poscar[6].split())})
                elements["POSCAR"] = {k for k in poscar[5].split()}
            
            # print(elements, "\n\n")
        
        except FileNotFoundError:
            raise Exception(f"Could not find file {folder}\\{poscar_file}")

            
    
    # return elements, energy["sigma_0"]
    return {"elements":elements, "energy": energy}



def processe_data(folder:str, recursive=False):
    if not recursive:
        return get_data(folder=folder)
    else:
        out = []
        for filename in glob.glob(f'{folder}\\**\\vasprun.xml', recursive=True):
            out.append(get_data(filename.replace("\\vasprun.xml", "")))
        
        return out


l = processe_data('./data/New_opt_p3x3', recursive=True)
with open("test_out", 'w') as file:
    file.write(l)