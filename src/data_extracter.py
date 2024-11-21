import glob, os

def find_file(file_name:str, folder:str) -> list:
    result = []
    for root_dir, folders, files, in os.walk(folder):
        for file in files:
            if file_name in file:
                result.append(file)
    
    return result

def get_data(folder:str) -> dict:
    '''
    Gets the data from a folder
    Args:
        folder (str): Path of the folder
    '''
    try:
        # OUTCAR FILE
        with open(fr"{folder}\OUTCAR", 'r') as outcar_file:
            outcar = outcar_file.readlines()

        index = 1

        # Easier to read file from the bottom
        for line in outcar[::-1]:
            index += 1
            if "energy(sigma->0) =" in line.strip():              
                break
        
        energy = None
        line_number = len(outcar) - index + 1

        # Get on of the energies
        # sigma->0
        
        line = outcar[line_number].split()
        
        # Cleaing data
        # consitancy of where the '=' appearses was not consisant
        try:
            line.remove("=")
            line.remove("=")
        except: pass
        energy = line[5]     

    except FileNotFoundError:
        raise Exception(f"There was no OUTCAR file found in {folder}")
    

    # POSCAR FILES
    elements = []
    poscar_file_names = find_file("POSCAR", folder)
    for poscar_file_name in poscar_file_names:
        try:       
            with open(fr'{folder}\{poscar_file_name}', 'r') as poscar_file:
                poscar = poscar_file.readlines()
            
            elements += poscar[5].split()
        
        except FileNotFoundError:
            raise Exception(f"Could not find file {folder}\\{poscar_file}")

        else:
            # Make sure elements are unique
            elements = list(dict.fromkeys(elements))

    # use the folder name to find which Pt is being used
    if "Pt" in elements:
        elements.remove("Pt")

        elements.insert(0, folder.split('\\')[::-1][0].split("_")[0])           
    
    return {"elements":elements, "energy": energy, "file": folder}



def processe_data(folder:str, recursive=False) -> list[dict]:
    '''
    Takes the folder where the vasprun.xml is and extracts the data

    Args:
        folder (str): the path to the folder
        recursive (bool): Look through all folders for all folders with vasprun.xml

    Returns:
        list[dict]: A list of dictionaries with all the data
    '''
    if not recursive:
        return [get_data(folder=folder)]
    else:
        out = []
        for filename in glob.glob(f'{folder}\\**\\vasprun.xml', recursive=True):
            out.append(get_data(filename.replace("\\vasprun.xml", "")))
        
        return out
