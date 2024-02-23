from numpy import average
import pandas
from typing import Callable

# あんまり綺麗な実装じゃないです
def speedup_table(data_dict: dict, xaxis: list, methods: list[int], func: Callable[[list[int]], float] = average):
    data = pandas.DataFrame({method: [] for method in methods})
    for x in xaxis:
        speedups: list[float] = []
        for method in methods:
            method_average: float = func(data_dict[method][x])
            workload_average: float = func(data_dict['Work-load'][x])
            speedups.append(workload_average/method_average)

        data.loc[x] = speedups

    return data