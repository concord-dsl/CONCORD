from itertools import chain
import os
import networkx as nx
from utils.io import file_exists, read_file, read_json, write_file
from utils.last_write_read.NodeType import NodeType

from utils.last_write_read.NodeUtils import NodeUtils


def get_print_statements(graph: nx.MultiDiGraph):
        """Returns AST nodes of print statements
        
        Parameter
        ---------
        ast: AST
            An Abstract Syntax Tree.
            
        Returns
        -------
            print_nodes : dict
                Dict of root nodes of AST subgraphs of the print statements.
                Example: 
                {
                    '1223457' : {1223457, 1223478, 1223425},
                    ...
                }
        """
        print_subgraphs = {}
        for node, data in graph.nodes(data=True):
            label = data['label']
            aux_id = label.split(',')
            if 'print' in aux_id[0]:
                print_subgraphs[node] = set(list(nx.algorithms.traversal.depth_first_search.dfs_tree(graph, node).nodes()))

        return print_subgraphs
    
def get_catch_block_statements(graph: nx.MultiDiGraph):
        """Returns a dictionary of catch blocks and their internal statements.
        
        Parameters
        ----------
        ast : MultiDiGraph or DiGraph.
            An Abstract Syntax Tree.
        
        Returns
        -------
        cb_statements : dict
            A mapping of each catch block node and the statements within that block.
        
        None 
            If there are no catch blocks.
        
        """
        def filter_catch_nodes(node):
            n_id, data = node
            return 'BLOCK,catch,catch' in data['label']
        
        nodes = graph.nodes(data=True)
        catch_nodes = list(filter(filter_catch_nodes, nodes))
        # What if there are no try/catch blocks?
        if not catch_nodes:
            return None
        # Create a dictionary
        cb_statements = {n[0]: set(nx.algorithms.traversal.depth_first_search.dfs_tree(graph, n[0]).nodes()) for n in catch_nodes}
        
        return cb_statements
    
def get_simple_assignment_statements(graph: nx.MultiDiGraph):
    
    nodes = graph.nodes(data=True)
    
    # Filter to get simple assigment nodes
    def filter_simple_assignment(node):
        n_id, data = node
        _label = data['label']
        _type = _label.split(',')[0][1:]
        # Don't bother if it's not an assignment node
        if NodeUtils.get_node_type(graph, n_id) != NodeType.OP_ASSIGNMENT:
            return False
        # If it is, then make sure that it has one level (more than level = not a simple assignment) and the rhs of v = exp is a literal, i.e exp == literal.
        assignment_tree_nodes = nx.algorithms.traversal.depth_first_search.dfs_tree(graph, n_id).nodes()
        if len(assignment_tree_nodes) != 3: # 3 because bfs_tree returns a tree, so root+children
            return False
        # There should exactly be one count of IDENTIFIER and LITERAL nodes
        id_nodes = 0
        literal_nodes = 0
        for an_node in assignment_tree_nodes:
            if NodeUtils.get_node_type(graph, an_node) == NodeType.IDENTIFIER:
                id_nodes += 1
            if NodeUtils.get_node_type(graph, an_node) == NodeType.LITERAL:
                literal_nodes += 1
                
        return id_nodes == 1 and literal_nodes == 1
    
    simple_assignment_nodes = list(filter(filter_simple_assignment, nodes))
    # Create a dictionary
    sa_statements = {n[0]: set(nx.algorithms.traversal.depth_first_search.dfs_tree(graph, n[0]).nodes()) for n in simple_assignment_nodes}
        
    return sa_statements
        
def get_if_statements(graph: nx.MultiDiGraph):
    """Returns a dictionary of if statements and their internal statements (i.e when the if condition is statisfied).
    
    Parameters
    ----------
    ast : MultiDiGraph or DiGraph.
        An Abstract Syntax Tree.
    
    Returns
    -------
    if_nodes_dict : dict
        A mapping of each if block node and the statements within that block.
    
    None 
        If there are no catch blocks.
    
    """
    nodes = graph.nodes()
    def filter_ifs(node):
        return NodeUtils.get_node_type(graph, node) == NodeType.IF_STATEMENT
    
    if_nodes = list(filter(filter_ifs, nodes))
    if not if_nodes:
        return None
    
    if_nodes_dict = {n: set(nx.algorithms.traversal.depth_first_search.dfs_tree(graph, n).nodes()) for n in if_nodes}
    
    return if_nodes_dict
            
def get_for_statements(graph: nx.MultiDiGraph):
    """Returns a dictionary of for statements and their internal statements (i.e for-loop body).
    
    Parameters
    ----------
    ast : MultiDiGraph or DiGraph.
        An Abstract Syntax Tree.
    
    Returns
    -------
    for_nodes_dict : dict
        A mapping of each for block node and the statements within that block.
    
    None 
        If there are no for statements.
    
    """
    nodes = graph.nodes()
    def filter_fors(node):
        return NodeUtils.get_node_type(graph, node) == NodeType.FOR_STATEMENT
    
    for_nodes = list(filter(filter_fors, nodes))
    if not for_nodes:
        return None
    
    for_nodes_dict = {n: set(nx.algorithms.traversal.depth_first_search.dfs_tree(graph, n).nodes()) for n in for_nodes}
    
    return for_nodes_dict
            
def get_while_statements(graph: nx.MultiDiGraph):
    """Returns a dictionary of while statements and their internal statements (i.e while-loop body).
    
    Parameters
    ----------
    ast : MultiDiGraph or DiGraph.
        An Abstract Syntax Tree.
    
    Returns
    -------
    for_nodes_dict : dict
        A mapping of each while block node and the statements within that block.
    
    None 
        If there are no while statements.
    
    """
    nodes = graph.nodes()
    def filter_whiles(node):
        return NodeUtils.get_node_type(graph, node) == NodeType.WHILE_STATEMENT
    
    while_nodes = list(filter(filter_whiles, nodes))
    if not while_nodes:
        return None
    
    while_nodes_dict = {n: set(nx.algorithms.traversal.depth_first_search.dfs_tree(graph, n).nodes()) for n in while_nodes}
    
    return while_nodes_dict
                       
def filter_statements(graph: nx.MultiDiGraph, filters: dict):
    # filter_name -> get_<filtername>_statements
    # e.g: catch_block -> get_catch_block_statements
    FILTERS_MAPPER = {
        'catch_block': get_catch_block_statements,
        'for_block': get_for_statements,
        'while_block': get_while_statements,
        'if_block': get_if_statements 
    }
    filters = {k:FILTERS_MAPPER[k] for k,v in filters.items() if v}
    
    if not filters:
        return graph
        
    _statements = set()
    for f in filters:
        results = FILTERS_MAPPER[f](graph)
        if results:
            _statements.update(set(chain.from_iterable(list(results.values()))))
            
    # Tag the nodes that should not be removed
    for n in _statements:
        graph.nodes[n]['protected'] = True
    
    return graph

def get_return_statements(graph: nx.MultiDiGraph):
    
    nodes = graph.nodes()
    
    def filter_returns(node):
        return NodeUtils.get_node_type(graph, node) == NodeType.RETURN_STATEMENT

    
    return set(filter(filter_returns , nodes))

def delete_statements(output_path):
    # See available files that contain removable statments
    file_names = ["print_stmnts.json", "simple_assignment_stmnts.json"]
    full_path_file_names = list(map(lambda x: os.path.join(output_path, x), file_names))
    # Keep only those that exist
    full_path_file_names = list(filter(lambda x: file_exists(x), full_path_file_names))
    # Control Structure file
    cs_file = os.path.join(output_path, "control_structures.json")
    # Merge all deletable statements
    deletable_statements = {}
    if len(full_path_file_names) == 1:
         # There is only one of statements (e.g. print) to be deleted
         deletable_statements = read_json(full_path_file_names[0])
    else:
        # Merge them all
        deletable_statements = read_json(full_path_file_names[0])
        full_path_file_names = full_path_file_names[1:]
        for dsfile in full_path_file_names:
            _dsfile = read_json(dsfile)
            for f in deletable_statements:
                deletable_statements[f] = deletable_statements[f] + _dsfile[f]

    # Remove statements that should not be removed since they exist
    # inside control structure blocks.
    if file_exists(cs_file):
        control_structures = read_json(cs_file)
        for f in deletable_statements:
            guarded_statments = control_structures[f]
            old_deletable_statements = deletable_statements[f]
            deletable_statements[f] = [line for line in old_deletable_statements if line[0] not in guarded_statments]
    _delete_statements(deletable_statements)


def _delete_statements(statments_dict):
    """
    statments_dict: dict(file_name -> list(list(int, string)))
    """
    # WARNING: This will override the original file
    for file in statments_dict:
        statements = statments_dict[file]
        file_content = read_file(file)
        line_numbers_to_modify = {line_nbr:string for line_nbr, string in statements}

        for line_nbr, string in line_numbers_to_modify.items():
            file_content[line_nbr - 1] = file_content[line_nbr - 1].replace(string, '')
 

        write_file(file, file_content)