import os


def find_file_like(directory: str, filename: str) -> list:
    '''
    Gets files with similar names
    '''
    result = []
    for root_dir, directories, files in os.walk(directory):
        for file in files:
            if filename in file:
                result.append(file)

    return result


def file_not_found(path: str) -> str:
    raise FileNotFoundError(f"{path} was not found, \
                            Please enter a different path")


def scandir(dirname):
    sub_folders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(sub_folders):
        sub_folders.extend(scandir(dirname))
    return sub_folders
