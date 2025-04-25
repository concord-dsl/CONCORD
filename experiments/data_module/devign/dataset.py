from dgl.data import DGLDataset
import torch
import pandas as pd
import dgl
from utils.io import load_nx_from_dict
import networkx as nx
import os
from utils.io import read_json 
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class DevignDataset(DGLDataset):
    """ Template for customizing graph datasets in DGL.
    Parameters
    ----------
    url : str
        URL to download the raw dataset
    raw_dir : str
        Specifying the directory that will store the
        downloaded data or the directory that
        already stores the input data.
        Default: ~/.dgl/
    save_dir : str
        Directory to save the processed dataset.
        Default: the value of `raw_dir`
    force_reload : bool
        Whether to reload the dataset. Default: False
    verbose : bool
        Whether to print out progress information
    """
    def __init__(self,
                 data_file,
                 split_name,
                 args,
                 url=None,
                 raw_dir=None,
                 save_dir=None,
                 force_reload=False,
                 verbose=False):
        
        self.data = read_json(data_file)
        self.tokenizer = args.tokenizer
        self.edge_mapping = args.edge_mapping
        self.repr = args.repr
        print(f"Number of {self.split_name} instances: {len(self.data)}")
 
        super(DevignDataset, self).__init__(name=f'devign_{split_name}',
                                           url=url,
                                           raw_dir=raw_dir,
                                           save_dir=save_dir,
                                           force_reload=force_reload,
                                           verbose=verbose)

    def download(self):
        # download raw data to local disk
        pass

    def process(self):
        pass

    def __getitem__(self, idx):

        data_point = self.data[idx]
        nx_graph = load_nx_from_dict(data_point)
        label = data_point['target']
        label = torch.tensor(label, device=self.args.device)

        # Get the 'code' attribute for all nodes in the graph
        code_dict = nx.get_node_attributes(nx_graph, 'code')

        # Encode the node codes using the tokenizer
        node_codes = list(code_dict.values())
        encoded_nodes = self.tokenizer(node_codes, add_special_tokens=True, padding='longest', truncation=True, return_tensors='pt')
        encoded_nodes = encoded_nodes['input_ids']

        
        # Encode edges
        for i, e in enumerate(nx_graph.edges(data=True, keys=True)):
            u, v, k, data = e
            nx_graph[u][v][k]['etype'] = self.edge_mapping[data['label']]
            nx_graph[u][v][k]['eid'] = i

        # Convert from networkx to DGL
        dgl_graph = dgl.from_networkx(nx_graph, edge_attrs=['etype'], edge_id_attr_name='eid')

        # Add node feature
        dgl_graph.ndata['feat']  = torch.tensor(encoded_nodes, device=self.args.device)
        
        
        return dgl_graph, label

    def __len__(self):
        # number of data examples
        return len(self.graphs)

    @property
    def processed_file(self):
        pass

    @property
    def max_etypes(self):
        return 1

    def save(self):
        # save processed data to directory `self.save_path`
        pass

    def load(self):
        # load processed data from directory `self.save_path`
        pass

    def has_cache(self):
        # check whether there are processed data in `self.save_path`
        pass
