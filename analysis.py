import json, csv
import pandas as pd

def load_data(file):
    with open(file) as fp:
        data = json.load(fp)

    df = pd.DataFrame(data)

    return  df




if __name__ == '__main__':
    load_data('yi_k3.json')