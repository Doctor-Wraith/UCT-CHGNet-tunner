import os
import random


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


def scandir(dirname):
    sub_folders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(sub_folders):
        sub_folders.extend(scandir(dirname))
    return sub_folders


def get_files(self, files: list, amount: int) -> list:
    """
    Gets a random assortment of files from a list

    Args:
        files (list): a list of folders
        amount (int): the amount of files wanted
    Returns:
        list: a random assortment of files
    Raises:
        ValueError: Raises a value Error
    """
    if len(files) < amount:
        raise ValueError(f"Amount: {amount} < File: {len(files)}")
    if len(files) == amount:
        return files
    else:
        out = random.sample(files, amount)
        return out
