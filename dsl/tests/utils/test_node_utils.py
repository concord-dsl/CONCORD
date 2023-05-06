import networkx as nx
import unittest
from pathlib import Path
from utils.graph import load_json

from utils.last_write_read.NodeUtils import NodeUtils

JSON_FILES = Path(__file__).parent.resolve().parent.joinpath('json_files')

class GetThenStatementTestCase(unittest.TestCase):
    
    def test_method1_get_then_statement(self):
        self.maxDiff = None
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method_if_stmnts_ast.json')
        # The ground truth is a mapping between each if node and its then statement node.
        # The then statement is rooted at a BLOCK node.
        # Sometimes there is no BLOCK node when the then statement is composed of one statement
        # e.g (C-like syntax):
        # if (condition) int p = foo(args); ==> covered in TC# 2
        
        ground_truth = {
            "1000111": "1000115",
            "1000128": "1000132",
            "1000136": "1000140",
            "1000153": "1000157"
        }
        if_nodes = ground_truth.keys()
        if_then_mapping = {}
        
        for n in if_nodes:
            if_then_mapping[n] = NodeUtils.get_if_then(ast, n)
            
        self.assertDictEqual(ground_truth, if_then_mapping, "Incorrect if-then mapping.")
        
    def test_method2_get_then_statements(self):
        self.maxDiff = None
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method2_if_stmnts_ast.json')
        ground_truth = {
            "1000108": "1000112"
        }
        if_nodes = ground_truth.keys()
        if_then_mapping = {}
        
        for n in if_nodes:
            if_then_mapping[n] = NodeUtils.get_if_then(ast, n)
            
        self.assertDictEqual(ground_truth, if_then_mapping, "Incorrect if-then mapping.")
        
class IdentifiersCollectorTestCase(unittest.TestCase):
    def test_method_collect_identifiers(self):
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method_if_stmnts_ast.json')
        root = "1000140"
        ground_truth = set(["1000143", "1000146", "1000148", "1000151", "1000155", "1000159"])
        identifiers = set(NodeUtils.identifier_collector(ast, root))
        
        self.assertSetEqual(ground_truth, identifiers, "Incorect set of identifiers.")
        
    def test_method2_collect_identifiers(self):
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method2_if_stmnts_ast.json')
        root = "1000101"
        ground_truth = set(["1000106", "1000110", "1000113"])
        identifiers = set(NodeUtils.identifier_collector(ast, root))
        
        self.assertSetEqual(ground_truth, identifiers, "Incorect set of identifiers.")
    
    def test_method3_collect_identifiers(self):
        ast = load_json(f'{JSON_FILES}/get_while_statements/test_method_while_stmnts_ast.json')
        root = "1000134"
        ground_truth = set(["1000136", "1000137", "1000142", "1000144", "1000147", "1000148"])
        identifiers = set(NodeUtils.identifier_collector(ast, root))
        
        self.assertSetEqual(ground_truth, identifiers, "Incorect set of identifiers.")
    
    def test_method4_collect_identifiers(self):
        ast = load_json(f'{JSON_FILES}/test_method_cmptd_frm_ast.json')
        root = "1000114"
        ground_truth = set(["1000115", "1000118", "1000119", "1000122"])
        identifiers = set(NodeUtils.identifier_collector(ast, root))
        
        self.assertSetEqual(ground_truth, identifiers, "Incorect set of identifiers.")

class GetIfGuardExpressionTestCase(unittest.TestCase):
    
    def test_method_get_if_guard_expression(self):
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method_if_stmnts_ast.json')
        if_node = "1000111"
        ground_truth = "1000112"
        guard_expression_node = NodeUtils.get_if_condition(ast, if_node)
        
        self.assertEqual(ground_truth, guard_expression_node, "Incorrect guard expression node.")
        
    def test_method2_get_if_guard_expression(self):
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method2_if_stmnts_ast.json')
        if_node = "1000108"
        ground_truth = "1000109"
        guard_expression_node = NodeUtils.get_if_condition(ast, if_node)
        
        self.assertEqual(ground_truth, guard_expression_node, "Incorrect guard expression node.")
        
    def test_method3_get_if_guard_expression(self):
        ast = load_json(f'{JSON_FILES}/test_method3_ast.json')
        if_node = "1000114"
        ground_truth = "1000115"
        guard_expression_node = NodeUtils.get_if_condition(ast, if_node)
        
        self.assertEqual(ground_truth, guard_expression_node, "Incorrect guard expression node.")
        
    def test_method4_get_if_guard_expression(self):
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method3_if_stmnts_ast.json')
        if_node = "1000124"
        ground_truth = "1000125"
        guard_expression_node = NodeUtils.get_if_condition(ast, if_node)
        
        self.assertEqual(ground_truth, guard_expression_node, "Incorrect guard expression node.")

class GetIfBodyTestCase(unittest.TestCase):
    def test_method_get_if_body(self):
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method_if_stmnts_ast.json')
        if_node = "1000111"
        ground_truth = "1000115"
        body_node = NodeUtils.get_if_then(ast, if_node)
        
        self.assertEqual(ground_truth, body_node, "Incorrect body node.")
        
    def test_method2_get_if_body(self):
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method2_if_stmnts_ast.json')
        if_node = "1000108"
        ground_truth = "1000112"
        body_node = NodeUtils.get_if_then(ast, if_node)
        
        self.assertEqual(ground_truth, body_node, "Incorrect body node.")
        
    def test_method3_get_if_body(self):
        ast = load_json(f'{JSON_FILES}/test_method3_ast.json')
        if_node = "1000114"
        ground_truth = "1000118"
        body_node = NodeUtils.get_if_then(ast, if_node)
        
        self.assertEqual(ground_truth, body_node, "Incorrect body node.")
        
    def test_method4_get_if_body(self):
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method4_if_stmnts_ast.json')
        if_node = "1000124"
        ground_truth = "1000137"
        body_node = NodeUtils.get_if_then(ast, if_node)
        
        self.assertEqual(ground_truth, body_node, "Incorrect body node.")

class GetElseStatementTestCase(unittest.TestCase):
    
    def test_method_get_else_statement(self):
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method_if_else_stmnts_ast.json')
        if_node = "1000124"
        ground_truth = "1000144"
        
        else_node = NodeUtils.get_if_else(ast, if_node)
        
        self.assertEqual(ground_truth, else_node, "Incorrect else node.")
        
    def test_method2_get_else_statement(self):
        ast = load_json(f'{JSON_FILES}/get_if_statements/test_method_if_stmnts_ast.json')
        if_node = "1000136"
        ground_truth = None
        
        else_node = NodeUtils.get_if_else(ast, if_node)
        
        self.assertEqual(ground_truth, else_node, "Incorrect else node.")

if __name__ == '__main__':
    unittest.main()