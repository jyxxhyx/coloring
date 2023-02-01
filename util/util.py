import os


def add_input_cwd(file_name):
    path = os.path.dirname(__file__)
    parent_path = os.path.dirname(path)
    return os.path.join(parent_path, 'data', 'input', file_name)


def add_output_cwd(file_name):
    path = os.path.dirname(__file__)
    parent_path = os.path.dirname(path)
    return os.path.join(parent_path, 'data', 'output', file_name)
