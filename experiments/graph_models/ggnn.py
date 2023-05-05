import torch
from dgl.nn import GatedGraphConv
from torch import nn
import torch.nn.functional as f
import dgl

class GGNN(nn.Module):
    def __init__(self, input_dim, output_dim, max_edge_types, read_out, num_steps=8):
        super(GGNN, self).__init__()
        self.read_out = read_out
        self.inp_dim = input_dim
        self.out_dim = output_dim
        self.max_edge_types = max_edge_types
        self.num_timesteps = num_steps
        # Feature reduction layer
        self.linear = nn.Linear(input_dim, output_dim)
        self.dropout = nn.Dropout(.2)
        self.ggcn = GatedGraphConv(in_feats=output_dim, out_feats=output_dim, n_steps=num_steps,
                                   n_etypes=max_edge_types)
        self.classifier = nn.Linear(in_features=output_dim, out_features=2)

    def forward(self, graph):

        node_features = graph.ndata['feat']
        edges = graph.edata['etype']
        node_features = self.dropout(self.linear(node_features))
        out = self.ggcn(graph, node_features, edges)
        out = self.dropout(out)
        graph.ndata['h'] = out
        
        if self.read_out == 'sum':
            feats = dgl.sum_nodes(graph, 'h')
        if self.read_out == 'mean':
            feats = dgl.mean_nodes(graph, 'h')

        result = self.classifier(feats)
        
        return result