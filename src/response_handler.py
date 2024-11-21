from . import get_data, util
import alive_progress


class ResponseHandler:
    LOAD_DATA = ["load"]
    def __init__(self) -> None:
        self.data = []

    def handler(self, command:str):
        
        if command in self.LOAD_DATA:
            self.load_data()
    
    def load_data(self):
        multiple = input("Recursively Search directory [Y/n]> ").lower()

        if multiple == "y":
            path = input("Path> ")
            self.data = []
            folders = util.scandir(path)
            with alive_progress.alive_bar(len(folders)) as bar:
                for folder in folders:
                    try:
                        outcar = get_data.get_file(folder)

                    except FileNotFoundError:
                        bar()
                        continue
                    else:
                        self.data.append(get_data.get_data(outcar))
                        bar()
        else:
            outcar = get_data.get_file(path)

            if outcar is not None:
                self.data = [get_data.get_data(outcar)]
        print(self.data) 