from ase.io import read, write # noqa
from ase.visualize import view # noqa
from ase import Atom, Atoms # noqa

from src.database import db # noqa
import time


def get_cell_size(a: Atoms) -> list:
    s = str(a.cell.bandpath())
    list_s = list(map(lambda x: x.strip(), s.split(",")))
    for j in list_s:
        if "cell" in j:
            k = j.split("=")[1]
            return list(map(lambda x: int(x), (
                k.replace("[", "").replace("]", "").split("x"))))


def test():
    for i in db.get_all_outcar():
        path: Atoms = read(i[0] + "/CONTCAR")
        get_cell_size(path)


def test_2():
    for i in db.get_all_outcar():
        path: Atoms = read(i[0] + "/OUTCAR")
        get_cell_size(path)


start = time.time()
test()
end = time.time()
print(f'Time taken: {end - start:.6f} seconds')
start = time.time()
test_2()
end = time.time()
print(f'Time taken: {end - start:.6f} seconds')

