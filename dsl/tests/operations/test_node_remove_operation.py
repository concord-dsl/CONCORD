from copy import deepcopy
import unittest
from pathlib import Path

import networkx as nx

from tasks.NodeOperations.RemoveOperations import RemoveOperations
from utils.graph import load_json

JSON_FILES = Path(__file__).parent.resolve().parent.joinpath('json_files')

class RemovePrintStatements(unittest.TestCase):
    def test_method_remove_print_statements(self):
        graph = load_json(f'{JSON_FILES}/test_method_prnts_ast.json')
        ground_truth = deepcopy(graph)
        ground_truth.remove_nodes_from(["1000108", "1000109", "1000110", "1000121", "1000122", "1000123", "1000127", "1000128", "1000129"])
        
        result_graph = RemoveOperations.print_statements(graph)
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
        
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
 
        match_result = nx.is_isomorphic(result_graph, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "Simplified graph by print statement removal does not match ground truth")
        
class RemoveSimpleAssignments(unittest.TestCase):
    def test_method_remove_simple_assignments(self):
        graph = load_json(f'{JSON_FILES}/remove_simple_assignment/test_method_simple_assignment_ast.json')
        ground_truth = deepcopy(graph)
        ground_truth.remove_nodes_from(["1000106", "1000107", "1000108", 
                                        "1000136", "1000137", "1000138", 
                                        "1000152", "1000153", "1000154",
                                        "1000121", "1000122", "1000123"])
        
        result_graph = RemoveOperations.simple_assignments(graph)
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
        
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
 
        match_result = nx.is_isomorphic(result_graph, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "Simplified graph by simple assignment statement removal does not match ground truth")
        
        
if __name__ == '__main__':
    unittest.main()