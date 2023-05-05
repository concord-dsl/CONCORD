import json, torch
import numpy as np
from networkx.readwrite import json_graph

def read_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def load_nx_from_json(file):
    with open(file) as f:
        return json_graph.node_link_graph(json.loads(f.read()))

def torch_setup(seed=4096):
    seed = seed
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False