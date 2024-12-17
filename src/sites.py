try:
    from .database import db
except ImportError:
    from database import db # noqa
from typing import Literal


def get_site_type(tune_id) -> Literal["A-top", "hcp", "fcc", "bridge", "4fh"]:
    atoms = db.get_atoms(tune_id)
    atoms_positions = {}

    for atom in atoms:
        atoms_positions[atom] = db.get_atom_positions(tune_id, atom)

    return atoms_positions


def get_tuning_with_surface(surface: str) -> list[str]:
    tunes = db.get_tune_from_surface(surface)
    for tune in tunes:
        print(get_site_type(tune[0]))


print(get_tuning_with_surface("Pt111"))
