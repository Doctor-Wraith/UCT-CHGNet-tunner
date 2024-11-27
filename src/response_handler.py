from . import data, util
import alive_progress


class ResponseHandler:
    LOAD_DATA = ["load", "--l"]
    SAVE_LOCAL = ["save", '--s']

    def __init__(self) -> None:
        self.data = []

    def handler(self, command: str, *args):

        if command in self.LOAD_DATA:
            self.load_data()
        elif command in self.SAVE_LOCAL:
            self.save_local()

    def load_data(self):
        multiple = input("Recursively Search directory [Y/n]> ").lower()

        if multiple == "y":
            path = input("Path> ")
            self.data = []
            folders = util.scandir(path)
            with alive_progress.alive_bar(len(folders)) as bar:
                for folder in folders:
                    try:
                        print(folder)
                        outcar = data.DataExtracter(folder)

                    except FileNotFoundError:
                        bar()
                        continue
                    except util.exceptions.NotCompleteOUTCAR:
                        bar()
                        continue
                    else:
                        self.data.append(outcar)
                        bar()
        else:
            path = input("Path> ")
            outcar = data.DataExtracter(path)
            self.data = [outcar]

    def save(self):
        if self.data is not None:
            for data in self.data:
                data.prep_data(data)

        else:
            print("Please load data")

    def save_local(self):
        local_save = input("Save local [Y/n]> ").strip().lower()

        if local_save == "y":
            with alive_progress.alive_bar(len(self.data)) as bar:
                for data in self.data:
                    try:
                        data.save_outcar_file()
                    except Exception:
                        pass
                    else:
                        self.save()
                    bar()
        else:
            with alive_progress.alive_bar(len(self.data)) as bar:
                for data in self.data:
                    self.save()
                    bar()
