"""Helper functions for finding a file."""

import os


def _walk_to_root(path: str):
    while True:
        if os.path.exists(os.path.join(path, ".git")):
            return path
        path = os.path.dirname(path)
        if path == "/":
            return None


def find(filename: str) -> str:
    """
    Find a file in the project.

    Parameters
    ----------
    filename : str
        The name of the file to find.

    Returns
    -------
    str
        The full path to the file. Empty string if not found.
    """
    root = _walk_to_root(os.path.dirname(__file__))
    if root is None:
        return ""
    for current_root, _, files in os.walk(root):
        if filename in files:
            return os.path.join(current_root, filename)
        if filename in files:
            return os.path.join(root, filename)
    return ""
