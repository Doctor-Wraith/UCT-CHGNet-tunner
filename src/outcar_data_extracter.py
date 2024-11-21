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
        # energy = None
        # OUTCAR FILE
        with open(fr"{folder}\OUTCAR", 'r') as outcar_file:
            outcar = outcar_file.readlines()
        index = 1
        done_energy = False
        done_forces = False
        for line in outcar[::-1]:
            index += 1
            if "energy(sigma->0) =" in line.strip():      
                # print(len(outcar) - index)
        
                break
        
        energy = {}
        line_number = len(outcar) - index

        # # Energy Toten
        # line = outcar[line_number+3].split()
        # # print(line)
        # energy["toten"] = line[4]

        # # Energy without entropy & energy sigma->0
        line = outcar[line_number+1].split()
        # print(line_number)
        # print(line)
        # # print(line)
        # energy["without_entropy"] = line[3]
        try:
            line.remove("=")
            line.remove("=")
        except: pass
        # print(line)
        energy["sigma_0"] = line[5]
        # print(energy["sigma_0"])

        # print(energy)        

    except FileNotFoundError:
        raise Exception(f"There was no OUTCAR file found in {folder}")
    

    # POSCAR FILES
    elements = []
    poscar_file_names = find_file("POSCAR", folder)
    for poscar_file_name in poscar_file_names:
        # print(poscar_file)
        try:       
            with open(fr'{folder}\{poscar_file_name}', 'r') as poscar_file:
                poscar = poscar_file.readlines()
            
              # elements[poscar_file_name.replace('POSCAR_', '')] = ({k:j for k, j in zip(poscar[5].split(), poscar[6].split())})
            elements += poscar[5].split()


            
            # print(elements, "\n\n")
        
        except FileNotFoundError:
            raise Exception(f"Could not find file {folder}\\{poscar_file}")

        else:
            elements = list(dict.fromkeys(elements))

    if "Pt" in elements:
        elements.remove("Pt")

        elements.insert(0, folder.split('\\')[::-1][0].split("_")[0])

    
    print(f"{elements}\n")

            
    
    # return elements, energy["sigma_0"]
    return {"elements":elements, "energy": energy["sigma_0"], "file": folder}



def processe_data(folder:str, recursive=False):
    if not recursive:
        return get_data(folder=folder)
    else:
        out = []
        for filename in glob.glob(f'{folder}\\**\\vasprun.xml', recursive=True):
            out.append(get_data(filename.replace("\\vasprun.xml", "")))
        
        return out

count_total = 0
count = 0
l = processe_data('./data/New_opt_p3x3', recursive=True)

with open("./data/test_out.json", 'w') as file:
    file.write(json.dumps(l, indent=2))

# p = get_data('./data/New_opt_p3x3\\Coverage_lat_int_OH_Pt_p3x3_copy\\Pt111_2xOH\\Pt111_2xOH_vasp')
# print(p)