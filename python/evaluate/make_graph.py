from matplotlib import pyplot
import yaml
import pandas
import seaborn
from os import makedirs
from pathlib import Path
pyplot.rcParams['font.size'] = 12

def make_graph(file_name: str):
    data_dict = yaml.safe_load(open(file_name, 'r'))
    xlabel: str = data_dict['x_label']
    xaxis = data_dict['x']
    methods: list[str] = data_dict['method']
    grapg_name: str = data_dict['name']

    data = pandas.DataFrame({'method': [], 'parameter': [], 'makespan': []})
    #colors = ['#40ff40', '#40c0ff', '#ffc0c0', '#c0ffff']


    idx: int = 0
    for method in methods:
        for x in xaxis:
            for v in data_dict['data'][method][x]:
                data.loc[str(idx)] = [method, x, v]
                idx += 1

    #print(data)
    #fig = pyplot.figure(figsize=(6.4,4.8))
    fig = pyplot.figure(figsize=(9.6,4.8))

    plot = seaborn.boxplot(x='parameter', y='makespan', hue='method', data=data, palette='Blues')
    plot.yaxis.set_major_formatter(pyplot.FuncFormatter(lambda x, loc: '{:,}'.format(int(x))))
    plot.set_xlabel(xlabel)
    #pyplot.legend(bbox_to_anchor=(1, 1.01), loc='lower right')
    pyplot.legend(bbox_to_anchor=(1.01, 1.), loc='upper left')
    plot.legend_.set_title('')
    pyplot.subplots_adjust(right=0.6)
    #pyplot.subplots_adjust(top=0.8)

    dst_dir = Path(__file__ + f'/../../../Image/{grapg_name}.png').parent
    makedirs(dst_dir, exist_ok=True)

    fig.savefig(__file__ + f'/../../../Image/{grapg_name}.png')
    fig.savefig(__file__ + f'/../../../Image/{grapg_name}.pdf')
