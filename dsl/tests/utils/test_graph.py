from calendar import c
import unittest
from pathlib import Path

import networkx as nx

from utils.graph import get_ast, get_local_variables, get_method_parameters, get_parent_nodes_mapping, get_variable_assignments, load_json

JSON_FILES = Path(__file__).parent.resolve().parent.joinpath('json_files')

class GetASTTestCase(unittest.TestCase):
    
    def setUp(self):
        self.ast = load_json(f'{JSON_FILES}/test_method_ast.json')
        self.ast_nodes_labels = [data.get('label') for (_, data) in self.ast.nodes(data=True)]
        self.node_match = nx.algorithms.isomorphism.categorical_node_match("label", self.ast_nodes_labels)
    
    def test_extract_ast_from_cfg_ast(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_ast_cfg.json')
        extracted_ast = get_ast(ground_truth)
        match_result = nx.is_isomorphic(extracted_ast, self.ast, node_match=self.node_match)
        
        self.assertTrue(match_result, "Extracted AST does not match baseline AST")
        
    
    def test_extract_ast_from_cfg_ast_pdg(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_ast_cfg_pdg.json')
        extracted_ast = get_ast(ground_truth)
        match_result = nx.is_isomorphic(extracted_ast, self.ast, node_match=self.node_match)
        
        self.assertTrue(match_result, "Extracted AST does not match baseline AST")

    def test_extract_ast_from_cfg_ddg(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_cfg_ddg.json')
        extracted_ast = get_ast(ground_truth)
        
        self.assertIsNone(extracted_ast, "No AST shall be returned")
        
    def test_extract_ast_from_cfg_cdg(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_cfg_cdg.json')
        extracted_ast = get_ast(ground_truth)
        
        self.assertIsNone(extracted_ast, "No AST shall be returned")
    
    def test_extract_ast_from_ast(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_ast.json')
        extracted_ast = get_ast(ground_truth)
        match_result = nx.is_isomorphic(extracted_ast, self.ast, node_match=self.node_match)
        
        self.assertTrue(match_result, "Extracted AST does not match baseline AST")
    
    def test_extract_ast_from_cfg(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_cfg.json')
        extracted_ast = get_ast(ground_truth)
        
        self.assertIsNone(extracted_ast, "No AST shall be returned")
    
    def test_extract_ast_from_pdg(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_pdg.json')
        extracted_ast = get_ast(ground_truth)
        
        self.assertIsNone(extracted_ast, "No AST shall be returned")
        
    def test_extract_ast_from_cdg(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_cdg.json')
        extracted_ast = get_ast(ground_truth)
        
        self.assertIsNone(extracted_ast, "No AST shall be returned")   

    def test_extract_ast_from_ddg(self):
        ground_truth = load_json(f'{JSON_FILES}/test_method_ddg.json')
        extracted_ast = get_ast(ground_truth)
        
        self.assertIsNone(extracted_ast, "No AST shall be returned")
    
class GetParentNodesMappingTestCase(unittest.TestCase):
    
    def test_method1_get_parent_nodes_mapping_ast(self):
        ground_truth = {
            '1000101': ['1000102', '1000103', '1000104', '1000122'],
            '1000104': ['1000105', '1000106', '1000111'],
            '1000106': ['1000107', '1000108'],
            '1000111': ['1000112', '1000115', '1000118'],
            '1000108': ['1000109', '1000110'],
            '1000112': ['1000113', '1000114'],
        }
        
        ast = load_json(f'{JSON_FILES}/test_method_ast.json')
        p_c_mapping = get_parent_nodes_mapping(ast)
                
        self.assertDictEqual(ground_truth, p_c_mapping, "Parent Nodes mapping is not correct")
        
    def test_method2_get_parent_nodes_mapping_ast(self):
        ground_truth = {
            '1000101': ['1000102', '1000103', '1000104', '1000105', '1000123'],
            '1000105': ['1000106', '1000107', '1000110', '1000121'],
            '1000107': ['1000108', '1000109'],
            '1000110': ['1000111', '1000112', '1000113'],
            '1000114': ['1000115', '1000118'],
            '1000115': ['1000116', '1000117']
        }
        
        ast = load_json(f'{JSON_FILES}/test_method2_ast.json')
        p_c_mapping = get_parent_nodes_mapping(ast)
                
        self.assertDictEqual(ground_truth, p_c_mapping, "Parent Nodes mapping is not correct")
        
class GetLocalVariablesTestCase(unittest.TestCase):
    
    def test_method1_get_local_variables(self):
        ground_truth = {"k"}
        ast = load_json(f'{JSON_FILES}/test_method_ast.json')
        
        local_vars = set(get_local_variables(ast))
        
        self.assertSetEqual(ground_truth, local_vars, "Incorrect set of local variables.")
    
    def test_method2_get_local_variables(self):
        ground_truth = {"result", "j"}
        ast = load_json(f'{JSON_FILES}/test_method2_ast.json')
        
        local_vars = set(get_local_variables(ast))
        
        self.assertSetEqual(ground_truth, local_vars, "Incorrect set of local variables.")
        
class GetLocalVariableAssignmentsTestCase(unittest.TestCase):
    
    def test_method2_get_local_vars_assignments(self):
        ground_truth = {"1000107", "1000119"}
        ast = load_json(f'{JSON_FILES}/test_method2_ast.json')
        var = "result"
        
        var_assigments = set(get_variable_assignments(ast, var))
                
        self.assertSetEqual(ground_truth, var_assigments, "Incorrect set of assignment nodes.")
    
    def test_method3_get_local_vars_assignments(self):
        ground_truth = {"1000106", "1000128", "1000130", "1000133", "1000136", "1000138", "1000141"}
        ast = load_json(f'{JSON_FILES}/test_method3_ast.json')
        var = "p"
        
        var_assigments = set(get_variable_assignments(ast, var))
                
        self.assertSetEqual(ground_truth, var_assigments, "Incorrect set of assignment nodes.")

class GetMethodParamters(unittest.TestCase):
    
    def test_method_get_method_parameters(self):
        ground_truth = {"this", "a"}
        ast =  load_json(f'{JSON_FILES}/test_method_ast.json')
        method_params = set(get_method_parameters(ast))
        self.assertSetEqual(ground_truth, method_params, "Incorrect set of method paramters.")

    def test_method2_get_method_parameters(self):
        ground_truth = {"this", "a", "b"}
        ast =  load_json(f'{JSON_FILES}/test_method2_ast.json')
        method_params = set(get_method_parameters(ast))
        
        self.assertSetEqual(ground_truth, method_params, "Incorrect set of method paramters.")
        
    def test_method3_get_method_parameters(self):
        ground_truth = {"this", "a"}
        ast =  load_json(f'{JSON_FILES}/test_method3_ast.json')
        method_params = set(get_method_parameters(ast))
        
        self.assertSetEqual(ground_truth, method_params, "Incorrect set of method paramters.")


if __name__ == '__main__':
    unittest.main()