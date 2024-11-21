from . import get_data, util


class ResponseHandler:
    LOAD_DATA = ["load"]
    def __init__(self) -> None:
        pass

    def handler(self, command:str):
        
        if command in self.LOAD_DATA:
            self.load_data()
    
    def load_data(self):
        multiple = input("Recursively Search directory [Y/n]> ").lower()

        if multiple == "y":
            path = input("Path> ")
            data = []
            for folder in util.scandir(path):
                outcar = get_data.get_file(folder)

                if outcar is not None:
                    data.append(get_data.get_data(outcar))
        else:
            outcar = get_data.get_file(path)

            if outcar is not None:
                data = get_data.get_data(outcar)
        print(data) 