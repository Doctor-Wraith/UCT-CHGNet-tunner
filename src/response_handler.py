from . import get_data, util
import alive_progress
from typing import Literal
import json


class ResponseHandler:
    LOAD_DATA = ["load", "--l"]
    SAVE = ["out", "--o"]
    SAVE_LOCAL = ["save", '--s']
    def __init__(self) -> None:
        self.data = []

    def handler(self, command:str, *args):
        
        if command in self.LOAD_DATA:
            self.load_data()
        elif command in self.SAVE:
            self.save()
        elif command in self.SAVE_LOCAL:
            self.save_local(args)
    
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
                        outcar = get_data.DataExtracter(folder)

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
            outcar = get_data.DataExtracter(path)
            self.data = [outcar]


    def save(self):
        if self.data is not None:
            with alive_progress.alive_bar(len(self.data)) as bar:
                for data in self.data:
                    get_data.prep_data(data)
                    bar()
            

        else:
            print("Please load data")

    def save_local(self, *args):
        if len(args) == 2:
            with alive_progress.alive_bar(len(self.data)) as bar:
                for data in self.data:
                    data.save_outcar_file(args)
                    bar()
        elif len(args) == 1:
            with alive_progress.alive_bar(len(self.data)) as bar:
                for data in self.data:
                    data.save_outcar_file()
                    bar()
        else:
            raise Exception("To many Args")