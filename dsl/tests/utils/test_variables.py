import unittest
from pathlib import Path

import networkx as nx
from utils.graph import load_json

from utils.variables import get_variable_occurences

JSON_FILES = Path(__file__).parent.resolve().parent.joinpath('json_files')

class GetVariableOccurencesTestCase(unittest.TestCase):
    def test_method_get_variable_occurences(self):
        ground_truth = {"1000107", "1000113"}
        ast = load_json(f'{JSON_FILES}/test_method_ast.json')
        var = "k"
        
        var_occurences = set(get_variable_occurences(ast, var))
        
        self.assertSetEqual(ground_truth, var_occurences, f'The set of the variable occurences of {var} is incorrect.')

    def test_method2_get_variable_occurences(self):
        ground_truth = {"1000120", "1000122", "1000108"}
        ast = load_json(f'{JSON_FILES}/test_method2_ast.json')
        var = "result"
        
        var_occurences = set(get_variable_occurences(ast, var))
        
        self.assertSetEqual(ground_truth, var_occurences, f'The set of the variable occurences of {var} is incorrect.')
        
    def test_method3_get_variable_occurences(self):
        ground_truth = {"1000107", "1000113", "1000116", "1000125", 
                        "1000129", "1000131", "1000134", "1000137", 
                        "1000139", "1000142", "1000148", "1000152"}
        ast = load_json(f'{JSON_FILES}/test_method3_ast.json')
        var = "p"
        
        var_occurences = set(get_variable_occurences(ast, var))
        
        self.assertSetEqual(ground_truth, var_occurences, f'The set of the variable occurences of {var} is incorrect.')
    
if __name__ == '__main__':
    unittest.main()