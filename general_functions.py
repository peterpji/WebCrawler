import os
import json
import logging
from urllib.parse import urljoin
from urllib.parse import urlparse


def create_file(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.mkdir(directory)

    if not os.path.exists(file_path):
        print("Opening file " + file_path)
        with open(file_path, "w"):
            pass


def import_file_to_set(path):
    results = set()
    with open(path, "r") as file_:
        for line in file_:
            results.add(line.replace("\n", ""))
    return results


def export_set_to_file(export_set, path):
    with open(path, "w") as file_:
        for item in sorted(export_set):
            file_.write(str(item) + "\n")
