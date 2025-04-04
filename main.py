from pathlib import Path
from src.util import logger
from src import util
from src.help import help
import os


def create_folders():
    folders_needed = [
        "./data/",
        "./data/chgnet",
        "./data/chgnet/models",
        "./data/chgnet/json",
        "./data/chgnet/json/train",
        "./data/chgnet/json/test",
        "./data/OUTCAR",
        "./output",
        "./output/graphs"
    ]
    logger.info("File Checker", "Checking if Folders exists",
                False)

    for folder in folders_needed:
        if not Path(folder).is_dir():
            logger.warn("File Checker", f"folder '{folder}' does not exists",
                        False)
            Path(folder).mkdir(parents=True, exist_ok=True)
            logger.info("File Checker", f"folder '{folder}' was created",
                        False)


def main():
    logger.info("Start", "Starting Setup",
                False)
    create_folders()
    from src.response_handler import ResponseHandler
    # Make sure that the console clears no matter which OS is used
    os.system("clear") | os.system("cls")
    running = True
    handler = ResponseHandler()
    logger.info("Start", "Starting",
                False)
    while running:
        command = util.get_input("Enter command> ").lower().strip()

        if command in ["q", "quit", "close", 'stop']:
            logger.info("main", "Stopping")
            running = False
        elif "help" in command:
            cmd = command.split()
            try:
                help.get_help(cmd[1])
            except IndexError:
                help.list_commands()
        else:
            handler.handler(command)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("main", "CRASHING")
        logger.error("main", e)
