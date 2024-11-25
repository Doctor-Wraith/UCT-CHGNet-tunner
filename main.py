from src import get_data
from src.response_handler import ResponseHandler
from .src.database import db, data_classes
import uuid

def main():
    running = True
    handler = ResponseHandler()
    while running:
        command = input("Enter command> ").lower()

        if command in ["q", "quit", "close", 'stop']:
            running = False
        else:
            handler.handler(command)

def test():
    t = get_data.DataExtracter(r"D:\UCT Stuff\Projects\UCT\New_opt_p3x3\COgas")
    atom = data_classes.Atom()

if __name__ == "__main__": 
    test()