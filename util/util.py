import os


def add_input_cwd(file_name):
    return os.path.join(os.getcwd(), 'data', 'input', file_name)


def add_output_cwd(file_name):
    return os.path.join(os.getcwd(), 'data', 'output', file_name)
