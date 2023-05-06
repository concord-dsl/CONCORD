from copy import deepcopy
import unittest
from pathlib import Path

import networkx as nx
from tasks.EdgeOperations.AddOperations import AddOperations
from utils.graph import load_json

DOT_FILES = Path(__file__).parent.resolve().parent.joinpath('dot_files')
JSON_FILES = Path(__file__).parent.resolve().parent.joinpath('json_files')

class AddNCSEdges(unittest.TestCase):
    
    def test_add_ncs_edge(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_ncs_cpg14_ground_truth.json')
        method_cpg = load_json(f'{JSON_FILES}/test_method_ncs_cpg14.json')
        method_with_ncs_edges = AddOperations.next_token(method_cpg)
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
        
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        match_result = nx.is_isomorphic(method_with_ncs_edges, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "NCS Augmented graph does not match ground truth")
        
class AddNextSiblingEdges(unittest.TestCase):
    
    def test_add_next_sib_edge(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_next_sib_ground_truth.json')
        method_ast = load_json(f'{JSON_FILES}/test_method_ast.json')
        method_with_next_sib_edges = AddOperations.next_sibling(method_ast)
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
        
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        match_result = nx.is_isomorphic(method_with_next_sib_edges, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "NEXT_SIB Augmented graph does not match ground truth")
        
class AddComputedFromEdges(unittest.TestCase):
    
    def test_add_computed_from_edge(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_cmptd_frm_ast_ground_truth.json')
        method_ast = load_json(f'{JSON_FILES}/test_method_cmptd_frm_ast.json')
        method_with_computed_from_edges = AddOperations.computed_from(method_ast)
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
        
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        match_result = nx.is_isomorphic(method_with_computed_from_edges, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "COMPUTED_FROM Augmented graph does not match ground truth")
    
class AddLastLexicalUseEdge(unittest.TestCase):

    def test_add_last_lexical_use_edge(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method3_last_lex_use_ast_ground_truth.json')
        method_ast = load_json(f'{JSON_FILES}/test_method3_ast.json')
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        method_with_last_lexical_use_edges = AddOperations.last_lexical_use(method_ast)
            
        match_result = nx.is_isomorphic(method_with_last_lexical_use_edges, ground_truth, node_match=node_match, edge_match=edge_match)
            
        self.assertTrue(match_result, "LAST_LEXICAL_USE Augmented graph does not match ground truth")
    
class AddWhileControlFlowEdges(unittest.TestCase):
    def test_method1_add_while_cfg_edges(self):
        method_ast = load_json(f'{JSON_FILES}/test_method_filtering_ast.json')
        ground_truth = deepcopy(method_ast)
        # Building the ground truth manually to avoid creating another DOT file.
        ground_truth.add_edge("1000163", "1000166", label="WHILE_EXEC")
        ground_truth.add_edge("1000166", "1000163", label="WHILE_NEXT")
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        method_with_while_cfg_edges = AddOperations.while_exec(method_ast)
            
        match_result = nx.is_isomorphic(method_with_while_cfg_edges, ground_truth, node_match=node_match, edge_match=edge_match)
            
        self.assertTrue(match_result, "WHILE_CFG Augmented graph does not match ground truth")

    def test_method2_add_while_cfg_edges(self):
        method_ast = load_json(f'{JSON_FILES}/get_while_statements/test_method_while_stmnts_ast.json')
        ground_truth = deepcopy(method_ast)
        # Building the ground truth manually to avoid creating another JSON file.
        ground_truth.add_edge("1000121", "1000125", label="WHILE_EXEC")
        ground_truth.add_edge("1000125", "1000121", label="WHILE_NEXT")
        
        ground_truth.add_edge("1000140", "1000145", label="WHILE_EXEC")
        ground_truth.add_edge("1000145", "1000140", label="WHILE_NEXT")
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        method_with_while_cfg_edges = AddOperations.while_exec(method_ast)
            
        match_result = nx.is_isomorphic(method_with_while_cfg_edges, ground_truth, node_match=node_match, edge_match=edge_match)
            
        self.assertTrue(match_result, "WHILE_CFG Augmented graph does not match ground truth")
    
    def test_method3_add_while_cfg_edges(self):
        method_ast = load_json(f'{JSON_FILES}/test_method3_ast.json')
        ground_truth = deepcopy(method_ast)
        # Building the ground truth manually to avoid creating another JSON file.
        ground_truth.add_edge("1000124", "1000127", label="WHILE_EXEC")
        ground_truth.add_edge("1000127", "1000124", label="WHILE_NEXT")

        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        method_with_while_cfg_edges = AddOperations.while_exec(method_ast)
            
        match_result = nx.is_isomorphic(method_with_while_cfg_edges, ground_truth, node_match=node_match, edge_match=edge_match)
            
        self.assertTrue(match_result, "WHILE_CFG Augmented graph does not match ground truth")

class AddForControlFlowEdges(unittest.TestCase):
    
    def test_method1_add_for_cfg_edges(self):
        method_ast = load_json(f'{JSON_FILES}/get_for_statements/test_method_for_stmnts_ast.json')
        ground_truth = deepcopy(method_ast)
        
        # Add the edges
        # 1st For loop
        ground_truth.add_edge("1000113","1000118", label='FOR_EXEC')
        ground_truth.add_edge("1000116","1000118", label='FOR_EXEC')
  
        ground_truth.add_edge("1000118", "1000113", label='FOR_NEXT')
        ground_truth.add_edge("1000118", "1000116", label='FOR_NEXT')

        
        # 2nd For loop
        ground_truth.add_edge("1000139","1000148", label='FOR_EXEC')
        ground_truth.add_edge("1000140","1000148", label='FOR_EXEC')
        ground_truth.add_edge("1000143","1000148", label='FOR_EXEC')
        ground_truth.add_edge("1000146","1000148", label='FOR_EXEC')
  
        ground_truth.add_edge("1000148","1000139", label='FOR_EXEC')
        ground_truth.add_edge("1000148","1000140", label='FOR_EXEC')
        ground_truth.add_edge("1000148","1000143", label='FOR_EXEC')
        ground_truth.add_edge("1000148","1000146", label='FOR_EXEC')
        
        # 3rd For loop
        ground_truth.add_edge("1000154","1000166", label='FOR_EXEC')
        ground_truth.add_edge("1000155","1000166", label='FOR_EXEC')
        ground_truth.add_edge("1000158","1000166", label='FOR_EXEC')
        ground_truth.add_edge("1000161","1000166", label='FOR_EXEC')
  
        ground_truth.add_edge("1000166","1000154", label='FOR_EXEC')
        ground_truth.add_edge("1000166","1000155", label='FOR_EXEC')
        ground_truth.add_edge("1000166","1000158", label='FOR_EXEC')
        ground_truth.add_edge("1000166","1000161", label='FOR_EXEC')
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        method_with_for_cfg_edges = AddOperations.for_exec(method_ast)
            
        match_result = nx.is_isomorphic(method_with_for_cfg_edges, ground_truth, node_match=node_match, edge_match=edge_match)
            
        self.assertTrue(match_result, "FOR_CFG Augmented graph does not match ground truth")
       
class AddGuardedByEdges(unittest.TestCase):
    
    def test_method_for_guraded_by_edges(self):
        method_ast = load_json(f'{JSON_FILES}/guraded_by/test_method_guraded_by.json')
        ground_truth = deepcopy(method_ast)
        
        # Add edges
        # First if stmnt
        # a
        ground_truth.add_edge("1000126", "1000118", label="GUARDED_BY")
        # p
        ground_truth.add_edge("1000129", "1000121", label="GUARDED_BY")
        # r
        ground_truth.add_edge("1000130", "1000122", label="GUARDED_BY")
        
        # Second if stmnt
        # p
        ground_truth.add_edge("1000138", "1000134", label="GUARDED_BY")
        # r
        ground_truth.add_edge("1000141", "1000135", label="GUARDED_BY")
        
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        method_with_gb_gbn_edges = AddOperations.guarded_by(method_ast)
        
        match_result = nx.is_isomorphic(method_with_gb_gbn_edges, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "GURADED_BY Augmented graph does not match ground truth")
    
    def test_method2_for_guraded_by_edges(self):
        method_ast = load_json(f'{JSON_FILES}/guraded_by/test_method2_guraded_by.json')
        ground_truth = deepcopy(method_ast)
        
        # Add edges
        
        # First if else
        ground_truth.add_edge("1000164", "1000158", label="GUARDED_BY")
        ground_truth.add_edge("1000168", "1000160", label="GUARDED_BY")
        ground_truth.add_edge("1000176", "1000160", label="GUARDED_BY_NEGATION")
        
        # Second if else
        ground_truth.add_edge("1000190", "1000184", label="GUARDED_BY") # chars
        ground_truth.add_edge("1000197", "1000186", label="GUARDED_BY") # replace
        ground_truth.add_edge("1000205", "1000186", label="GUARDED_BY_NEGATION")
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        method_with_gb_gbn_edges = AddOperations.guarded_by(method_ast)
        
        match_result = nx.is_isomorphic(method_with_gb_gbn_edges, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "GURADED_BY Augmented graph does not match ground truth")
    
    def test_method3_for_guraded_by_edges(self):
        method_ast = load_json(f'{JSON_FILES}/guraded_by/test_method3_guraded_by.json')
        ground_truth = deepcopy(method_ast)
        
        # Add edges
        targetStr_node = "1000245"
        targets_node = "1000247"
        ptr_node = "1000250"
        
        ground_truth.add_edge("1000255", targets_node, label="GURADED_BY")
        ground_truth.add_edge("1000259", targetStr_node, label="GURADED_BY")
        ground_truth.add_edge("1000262", ptr_node, label="GURADED_BY")
        
  
        ground_truth.add_edge("1000275", targets_node, label="GURADED_BY_NEGATION")
        ground_truth.add_edge("1000271", ptr_node, label="GURADED_BY_NEGATION")
        ground_truth.add_edge("1000267", ptr_node, label="GURADED_BY_NEGATION")
        
        ground_truth.add_edge("1000271", "1000267", label="") # ptr in if statement
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
    
        method_with_gb_gbn_edges = AddOperations.guarded_by(method_ast)
        
        match_result = nx.is_isomorphic(method_with_gb_gbn_edges, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "GURADED_BY Augmented graph does not match ground truth")
     
class AddReturnsToEdges(unittest.TestCase):
    def test_method_add_returns_to_edges(self):
        self.maxDiff = None
        ground_truth = set()
        ast = load_json(f'{JSON_FILES}/test_method_catch_blocks_ast.json')
        ground_truth = deepcopy(ast)
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        method_with_rt_edges = AddOperations.returns_to(ast)
        # Add Edges
        # No edges will be added (no return statements)
        match_result = nx.is_isomorphic(method_with_rt_edges, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "RETURNS_TO Augmented graph does not match ground truth")
    
    def test_method2_add_returns_to_edges(self):
        self.maxDiff = None
        ground_truth = set(["1000199", "1000216"])
        ast = load_json(f'{JSON_FILES}/test_method_multiple_returns.json')
        ground_truth = deepcopy(ast)
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        method_with_rt_edges = AddOperations.returns_to(ast)
        
        # Add Edges
        ground_truth.add_edge("1000199", "1000225", label="RETURNS_TO")
        ground_truth.add_edge("1000199", "1000143", label="RETURNS_TO")
        
        ground_truth.add_edge("1000216", "1000225", label="RETURNS_TO")
        ground_truth.add_edge("1000216", "1000143", label="RETURNS_TO")
        
        match_result = nx.is_isomorphic(method_with_rt_edges, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "RETURNS_TO Augmented graph does not match ground truth")
        
    def test_method3_add_returns_to_edges(self):
        self.maxDiff = None
        ground_truth = set(["1000121"])
        ast = load_json(f'{JSON_FILES}/test_method2_ast.json')
        ground_truth = deepcopy(ast)
        
        node_labels = [data.get('label') for (_, data) in ground_truth.nodes(data=True)]
        edge_labels = [data.get('label') for (u, v, data) in ground_truth.edges(data=True)]
            
        node_match = nx.algorithms.isomorphism.categorical_node_match("label", node_labels)
        edge_match = nx.algorithms.isomorphism.categorical_edge_match("label", edge_labels)
        
        method_with_rt_edges = AddOperations.returns_to(ast)
        
        # Add Edges
        ground_truth.add_edge("1000121", "1000101", label="RETURNS_TO")
        ground_truth.add_edge("1000121", "1000123", label="RETURNS_TO")
        
        match_result = nx.is_isomorphic(method_with_rt_edges, ground_truth, node_match=node_match, edge_match=edge_match)
        
        self.assertTrue(match_result, "RETURNS_TO Augmented graph does not match ground truth")
        
if __name__ == '__main__':
    unittest.main()