from output_handler.analyzer import GurobiAnalyzer, InstanceAnalyzer
from util.util import add_input_cwd, add_output_cwd, add_logs_cwd
from input_handler.reader import read_graph_from_file
from output_handler.writer import write_result
from model import poph, assign, pop, heuristics
from config_env import get_configuration


def main():
    config = get_configuration('config_large.yaml')
    analyzer = GurobiAnalyzer('result.csv')
    instance_analyzer = InstanceAnalyzer('instance.csv')
    models = {'assign': assign.AssignModel, 'pop': pop.PopModel, 'poph': poph.PophModel}
    
    # Solve multiple instances
    for input_file in config['input_files']:
        output_file = input_file.replace('.col', '.sol')
        graph = read_graph_from_file(add_input_cwd(input_file))
        lower_bound = _get_lower_bound(graph, config['is_lb_added'])
        upper_bound = _get_upper_bound(graph, config['is_ub_added'])
        instance_analyzer.add_record(input_file, len(graph.get_nodes()), len(graph.get_edges()), upper_bound,
                                     lower_bound)
        print(f'{input_file}: {upper_bound}, {lower_bound}')

        for model_name, Model in models.items():
            instance_key = f'{model_name}_{input_file}'
            config['model_name'] = instance_key
            output_name = f'{model_name}_{output_file}'
            # JIC you encountered the Gurobi error of writing log (on Windows platform),
            # change the log file to the default gurobi.log.
            # The code is still able to parse the log correctly.
            # log_file = 'gurobi.log'
            log_file = add_logs_cwd(f'{instance_key}.log')
            config['log_file'] = log_file
            model = Model(graph, config, upper_bound=upper_bound, lower_bound=lower_bound)
            result = model.solve()
            write_result(add_output_cwd(output_name), result)
            analyzer.parse_log(log_file, model=model_name, instance=input_file,
                               is_iteration_parsed=config.get('parse_iter', None))
    analyzer.write_summary()
    instance_analyzer.write_summary()
    return


def _get_lower_bound(graph, lb_config):
    if lb_config == 'exact':
        return graph.max_clique()
    elif lb_config == 'greedy':
        lower_bound, _ = heuristics.find_clique(graph)
        return lower_bound
    else:
        return None


def _get_upper_bound(graph, ub_config):
    if ub_config is True:
        return heuristics.random_coloring(graph)
    else:
        return None


if __name__ == '__main__':
    main()
