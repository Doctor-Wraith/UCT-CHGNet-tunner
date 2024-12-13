try:
    from .database import db
    from .database.data_classes import Atom
except ImportError:
    from database import db
    from database.data_classes import Atom
import numpy as np
import uuid
import alive_progress


LATTICE = {
    "Pt": 3.9242
}


def get_posses(surface: str) -> dict:
    tunes = db.search_incomplete_surface_tune(surface=surface)
    out = []
    for tune in tunes:
        layers_all: dict = {}
        posses = db.search_pos_atom_tune(tune[0], tune[1])
        for pos in posses:
            if layers_all == {}:
                layers_all[1] = [pos[2]]
            else:
                found = False
                for i, j in layers_all.items():
                    if j[0] - 0.3 <= pos[2] and pos[2] <= j[0] + 0.3:
                        layers_all[i].append(pos[2])
                        found = True

                if not found:
                    layers_all[i+1] = [pos[2]]
        layers_avg = {}
        for i, j in layers_all.items():
            layers_avg[i] = sum(j)/len(j)
            # layers_avg[i] = j[0]

        out.append(layers_avg)
    return out, tunes


def type_of_surface(positions: dict, surface_type: str,
                    h_max: int = 10, k_max: int = 10, l_max: int = 10) -> str:
    distance = positions[2] - positions[1]
    found = False
    for l in range(l_max+1): # noqa
        for k in range(k_max+1):
            for h in range(h_max+1):
                try:
                    eq = LATTICE.get(surface_type, 0) / ((h**2 + k ** 2 + l ** 2) ** (1/2)) # noqa
                except ZeroDivisionError:
                    eq = 0
                if distance - 0.005 <= eq and eq <= distance + 0.005:
                    found = True
                    break
            if found:
                break
        if found:
            break
    if not found:
        return (False, eq, distance)
    else:
        min_value = np.inf
        if h < min_value and h != 0:
            min_value = h
        if k < min_value and k != 0:
            min_value = k
        if l < min_value and l != 0:
            min_value = l

        h, k, l = str(int(h/min_value)), str(int(k/min_value)), str(int(l/min_value)) # noqa
    return (h, k, l)


def update_db():
    posses, id_s = get_posses("Pt")
    with alive_progress.alive_bar(len(posses)) as bar:
        for pos, id_ in zip(posses, id_s):
            tune_id = id_[0]
            Pt_id = id_[1]

            Pt_new = f"Pt{''.join(type_of_surface(pos, 'Pt'))}"

            if db.search_atom_id(Pt_new) is None:
                Pt_new_id = uuid.uuid4().hex
                db.add_atom(Atom(Pt_new_id, Pt_new))

                db.update_surface(Pt_id, tune_id, Pt_new_id)
            else:
                Pt_new_id = db.search_atom_id(Pt_new)[0]
                db.update_surface(Pt_id, tune_id, Pt_new_id)

            bar()
