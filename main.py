from src.response_handler import ResponseHandler
from pathlib import Path

def main():
    Path("./data/").mkdir(parents=True, exist_ok=True)
    running = True
    handler = ResponseHandler()
    while running:
        command = input("Enter command> ").lower()

        if command in ["q", "quit", "close", 'stop']:
            running = False
        else:
            handler.handler(command)

if __name__ == "__main__": 
    main()
