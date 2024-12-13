try:
    from .database import db
except ImportError:
    from database import db


LATTICE = {
    "Pt": 3.9242
}


def get_posses(surface: str) -> dict:
    tunes = db.search_incomplete_surface_tune(surface=surface)
    out = []
    for tune in tunes:
        layers_all: dict = {}
        print(tune)
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

        print(layers_all)
        layers_avg = {}
        for i, j in layers_all.items():
            layers_avg[i] = sum(j)/len(j)
            # layers_avg[i] = j[0]

        print(layers_avg)
        out.append(layers_avg)

        print()
    return out, tunes


def type_of_surface(positions: dict, surface_type: str,
                    h_max: int = 10, k_max: int = 10, l_max: int = 10) -> str:
    distance = positions[2] - positions[1]
    found = False
    for l in range(l_max+1):
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
    return ((h, k, l), eq, distance)


a, d = get_posses("Pt")
l = []
with open("test.txt", "w") as output:
    for b, g in zip(a, d):
        s = type_of_surface(b, "Pt")
        l.append(s)
        # print(db.search_outcar_from_id(g[0]))
        # print(s)
        k = f"{db.search_outcar_from_id(g[0])}: \t\t\t {s}"
        print(k)
        output.write(k + "\n")

# print(l)
