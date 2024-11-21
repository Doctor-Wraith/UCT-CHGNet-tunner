from chgnet.model import CHGNet
import numpy as np
from pymatgen.core import Structure

# Parse DFT outputs to CNGNet readable formats
from chgnet.utils import parse_vasp_dir

dataset_dict = parse_vasp_dir(
    base_dir=r"C:\Users\Work\Desktop\Projects\UCT\data\New_opt_p3x3\COgas"
)

print(dataset_dict.items())