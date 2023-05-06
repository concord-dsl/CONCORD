from pathlib import Path
import unittest

import networkx as nx
from utils.graph import load_json

from utils.statements import filter_statements, get_catch_block_statements, get_for_statements, get_if_statements, get_print_statements, get_return_statements, get_simple_assignment_statements, get_while_statements


JSON_FILES = Path(__file__).parent.resolve().parent.joinpath('json_files')

class GetPrintStatementsTestCase(unittest.TestCase):
    
    def test_method_get_print_statements(self):
        ground_truth = {
            "1000108": {"1000109", "1000110", "1000108"},
            "1000121": {"1000122", "1000123", "1000121"},
            "1000127": {"1000128", "1000129", "1000127"}
        }
        ast = load_json(f'{JSON_FILES}/test_method_prnts_ast.json')
        print_statements = get_print_statements(ast)
        
        self.assertDictEqual(ground_truth, print_statements, "The set of print statements is incorrect.")
    
class GetCatchBlockStatements(unittest.TestCase):
    def test_method_get_catch_block_statements(self):
        self.maxDiff = None
        ground_truth = {
            "1000118": {"1000118", "1000119", "1000127", "1000135", "1000120", 
                        "1000121", "1000122", "1000123", "1000128", "1000132", 
                        "1000124", "1000125", "1000126", "1000129", "1000130",
                        "1000136", "1000140", "1000137", "1000138", "1000139",
                        "1000133", "1000134", "1000140", "1000141", "1000142",
                        "1000131"},
            "1000167": {"1000167", "1000168", "1000169", "1000170", "1000171"}
        }
        ast = load_json(f'{JSON_FILES}/test_method_catch_blocks_ast.json')
        catch_blocks = get_catch_block_statements(ast)
        
        self.assertDictEqual(ground_truth, catch_blocks, "The set of catch blocks is incorrect.")
        
class GetSimpleAssignments(unittest.TestCase):
    def test_method_get_simple_assingments(self):
        self.maxDiff = None
        ground_truth = {
            "1000106": {"1000106", "1000107", "1000108"},
            "1000136": {"1000136", "1000137", "1000138"},
            "1000152": {"1000152", "1000153", "1000154"},
            "1000121": {"1000121", "1000122", "1000123"}
        }
        ast = load_json(f'{JSON_FILES}/remove_simple_assignment/test_method_simple_assignment_ast.json')
        simple_assignments = get_simple_assignment_statements(ast)
        
        self.assertDictEqual(ground_truth, simple_assignments, "The set of simple assignments is incorrect.")
   
class GetIfStatements(unittest.TestCase):
    def test_method_get_if_statements(self):
        self.maxDiff = None
        ground_truth = {
            "1000111": {'1000115', '1000125', '1000134', '1000117', 
                        '1000112', '1000124', '1000122', '1000135', 
                        '1000116', '1000126', '1000130', '1000132', 
                        '1000131', '1000129', '1000123', '1000121', 
                        '1000118', '1000133', '1000120', '1000119', 
                        '1000127', '1000111', '1000128', '1000113', 
                        '1000114'},
            "1000128": {'1000130', '1000134', '1000132', '1000133', 
                        '1000128', '1000131', '1000135', '1000129'},
            "1000136": {'1000136', '1000148', '1000160', '1000155', 
                        '1000153', '1000151', '1000144', '1000147', 
                        '1000138', '1000152', '1000157', '1000149', 
                        '1000146', '1000139', '1000143', '1000150', 
                        '1000142', '1000140', '1000159', '1000145', 
                        '1000158', '1000141', '1000156', '1000137', 
                        '1000154'},
            "1000153": {'1000159', '1000157', '1000160', '1000155', 
                        '1000153', '1000158', '1000156', '1000154'}
        }
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method_if_stmnts_ast.json')
        if_stats = get_if_statements(ast)
        
        self.assertDictEqual(ground_truth, if_stats, "The set of if statements is incorrect.")
 
class GetForStatements(unittest.TestCase):
    def test_get_for_statements(self):
        self.maxDiff = None
        ground_truth = {
            "1000112": {'1000115', '1000125', '1000117', '1000112', 
                        '1000124', '1000122', '1000116', '1000126', 
                        '1000130', '1000132', '1000131', '1000129', 
                        '1000123', '1000121', '1000118', '1000133', 
                        '1000120', '1000119', '1000127', '1000128', 
                        '1000113', '1000114'},
            "1000138": {'1000148', '1000160', '1000155', '1000153', 
                        '1000151', '1000166', '1000144', '1000147', 
                        '1000162', '1000138', '1000152', '1000157', 
                        '1000149', '1000169', '1000146', '1000165', 
                        '1000139', '1000143', '1000163', '1000150', 
                        '1000161', '1000142', '1000167', '1000140', 
                        '1000159', '1000145', '1000170', '1000158', 
                        '1000141', '1000156', '1000164', '1000168', 
                        '1000154'},
            "1000153": {'1000167', '1000159', '1000157', '1000160', 
                        '1000155', '1000153', '1000165', '1000170', 
                        '1000163', '1000166', '1000158', '1000164', 
                        '1000161', '1000156', '1000162', '1000169', 
                        '1000168', '1000154'}
        }
        ast = load_json(f'{JSON_FILES}/get_for_statements/test_method_for_stmnts_ast.json')
        if_stats = get_for_statements(ast)
        
        self.assertDictEqual(ground_truth, if_stats, "The set of for statements is incorrect.")
   
class GetWhileStatements(unittest.TestCase):
    def test_method_get_while_statements(self):
        self.maxDiff = None
        ground_truth = {
            "1000120": {'1000120', '1000133', '1000124', '1000131', 
                        '1000127', '1000129', '1000125', '1000130', 
                        '1000132', '1000122', '1000126', '1000128', 
                        '1000121', '1000123'},
            "1000139": {'1000141', '1000147', '1000143', '1000140', 
                        '1000148', '1000144', '1000139', '1000142', 
                        '1000146', '1000145'},
        }
        ast = load_json(f'{JSON_FILES}/get_while_statements/test_method_while_stmnts_ast.json')
        while_stats = get_while_statements(ast)
        
        self.assertDictEqual(ground_truth, while_stats, "The set of while statements is incorrect.")
 
class FilterStatementsTestCase(unittest.TestCase):
    def test_method_filter_catch_if_statements(self):
        # This translates to: Exclude -> {catch_block, if_block} and Include -> {while_block}
        # when performing reduction strategies.
        filters = {
            'catch_block': True,
            'if_block': True,
            'while_block': False
        } 
        ast = load_json(f'{JSON_FILES}/test_method_filtering_ast.json')
        # Tags all catch and if blocks nodes.
        filtered_statements = filter_statements(ast, filters)
        nodes = filtered_statements.nodes(data=True)
        # Ground truth that represents the set of catch and if blocks.
        ground_truth = {'1000160', '1000127', '1000143', '1000125', 
                        '1000153', '1000155', '1000146', '1000148', 
                        '1000147', '1000149', '1000128', '1000151', 
                        '1000159', '1000142', '1000158', '1000126', 
                        '1000161', '1000150', '1000157', '1000130', 
                        '1000129', '1000145', '1000156', '1000154', 
                        '1000152', '1000144'}
        
        # Iterate over nodes labeled 'protected'
        protected_nodes = {n for n, data in nodes if ('protected' in data)}
        
        # Check if the labeled nodes match with the ground truth
        self.assertSetEqual(ground_truth, protected_nodes, "The set of filtered statements is incorrect.")

    def test_method_filter_catch_if_while_statements(self):
        filters = {
            'catch_block': True,
            'if_block': True,
            'while_block': True
        } 
        ast = load_json(f'{JSON_FILES}/test_method_filtering_ast.json')
        filtered_statements = filter_statements(ast, filters)
        nodes = filtered_statements.nodes(data=True)
        ground_truth = {'1000160', '1000165', '1000127', '1000143', 
                        '1000125', '1000162', '1000153', '1000155', 
                        '1000146', '1000148', '1000147', '1000149', 
                        '1000128', '1000171', '1000151', '1000163', 
                        '1000159', '1000142', '1000170', '1000158', 
                        '1000126', '1000166', '1000169', '1000161', 
                        '1000168', '1000150', '1000157', '1000167', 
                        '1000130', '1000129', '1000145', '1000156', 
                        '1000154', '1000152', '1000144', '1000164'}
        
        protected_nodes = {n for n, data in nodes if ('protected' in data)}
        self.assertSetEqual(ground_truth, protected_nodes, "The set of filtered statements is incorrect.")
        
    def test_method_filter_no_statement(self):
        filters = {
            'catch_block': False,
            'if_block': False,
            'while_block': False
        } 
        ast = load_json(f'{JSON_FILES}/test_method_filtering_ast.json')
        filtered_statements = filter_statements(ast, filters)
        nodes = filtered_statements.nodes(data=True)
        
        ground_truth = set()
        protected_nodes = {n for n, data in nodes if ('protected' in data)}
        
        # There should be no protected node.
        self.assertSetEqual(ground_truth, protected_nodes, "The set of filtered statements is incorrect.")

class GetReturnStatements(unittest.TestCase):
    def test_method_get_return_statements(self):
        self.maxDiff = None
        ground_truth = set()
        ast = load_json(f'{JSON_FILES}/test_method_catch_blocks_ast.json')
        return_statements = get_return_statements(ast)
        
        self.assertSetEqual(ground_truth, return_statements, "The set of return statements is incorrect.")
    
    def test_method2_get_return_statements(self):
        self.maxDiff = None
        ground_truth = set(["1000199", "1000216"])
        ast = load_json(f'{JSON_FILES}/test_method_multiple_returns.json')
        return_statements = get_return_statements(ast)
        
        self.assertSetEqual(ground_truth, return_statements, "The set of return statements is incorrect.")
        
    def test_method3_get_return_statements(self):
        self.maxDiff = None
        ground_truth = set(["1000121"])
        ast = load_json(f'{JSON_FILES}/test_method2_ast.json')
        return_statements = get_return_statements(ast)
        
        self.assertSetEqual(ground_truth, return_statements, "The set of return statements is incorrect.")
 
if __name__ == '__main__':
    unittest.main()