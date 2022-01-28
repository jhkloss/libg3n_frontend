import os
from .library import Library
from flask import render_template


def get_libraries(root_path: str) -> dict:
    result = {}
    obj = os.scandir(path=root_path)
    for entry in obj:
        if entry.is_dir():
            result[entry.name] = Library(entry.name, entry.path)
    return result


def get_libraries_table_html(root_path: str) -> str:
    result = ''

    for library in get_libraries(root_path):
        result += render_template('library_entry.html', library=library)

    return result