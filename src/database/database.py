import sqlite3
try:
    from . import sqlstatements
    from . import data_classes
except ImportError:
    import sqlstatements
    import data_classes


class SqliteDataBase:
    def __init__(self, connection_string="./data/db.db") -> None:
        self.connection = sqlite3.connect(connection_string)

    def create_tables(self):
        cursor = self.connection.cursor()

        for name, statement in sqlstatements.CREATE_TABLE.items():
            cursor.execute(statement)
    
    # region ################# INSERTS #################
    def add_atom(self, atom: data_classes.Atom):
        cursor = self.connection.cursor()
        if atom is None: return
        try:
            cursor.execute(sqlstatements.ADD_ITEMS.get("atom"), (atom.atom_id, atom.atom_name))
        except Exception as e:
            print(f"falied: {e}")
        else:
            self.connection.commit()
    
    def add_tuning(self, tunning: data_classes.Tunning):
        cursor = self.connection.cursor()
        # adsorbate_1, adsorbate_2, adsorbate_3 = tunning.adsorbate_1.atom_id if tunning.adsorbate_1 is not None else None, tunning.adsorbate_2.atom_id if tunning.adsorbate_2 is not None else None, tunning.adsorbate_3.atom_id if tunning.adsorbate_3 is not None else None
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

        try:
            cursor.execute(sqlstatements.ADD_ITEMS.get("tune"),
                           (tunning.tunning_id, surface,
                            adsorbate_1, adsorbate_2, adsorbate_3,
                            tunning.Energy,
                            tunning.outcar_path, tunning.training))
        except Exception as e:
            print(f"falied: {e}")
        else:
            self.connection.commit()
    
    def add_position(self, pos:data_classes.Position):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sqlstatements.ADD_ITEMS.get("position"), 
                           (pos.position_id, pos.atom.atom_id,
                            pos.tunning.tunning_id, pos.x,
                            pos.y, pos.z,
                            pos.position_type))
        except Exception as e:
            print(f"falied: {e}")
        else:
            self.connection.commit()
    
    def add_force(self, force:data_classes.Force):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sqlstatements.ADD_ITEMS.get("force"),
                           (force.force_id, force.atom.atom_id,
                            force.tunning.tunning_id, force.x,
                            force.y, force.z))
        except Exception as e:
            print(f"falied: {e}")
        else:
            self.connection.commit()


    # endregion

    # region ################# SEARCHES #################

    def search_atom_id(self, atom_name:str) -> str:
        cursor = self.connection.cursor()
        cursor.execute(sqlstatements.SEARCH_IDS.get("atom"), (atom_name,))

        result = cursor.fetchone()

        return result

    def search_outcar_file(self, path:str) -> str:
        cursor = self.connection.cursor()
        cursor.execute(sqlstatements.SEARCH_OUTCAR_PATH, (path,))

        reslut = cursor.fetchall()

        return reslut
    
    # endregion


db = SqliteDataBase()
db.create_tables()