import torch
from dgl.nn import GatedGraphConv, GlobalAttentionPooling
from torch import nn
import torch.nn.functional as f
import dgl

class GGNNGAP(nn.Module):
    def __init__(self, input_dim, output_dim, max_edge_types, num_steps=4):
        super(GGNNGAP, self).__init__()
        self.inp_dim = input_dim
        self.out_dim = output_dim
        self.max_edge_types = max_edge_types
        self.num_timesteps = num_steps
        # Feature reduction layer
        self.linear = nn.Linear(input_dim, output_dim)
        pooling_gate_nn = torch.nn.Linear(self.out_dim, 1)
        self.pooling = GlobalAttentionPooling(pooling_gate_nn)
        self.ggcn = GatedGraphConv(in_feats=output_dim, out_feats=output_dim, n_steps=num_steps,
                                   n_etypes=max_edge_types)
        self.classifier = nn.Linear(in_features=self.out_dim, out_features=2)

    def forward(self, graph):

        node_features = graph.ndata['feat']
        edges = graph.edata['etype']
        node_features = self.linear(node_features)
        out = self.ggcn(graph, node_features, edges)
        out = self.pooling(graph, out)
        result = self.classifier(out)
        
        return result