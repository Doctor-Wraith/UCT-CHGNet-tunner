from src.response_handler import ResponseHandler
def main():
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