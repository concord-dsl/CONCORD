import networkx as nx
from utils.last_write_read.NodeType import NodeType

from utils.last_write_read.NodeUtils import NodeUtils

def get_variable_occurences(graph: nx.MultiDiGraph, var: str):
    """Returns all IDENTIFIER nodes of var.
    
    Paramters
    ---------
        ast : AST
        
    Returns
    -------
        occurences : list
            List of node IDs of the occurences of var
    
    """
    nodes = graph.nodes()
    
    def filter_nodes(node):
        return NodeUtils.get_node_type(graph, node) == NodeType.IDENTIFIER and (NodeUtils.get_identifier_name(graph, node).strip() == var)
    
    return list(filter(filter_nodes, nodes))