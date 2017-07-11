import json, csv
import numpy as np


def load_data(file):
    with open(file) as fp:
        data = json.load(fp)

    mat = np.asarray([list(map(int, item['number'].split())) for item in data])
    return  mat


if __name__ == '__main__':
    load_data('gxk3.json')