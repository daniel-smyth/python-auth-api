import os
from pathlib import Path
from typing import List

ROOT_PATH: Path = Path(__file__).resolve().parents[1]


def get_root():
    """Get root directory"""

    return ROOT_PATH


def create_dir(name: str):
    """
    Create a directory

    Args:
       - `name`: Directory name
    """
    os.makedirs(name) if os.path.exists(ROOT_PATH / name) is False else None
    download_dir: Path = ROOT_PATH / name

    return download_dir


def delete_dir(path: Path):
    """
    Delete a directory and its containing files

    Args:
       - `name`: Directory path
    """
    try:
        files = list(path.iterdir())

        for file_name in files:
            file_name.unlink()

        Path.rmdir(path)
    except Exception:
        pass


def delete_dir_files(path: Path):
    """
    Delete a directory's containing files

    Args:
       - `name`: Directory path
    """
    files = list(path.iterdir())

    for file_name in files:
        file_name.unlink()


def select_from_dir(name: str, dir_path: str = None):
    """
    Select file from a directory

    Args:
       - `selected`: String containing file name
       - `path`: Path to directory
    """
    all_files = list((get_root() / dir_path).iterdir())

    for file in all_files:
        # file name with extension
        file_name = os.path.basename(file)

        # file name without extension
        file_name_no_extension = os.path.splitext(file_name)[0]

        if file_name_no_extension == name:
            return file


def select_list_from_dir(names: List[str], path: str = None):
    """
    Select list of files from a directory

    Args:
       - `name`: List of file names
       - `path`: Path to directory
    """
    all_files = list((get_root() / path).iterdir())

    if path is None:
        return all_files

    selected_files = []

    for file in all_files:
        for selected_file in names:
            if selected_file in file.__str__():
                selected_files.append(file)

    return selected_files
