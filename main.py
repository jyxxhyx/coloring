from output_handler.analyzer import Analyzer
from util.util import add_input_cwd, add_output_cwd, add_logs_cwd
from input_handler.reader import read_graph_from_file
from output_handler.writer import write_result
from model import poph, assign, pop, heuristics
from config_env import get_configuration


def main():
    config = get_configuration('config_local_large.yaml')
    analyzer = Analyzer()
    # Solve multiple instances
    for input_file, output_file in zip(config['input_files'], config['output_files']):
        graph = read_graph_from_file(add_input_cwd(input_file))
        # lower_bound, _ = heuristics.find_clique(graph)
        lower_bound = graph.max_clique()
        upper_bound = heuristics.random_coloring(graph)
        print(f'{input_file}: {upper_bound}, {lower_bound}')
        models = {'assign': assign.AssignModel, 'pop': pop.PopModel, 'poph': poph.PophModel}

        for name, Model in models.items():
            instance_key = f'{name}_{input_file}'
            config['model_name'] = instance_key
            output_name = f'{name}_{output_file}'
            model = Model(graph, config, upper_bound=upper_bound, lower_bound=lower_bound)
            result = model.solve()
            write_result(add_output_cwd(output_name), result)
            analyzer.parse_log(add_logs_cwd(f'{instance_key}.log'), instance_key)
    analyzer.write_summary()
    return


if __name__ == '__main__':
    main()

