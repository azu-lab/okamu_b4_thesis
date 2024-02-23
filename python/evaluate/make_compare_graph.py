from matplotlib import pyplot
from pandas import DataFrame
from numpy import array, argmin
import yaml
from os import makedirs
from pathlib import Path

def make_compare_graph(file_name: str):
    data_dict = yaml.safe_load(open(file_name, 'r'))
    xlabel: str = data_dict['x_label']
    xaxis = data_dict['x']
    methods: list[str] = data_dict['method']
    grapg_name: str = data_dict['name']

    data = DataFrame({method: [] for method in methods + ['Equivalence']})
    #colors = ['#40ff40', '#40c0ff', '#ffc0c0', '#c0ffff']

    for x in xaxis:
        values: list[list[int]] = []

        for method in methods:
            values.append(data_dict['data'][method][x])

        eva: list[int] = [0 for _ in methods + ['Equivalence']]

        values_t: list[list[int]] = array(values).T.tolist()
        for value_row in values_t:
            min_idx: int = argmin(value_row)

            if len([v for v in value_row if v == value_row[min_idx]]) != 1:
                if 'Equivalence' in methods:
                    eva[-1] += 1
            else:
                eva[min_idx] += 1

        data.loc[x] = eva

    print(data)

    pyplot.figure()

    data.plot.bar(stacked=True, edgecolor='black', linewidth=1, cmap='Blues')
    pyplot.subplots_adjust(bottom=0.2)
    pyplot.xlabel(xlabel)
    pyplot.ylabel('count')

    dst_dir = Path(__file__ + f'/../../../Image/Compare/{grapg_name}.png').parent
    makedirs(dst_dir, exist_ok=True)

    pyplot.savefig(__file__ + f'/../../../Image/Compare/{grapg_name}.png')
    pyplot.savefig(__file__ + f'/../../../Image/Compare/{grapg_name}.png')