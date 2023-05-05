from dgl.data import DGLDataset
import torch
import pandas as pd
import dgl
from utils.io import load_nx_from_json
import networkx as nx
import os
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class ConcordDataset(DGLDataset):
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
                 df,
                 args,
                 url=None,
                 raw_dir=None,
                 save_dir=None,
                 force_reload=False,
                 verbose=False):
        self.root = args.root
        self.tokenizer = args.tokenizer
        self.w_embeddings = args.embeddings
        self.edge_mapping = args.edge_mapping
        self.repr = args.repr
        self.labels = df['label'].tolist()
        # For Classes:
        #self.graphs = df[f'{self.repr}_classe'].tolist()
        self.projects = df['project'].tolist()
        self.graphs = df[f'{self.repr}'].tolist()
        self.split_name = df['split'].iloc[0]
        print(f"Number of {self.split_name} instances: {len(self.labels)}")
 
        super(ConcordDataset, self).__init__(name=f'concord_{self.split_name}',
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
        graph = self.graphs[idx]

        file_path = os.path.join(f"{self.root}/{self.repr.upper()}", self.projects[idx],  graph)
        
        nx_graph = load_nx_from_json(file_path)
        label = self.labels[idx]

        # Get the 'code' attribute for all nodes in the graph
        code_dict = nx.get_node_attributes(nx_graph, 'code')

        # Encode the node codes using the tokenizer
        node_codes = list(code_dict.values())
        encoded_nodes = self.tokenizer(node_codes, add_special_tokens=True, padding='longest', truncation=True, return_tensors='pt')
        encoded_nodes = encoded_nodes['input_ids']

        # Generate node features using the CodeBERT model embedding layer
        num_nodes = encoded_nodes.size(0)
        #assert num_nodes == nx_graph.number_of_nodes()
        feat = []
        for i in range(num_nodes):
          # Creating feature vector for one node
            node_features = []
            node_tokens = encoded_nodes[i].size(0)
            for k in range(node_tokens):
                embd = torch.tensor(self.w_embeddings[encoded_nodes[i][k]])
                node_features.append(embd)
            # Stack on top of each other
            node_features = torch.stack(node_features, dim=0)
            # Take mean so that a node is represented by one vector (1, 768)
            node_features = torch.mean(node_features, dim=0)
            # Add to graph nodes' feature matrix
            feat.append(node_features) # at the end (num_nodes, 768)
        
        
        feat = torch.stack(feat, dim=0)
        
        # Encode edges
        for i, e in enumerate(nx_graph.edges(data=True, keys=True)):
            u, v, k, data = e
            nx_graph[u][v][k]['etype'] = self.edge_mapping[data['label']]
            nx_graph[u][v][k]['eid'] = i

        # Convert from networkx to DGL
        dgl_graph = dgl.from_networkx(nx_graph, edge_attrs=['etype'], edge_id_attr_name='eid')

        # Add node feature
        dgl_graph.ndata['feat']  = feat
        
        
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
