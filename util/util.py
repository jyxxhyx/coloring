import os

# The parent directory of the current file
BASE_PATH = os.path.dirname(os.path.dirname(__file__))


def add_input_cwd(file_name):
    return os.path.join(BASE_PATH, 'data', 'input', file_name)


def add_output_cwd(file_name):
    return os.path.join(BASE_PATH, 'data', 'output', file_name)


def add_logs_cwd(file_name):
    return os.path.join(BASE_PATH, 'data', 'logs', file_name)


def add_figure_cwd(file_name):
    return os.path.join(BASE_PATH, 'data', 'figure', file_name)
