import pandas as pd
import torch
import numpy as np

def static_splitter(src):
    _df = pd.read_csv(src)
    col_name = 'split'
    splits = []

    for split in ['train', 'test', 'val']:
        splits.append(_filter_by_col(_df, col_name, split))

    return splits
    

def _filter_by_col(df, col, val):
    return df[df[col] == val]


def torch_setup(seed=4096):
    seed = seed
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False