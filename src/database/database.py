import sqlite3
try:
    from . import sqlstatements
    from . import data_classes
except ImportError:
    import sqlstatements
    import data_classes
from pathlib import Path
import random


class SqliteDataBase:
    def __init__(self, connection_string="./data/") -> None:
        Path(connection_string).mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(connection_string + "db.db")

    def create_tables(self):
        cursor = self.connection.cursor()

        for name, statement in sqlstatements.CREATE_TABLE.items():
            cursor.execute(statement)

    # region INSERTS
    def add_atom(self, atom: data_classes.Atom):
        cursor = self.connection.cursor()
        if atom is None:
            return
        try:
            cursor.execute(sqlstatements.ADD_ITEMS.get("atom"),
                           (atom.atom_id, atom.atom_name))
        except Exception as e:
            print(f"failed: {e}")
        else:
            self.connection.commit()

    def add_tuning(self, tunning: data_classes.Tunning):
        cursor = self.connection.cursor()
        if tunning.adsorbate_1 is None:
            adsorbate_1 = None
        else:
            adsorbate_1 = tunning.adsorbate_1.atom_id

        if tunning.adsorbate_2 is None:
            adsorbate_2 = None
        else:
            adsorbate_2 = tunning.adsorbate_2.atom_id

        if tunning.adsorbate_3 is None:
            adsorbate_3 = None
        else:
            adsorbate_3 = tunning.adsorbate_3.atom_id

        if tunning.surface is None:
            surface = None
        else:
            surface = tunning.surface.atom_id

        name = tunning.outcar_path.replace("\\", "/").split("/")[-1]

        try:
            cursor.execute(sqlstatements.ADD_ITEMS.get("tune"),
                           (tunning.tunning_id, name, surface,
                            adsorbate_1, adsorbate_2, adsorbate_3,
                            tunning.Energy,
                            tunning.outcar_path, tunning.training))
        except Exception as e:
            print(f"failed: {e}")
        else:
            self.connection.commit()

    def add_position(self, pos: data_classes.Position):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sqlstatements.ADD_ITEMS.get("position"),
                           (pos.position_id, pos.atom.atom_id,
                            pos.tunning.tunning_id, pos.x,
                            pos.y, pos.z,
                            pos.position_type))
        except Exception as e:
            print(f"failed: {e}")
        else:
            self.connection.commit()

    def add_force(self, force: data_classes.Force):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sqlstatements.ADD_ITEMS.get("force"),
                           (force.force_id, force.atom.atom_id,
                            force.tunning.tunning_id, force.x,
                            force.y, force.z))
        except Exception as e:
            print(f"failed: {e}")
        else:
            self.connection.commit()

    # endregion

    # region SEARCHES
    def search_atom_id(self, atom_name: str) -> str:
        cursor = self.connection.cursor()
        cursor.execute(sqlstatements.SEARCH_IDS.get("atom"), (atom_name,))

        result = cursor.fetchone()

        return result

    def search_outcar_file(self, path: str) -> str:
        cursor = self.connection.cursor()
        cursor.execute(sqlstatements.SEARCH_OUTCAR_PATH, (path,))

        result = cursor.fetchall()

        return result

    def search_outcar_file_train(self, training: bool = True):
        cursor = self.connection.cursor()
        cursor.execute(sqlstatements.SEARCH_OUTCAR_TRAIN_PATH, (training,))

        result = cursor.fetchall()

        return result

    def search_outcar_energy(self, training: bool = False) -> list:
        cursor = self.connection.cursor()
        cursor.execute(sqlstatements.SEARCH_OUTCAR_ENERGY, (training, ))

        results = cursor.fetchall()

        return results

    def get_energy(self, name: str) -> float:
        cursor = self.connection.cursor()
        cursor.execute("SELECT energy FROM tuning WHERE name = ?", (name,))
        results = cursor.fetchone()

        return results

    def get_atom_count(self, name: str) -> int:
        cursor = self.connection.cursor()
        cursor.execute("SELECT tuning_id FROM tuning WHERE name = ?", (name,))
        uid = cursor.fetchone()[0]
        cursor.execute("SELECT count(*) FROM position WHERE tuning_id = ?",
                       (uid,))
        count = cursor.fetchone()[0]
        print(count)
        return count

    def get_all_outcar(self):
        cursor = self.connection.cursor()
        cursor.execute(sqlstatements.SEARCH_ALL_OUTCAR)
        return cursor.fetchall()

    # endregion
    # region Update
    def randomize_tunning(self, prob_train: int = 80, prob_test: int = 20):
        cursor = self.connection.cursor()
        cursor.execute(sqlstatements.RANDOMIZE_TRAINING.get("Get_rows"))
        rows = cursor.fetchall()

        for row in rows:
            cursor.execute(sqlstatements.RANDOMIZE_TRAINING.get("randomize"),
                           (random.choices([True, False],
                                           [prob_train, prob_test])[0],
                            row[0]))

    # endregion
    # region Delete
    def clear_database(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE tuning")
        cursor.execute("DROP TABLE atom")
        cursor.execute("DROP TABLE position")
        cursor.execute("DROP TABLE force")
        self.create_tables()
    # endregion


db = SqliteDataBase()
db.create_tables()
