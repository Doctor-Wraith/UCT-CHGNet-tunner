from . import get_data, util
import alive_progress
from typing import Literal
import json


class ResponseHandler:
    LOAD_DATA = ["load"]
    SAVE = ["save"]
    def __init__(self) -> None:
        self.data = []

    def handler(self, command:str):
        
        if command in self.LOAD_DATA:
            self.load_data()
        elif command in self.SAVE:
            self.save('json')
    
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

    def save(self, type:Literal["json"]):
        if self.data is not None:
            
            if type == "json":
                with open("./data/out.json", 'w') as json_file:
                    json_file.write(json.dumps(self.data, indent=3))

        else:
            print("Please load data")