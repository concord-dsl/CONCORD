from copy import deepcopy
from pathlib import Path
from typing import Any
import json

import networkx as nx
from utils.last_write_read.NodeType import NodeType

from utils.last_write_read.NodeUtils import NodeUtils

def join(graphs: 'list[str]'):
    #TODO add docstring
    
    out_dir = Path(graphs[0]).parent.resolve()
    method_name = Path(graphs[0]).name.split('.')[0].split('_')[0]
    graphs: list[nx.MultiDiGraph] = [load(g) for g in graphs]
    merged_graph = nx.algorithms.operators.compose_all(graphs)
    
    merged_graph_path = f'{out_dir}/{method_name}.dot' 
    save(merged_graph, merged_graph_path)
    
    return merged_graph_path
    
def load(graph_file: str):
    graph = nx.drawing.nx_pydot.read_dot(graph_file)
    return clean_nodes(graph)

def save(graph: nx.MultiDiGraph, path: str):
    graph = clean_nodes(graph)
    nx.drawing.nx_pydot.write_dot(graph, path)
    
def load_json(graph_file: str):
    with open(graph_file) as jf:
        graph = nx.readwrite.json_graph.node_link_graph(json.load(jf))
    
    return graph

def save_json(graph: nx.MultiDiGraph, path: str):
    with open(path, 'w') as outfile:
        json.dump(nx.readwrite.json_graph.node_link_data(graph), outfile, indent=4)

              
def label_base_graphs(base_graphs: dict):
    # Only needed for ASTs and CFG since PDGs (DDGs and CDGs) are already labeled.
    base_graph_types = {'ast', 'cfg'}
    
    for m, g in base_graphs.items():
        for bg in g:
            graph_type = Path(bg).name.split('.')[0].split('_')[1]
            if graph_type in base_graph_types:
                loaded_g = load(bg)
                new_bg = nx.MultiDiGraph()
                # Add the nodes
                new_bg.add_nodes_from(loaded_g.nodes(data=True))
                for e in loaded_g.edges(data=True, keys=True):
                    u, v, k, d = e
                    new_bg.add_edge(u, v, key=k, label=graph_type.upper() )
                
                save(new_bg, bg)

def clean_nodes(graph: nx.MultiDiGraph):
    # For some reason, '\n' is added to the list of nodes, could be an issue when reading .dot files.
    # Doing this temp fix until I find a better solution.
    if "\\n" in graph:
        graph.remove_node("\\n")
        
    return graph

def add_key_base_graphs(base_graphs: dict):
    # Adding keys to each graph. This is important because we are dealing with networkx's MultiDiGraphs that will
    # later be merged together
    
    for m, g in base_graphs.items():
        pdg_types = {'cdg', 'ddg' ,'pdg'}
        
        for bg in g:
            graph_type = Path(bg).name.split('.')[0].split('_')[1]
            loaded_g = load(bg)
            new_bg = nx.MultiDiGraph()
            # Add the nodes
            new_bg.add_nodes_from(loaded_g.nodes(data=True))
            idx = 0
            for e in loaded_g.edges(data=True):
                u, v, d = e
                g_idx = f'{graph_type}{idx}'
                if graph_type in pdg_types:
                    new_bg.add_edge(u, v, key=g_idx, label=d['label'])
                else:
                    new_bg.add_edge(u, v, key=g_idx)
                idx += 1
            save(new_bg, bg)

def sort_nodes(graph: nx.MultiDiGraph):
    """Sorts nodes by their label.
    
    Parameters
    ----------
    graph : nx.MultiGraph
        A graph.
        
    Returns
    -------
    graph : nx.MultiGraph
        A graph with nodes sorted in increasing order.
    
    """
    sorted_graph = nx.MultiDiGraph()
    sorted_graph.add_nodes_from(sorted(graph.nodes(data=True)))
    sorted_graph.add_edges_from(graph.edges(data=True))
    
    return sorted_graph
    
def get_ast(graph: nx.MultiDiGraph):
        """Extracts the Abstract Syntex Tree from the Code Property Graph.
        
        Paramters
        ---------
        None
        
        Returns
        -------
        ast : CPG
            The Abstract Syntax Tree extracted from the CPG.
        
        """
        ast = nx.MultiDiGraph()
        ast.add_nodes_from(graph.nodes(data=True))
        ast_edges = []
        for e in graph.edges(keys=True, data=True):
            u, v, k, d = e
            if d and ('AST:' in d['label']):
                ast_edges.append(e)

        if not ast_edges:
            return None
        
        ast.add_edges_from(ast_edges)
        
  
        return ast
    
def get_token_nodes(graph: nx.MultiDiGraph):
        """Returns the sequence of tokens of the source code by collecting leaf nodes of the AST.
        
        Parameters
        ----------
        ast : AST
        
        Returns
        -------
        leaf_nodes : list
            List of the leaf nodes of the AST
        """
        out_degs = graph.out_degree()
        leaf_nodes = list(filter(lambda n: n[1] == 0, out_degs))
        
        return leaf_nodes
    
def get_parent_nodes_mapping(graph: nx.MultiDiGraph):
        """Returns a mapping between parent nodes and their children.
        
        Parameters
        ----------
        ast : AST
        
        Returns
        -------
        mapping : dict
            <parent> -> <children> mapping of parent and their children.
        """
        is_tree = nx.algorithms.is_tree
        if not is_tree(graph):
            return {}
        
        mapping = {}
        descendants_at_distance = nx.algorithms.traversal.breadth_first_search.descendants_at_distance
        nodes = graph.nodes()
        for n in nodes:
            children = list(descendants_at_distance(graph, n, 1))
            # Important to sort
            children.sort()
            if len(children) > 1:
                mapping[n] = children
        
        return mapping
    
def get_local_variables(graph: nx.MultiDiGraph, by_id: bool = False):
    """Returns the list of local variables within a method.
    
    Parameters
    ----------
    ast : AST
    by_id : boolean
        If set to true, it will return the IDs of local variable nodes. Default false (return variable names)
    
    Returns
    -------
    local_vars : list
        List of local variables.
    
    """
    def filter_local_nodes(node):
        n_id, data = node
        # Check if the node type is LOCAL (refers to a local variable, ref: https://cpg.joern.io/#node-ref-local)
        # Right now we are using the label to determine nodes' types. 
        # Local variable nodes' labels are formatted as the following:
        # (LOCAL, <type> <var-name>: <type>)
        # In the future, I will add another step (in the create() method of Representation) to preprocess the graph nodes to attach
        # some properties such as type, src_code etc.
        
        _type = data['label'].split(',')[0]
        return 'LOCAL' in _type
    
    def map_name(node):
        n_id, data = node
        _label_split = data['label'].split(',')
        var_name = _label_split[1].split(':')[0].split(' ')[1]
        
        return var_name
    
    def map_id(node):
        return node[0]
        
    
    nodes = graph.nodes(data=True)
    
    if by_id:  
        local_vars = list(map(map_id, filter(filter_local_nodes, nodes)))
    else:
        local_vars = list(map(map_name, filter(filter_local_nodes, nodes)))
    
    return local_vars

def get_variable_assignments(graph: nx.MultiDiGraph, var: str):
    """Returns all nodes where a variable var was assigned a value
    
    Parameters
    ----------
    ast : AST
    
    Returns
    -------
        assignment_nodes : list
            List of nodes where var was written to.
    
    """
    
    nodes = graph.nodes()
    # Filter function to get all nodes where variable var was assigned a value.
    def filter_var_assignments(node):
        assignements = {
            NodeType.OP_ASSIGNMENT, NodeType.OP_ASSIGN_PLUS, NodeType.OP_ASSIGN_MINUS, 
            NodeType.OP_ASSIGN_MUL, NodeType.OP_ASSIGN_DIV, NodeType.OPS_ASSIGN_AND, 
            NodeType.OPS_ASSIGN_OR, NodeType.OPS_ASSIGN_XOR, NodeType.OPS_ASSIGN_MOD, 
            NodeType.OPS_ASSIGN_SHIFT_LEFT, NodeType.OPS_ASSIGN_ARITH_SHIFT_RIGHT, NodeType.OPS_ASSIGN_LOGICAL_SHIFT_RIGHT,
            NodeType.OP_POST_DECREMENT, NodeType.OP_POST_INCREMENT, NodeType.OP_PRE_DECREMENT, NodeType.OP_PRE_INCREMENT
        }
        if NodeUtils.get_node_type(graph, node) in assignements:
            # Get its children
            children = list(graph.successors(node))
            # Check if the identifier child is var
            for c in children:
                if NodeUtils.get_node_type(graph, c) == NodeType.IDENTIFIER and (NodeUtils.get_identifier_name(graph, c).strip() == var):
                    return True
        
        return False
         
    return list(filter(filter_var_assignments, nodes))
    
def get_method_parameters(graph: nx.MultiDiGraph):
    nodes = graph.nodes()    
    
    def filter_nodes(node):
        return NodeUtils.get_node_type(graph, node) == NodeType.PARAMETER
    
    def map_name(node):
        return NodeUtils.get_identifier_name(graph, node)
        
    
    return list(map(map_name, filter(filter_nodes, nodes)))

def transform_nodes(graph: nx.MultiDiGraph) -> nx.MultiDiGraph:
    """Transforms the nodes of a graph. It addes 'node_type' and 'code' attribute to each node.
    
    Parameters
    ----------
    graph: MultiDiGraph
    
    Returns
    -------
        graph : MultiDiGraph
            The graph with transformation applied on each node.
    """
    
    nodes = graph.nodes()
    for n in nodes:
        graph.nodes[n]['node_type'] = str(NodeUtils.get_node_type(graph, n).name)
        code = NodeUtils.label_splitter(graph, n)
        graph.nodes[n]['code'] = code[-1]
        
    return graph
    
        
