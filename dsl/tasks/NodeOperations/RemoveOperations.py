import networkx as nx

import inspect
import logging
from itertools import chain

from utils.statements import get_print_statements, get_simple_assignment_statements
from utils.graph import get_ast, get_local_variables

class RemoveOperations:
    
    @staticmethod
    def print_statements(graph: nx.MultiDiGraph):
        if not graph:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Null graph, skipping')
            return graph
        ast = get_ast(graph)
        if not ast:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph
        
        # Get print statements
        print_stmtns = get_print_statements(ast)
        if not print_stmtns:
            logging.warn(f'{inspect.currentframe().f_code.co_name} No print statements were found, skipping')
            return graph
        
        # Since print statements are returned as dicts, we have to get dict.values() + faltten since for each e in 
        # dict.values(), e is a set.
        print_stmtns = list(chain(*list(print_stmtns.values())))
                
        # Filter the print statements to be removed.
        filtered_print_stmtns = [s for s in print_stmtns if not 'protected' in graph.nodes[s]]
        graph.remove_nodes_from(filtered_print_stmtns)
        
        return graph
    
    @staticmethod
    def logging_statements():
        pass
    
    @staticmethod
    def sys_exit_statements():
        pass
    
    @staticmethod
    def simple_assignments(graph: nx.MultiDiGraph):
        if not graph:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Null graph, skipping')
            return graph
        ast = get_ast(graph)
        if not ast:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph
        
        # Get simple assignments nodes
        simple_assignments = get_simple_assignment_statements(ast)
        # Flatten
        simple_assignments = list(chain(*list(simple_assignments.values())))
        # Filter statements
        filtered_simple_assignments = [s for s in simple_assignments if not 'protected' in graph.nodes[s]]
        
        graph.remove_nodes_from(filtered_simple_assignments)
        
        return graph