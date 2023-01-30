

def write_result(file_name, result: dict):
    with open(file_name, mode='w', encoding='utf-8-sig') as f:
        f.write('node,color\n')
        for node, color in result.items():
            f.write(f'{node},{color}\n')
    return
