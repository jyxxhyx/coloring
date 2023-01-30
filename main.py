
from util.util import add_input_cwd, add_output_cwd
from input_handler.reader import read_graph_from_file
from output_handler.writer import write_result
from model import poph, assign, pop, heuristics
from config_env import get_configuration


def main():
    config = get_configuration('config_local.yaml')
    # Solve multiple instances
    for input_file, output_file in zip(config['input_files'], config['output_files']):
        graph = read_graph_from_file(add_input_cwd(input_file))
        upper_bound = heuristics.random_coloring(graph)
        print(f'{input_file}: {upper_bound}')
        models = {'assign': assign.AssignModel, 'pop': pop.PopModel, 'poph': poph.PophModel}

        for name, Model in models.items():
            config['model_name'] = f'{name}_{input_file}'
            output_name = f'{name}_{output_file}'
            model = Model(graph, config, upper_bound=upper_bound)
            result = model.solve()
            write_result(add_output_cwd(output_name), result)
    return


if __name__ == '__main__':
    main()

