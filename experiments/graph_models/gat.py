import torch
from dgl.nn import GATConv
from torch import nn
import torch.nn.functional as f
import dgl

class GAT(nn.Module):
    def __init__(self, input_dim, output_dim, attention_heads, feat_dp, attention_dp ,read_out):
        super(GAT, self).__init__()
        self.read_out = read_out
        self.inp_dim = input_dim
        self.out_dim = output_dim
        self.num_heads = attention_heads
        self.feat_drop = feat_dp
        self.attn_drop = attention_dp
        # Feature reduction layer
        self.reduction_linear = nn.Linear(input_dim, output_dim)
        self.dropout = nn.Dropout(.2)

        # GAT Config
        self.gat =  GATConv(
                                    in_feats=self.inp_dim,
                                    out_feats=self.out_dim,
                                    num_heads=self.num_heads,
                                    feat_drop=self.feat_drop,
                                    attn_drop=self.attn_drop,
                                    allow_zero_in_degree=True
                                    )
        self.gat_layer_activation = nn.LeakyReLU()

        self.classifier = nn.Linear(in_features=self.out_dim, out_features=2)


    def forward(self, graph):

        node_features = graph.ndata['feat']
        node_features = self.dropout(self.reduction_linear(node_features))
        
        out = self.gat(graph, node_features)
        out = self.gat_layer_activation(out)
        out = torch.mean(out, dim=1) # Because we have multiple attention heads
        
        graph.ndata['h'] = out
        
        if self.read_out == 'sum':
            feats = dgl.sum_nodes(graph, 'h')
        if self.read_out == 'mean':
            feats = dgl.mean_nodes(graph, 'h')

        result = self.classifier(feats)
        
        return result