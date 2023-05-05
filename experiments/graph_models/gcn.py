import torch
from dgl.nn import GraphConv
from torch import nn
import torch.nn.functional as f
import dgl

class GCN(nn.Module):
    def __init__(self, input_dim, output_dim, num_layers, read_out):
        super(GCN, self).__init__()
        self.read_out = read_out
        self.inp_dim = input_dim
        self.out_dim = output_dim
        self.num_layers = num_layers
        # Feature reduction layer
        self.reduction_linear = nn.Linear(input_dim, output_dim)
        self.dropout = nn.Dropout(.2)

        # GCN Config
        self.gcn_layers =  nn.ModuleList([GraphConv(self.out_dim, self.out_dim, allow_zero_in_degree=True) for _ in range(num_layers)])
        self.gcn_layer_activation = nn.LeakyReLU()

        self.classifier = nn.Linear(in_features=self.out_dim, out_features=2)

    def forward(self, graph):

        node_features = graph.ndata['feat']
        node_features = self.dropout(self.reduction_linear(node_features))
        for gcn in self.gcn_layers:
            out = self.gcn_layer_activation(gcn(node_features))
        
        graph.ndata['h'] = out
        
        if self.read_out == 'sum':
            feats = dgl.sum_nodes(graph, 'h')
        if self.read_out == 'mean':
            feats = dgl.mean_nodes(graph, 'h')

        result = self.classifier(feats)
        
        return result