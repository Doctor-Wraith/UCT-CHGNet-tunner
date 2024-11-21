from . import get_data, util


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
            for folder in util.scandir(path):
                try:
                    outcar = get_data.get_file(folder)

                except FileNotFoundError:
                    continue
                else:
                    self.data.append(get_data.get_data(outcar))
        else:
            outcar = get_data.get_file(path)

            if outcar is not None:
                self.data = [get_data.get_data(outcar)]
        print(self.data) 