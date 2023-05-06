#  This work is a Python port of the original work done by cvitkovic et al.
#  Repo: https://github.com/mwcvitkovic/Open-Vocabulary-Learning-on-Source-Code-with-a-Graph-Structured-Cache--Code-Preprocessor
#  There were multiple changes made to accomodate the differences between the generated AST by joern and the AST generated in the original repo.
#  + other helper functions.


from typing import Any
import networkx as nx

from utils.last_write_read.ExtraNodeProps import ExtraNodeProps
from utils.last_write_read.NodeType import NodeType
from utils.last_write_read.NodeUtils import NodeUtils
from utils.last_write_read.LexicalNodeFactory import LexicalNodeFactory
from utils.last_write_read.LexicalNode import LexicalNode

MDG = nx.MultiDiGraph


class LastReadWriteProcessor:
    
    lexicalClasses = {NodeType.METHOD_DECLARATION, NodeType.BLOCK_STATEMENT}
    
    def __init__(self, graph: MDG) -> None:
        self.graph = graph
        
    def preprocess(self):
        nodes = self.graph
        for n in nodes:
            if NodeUtils.get_node_type(self.graph, n) in {NodeType.IDENTIFIER, NodeType.PARAMETER, NodeType.LOCAL_DECLARATION}:
                self.graph.nodes[n]['ExtraNodeProps'] = ExtraNodeProps(NodeUtils.get_identifier_name(self.graph, n), n)

    def process(self, general_node: str) -> None:
        if NodeUtils.get_node_type(self.graph, general_node) in self.lexicalClasses:
            lexical_nodes: list[LexicalNode] = []
            try:
              lexical_node = LexicalNodeFactory.getLexicalNode(self.graph, general_node)
            except ValueError as e:
                return
            lexical_nodes.append(lexical_node)
            self.traverse_ls(self.get_child_node(lexical_node.get_node()), lexical_nodes)
        else:
            for child in self.get_child_node(general_node):
                self.process(child)
    
    def get_child_node(self, node) -> 'list[str]':
        return list(self.graph.successors(node))
    
    # WARNING: weird method naming up ahead (because there's no method overloading in python (not entirely true though.))
    
    def traverse_ls(self, node_list: 'list[str]', lexical_nodes: 'list[LexicalNode]') -> None:
        self.traverse_lsb(node_list, lexical_nodes, False)
        
    def traverse_lsb(self, node_list: 'list[str]', lexical_nodes: 'list[LexicalNode]', new_write: bool) -> None:
        for node in node_list:
            self.traverse_nsb(node, lexical_nodes, new_write)
    
    def traverse_ns(self, node: str, lexical_nodes: 'list[LexicalNode]') -> None:
        self.traverse_nsb(node, lexical_nodes, False)
    
    def traverse_nsb(self, node: str, lexical_nodes: 'list[LexicalNode]', new_write: bool) -> None:
        child_node: list[str] = self.get_child_node(node)
        # Handling Local Variable Declators
        if NodeUtils.get_node_type(self.graph, node) == NodeType.LOCAL_DECLARATION:
            name_node = NodeUtils.get_variable_name_from_local(self.graph, node)
            lexical_nodes[-1].add_variable(node)
            self.traverse_ls(child_node, lexical_nodes)
        
        # Handling For Statements
        elif NodeUtils.get_node_type(self.graph, node) == NodeType.FOR_STATEMENT:
            lexical_nodes.append(LexicalNodeFactory.getLexicalNode(self.graph, node))
            self.traverse_ls(NodeUtils.get_for_loop_initializations(self.graph, node), lexical_nodes)
            for_comps = NodeUtils.get_for_loops_compares(self.graph, node)
            if for_comps:
                self.traverse_ns(for_comps[0], lexical_nodes)
            self.stack_lexical_node(lexical_nodes)
            for_loop_body = NodeUtils.get_for_loop_body(self.graph, node)
            self.traverse_ns(for_loop_body, lexical_nodes)
            for_loop_updates = NodeUtils.get_for_loop_updates(self.graph, node)
            self.traverse_ls(for_loop_updates[0], lexical_nodes)
            if for_comps:
                self.traverse_ns(for_comps[0], lexical_nodes)
            self.destack_lexical_node(lexical_nodes, True)
            lexical_nodes.pop()
       
        # Handling While Statements        
        elif NodeUtils.get_node_type(self.graph, node) == NodeType.WHILE_STATEMENT:
            self.traverse_ls([NodeUtils.get_while_statement_condition(self.graph, node)], lexical_nodes)
            self.stack_lexical_node(lexical_nodes)
            self.traverse_ls([NodeUtils.get_while_statement_body(self.graph, node)], lexical_nodes)
            self.traverse_ls([NodeUtils.get_while_statement_condition(self.graph, node)], lexical_nodes)
            self.destack_lexical_node(lexical_nodes, True)
        
        # Handling Unary Expressions
        elif NodeUtils.get_node_type(self.graph, node) in {NodeType.OP_NOT, NodeType.OP_LOGICAL_NOT, NodeType.OP_MINUS, NodeType.OP_PLUS, NodeType.OP_POST_DECREMENT, NodeType.OP_POST_INCREMENT, NodeType.OP_PRE_DECREMENT, NodeType.OP_PRE_INCREMENT}:
            self.traverse_lsb(child_node, lexical_nodes, True)
        
        # Handling Assignment Expressions
        elif NodeUtils.get_node_type(self.graph, node) in {NodeType.OP_ASSIGNMENT, NodeType.OP_ASSIGN_PLUS, NodeType.OP_ASSIGN_MINUS, NodeType.OP_ASSIGN_MUL, NodeType.OP_ASSIGN_DIV, NodeType.OPS_ASSIGN_AND, NodeType.OPS_ASSIGN_OR, NodeType.OPS_ASSIGN_XOR, NodeType.OPS_ASSIGN_MOD, NodeType.OPS_ASSIGN_SHIFT_LEFT, NodeType.OPS_ASSIGN_ARITH_SHIFT_RIGHT, NodeType.OPS_ASSIGN_LOGICAL_SHIFT_RIGHT}:
            if len(child_node) != 2:
                raise ValueError("Not Expected")
            lhs, rhs = NodeUtils.get_assign_expr_target_val(self.graph, node)
            self.traverse_nsb(lhs, lexical_nodes, False)
            self.traverse_nsb(rhs, lexical_nodes, True)
            
        elif NodeUtils.get_node_type(self.graph, node) in self.lexicalClasses:
            lexical_nodes.append(LexicalNodeFactory.getLexicalNode(self.graph, node))
            self.traverse_ls(child_node, lexical_nodes)
            lexical_nodes.pop()
         
        # Handling If Statements   
        elif NodeUtils.get_node_type(self.graph, node) == NodeType.IF_STATEMENT:
            if_cond = NodeUtils.get_if_condition(self.graph, node)  
            self.traverse_ls([if_cond], lexical_nodes)
            self.stack_lexical_node(lexical_nodes)
            
            then_stmnt = NodeUtils.get_if_then(self.graph, node)
            self.traverse_ls([then_stmnt], lexical_nodes)
            
            else_stmnt = NodeUtils.get_if_else(self.graph, node)
            if else_stmnt:
                for lexnode in lexical_nodes:
                    lexnode.shuffle_stack_variable()
                self.traverse_ls([else_stmnt], lexical_nodes)
                
            self.destack_lexical_node(lexical_nodes, False)
            
        
        # Handling Identifier Nodes
        elif NodeUtils.get_node_type(self.graph, node) == NodeType.IDENTIFIER:
            name_node = node
            for lexical_node in lexical_nodes:
                if lexical_node.has_variable(name_node):
                    lexical_node.set_and_update_variable_pointer(name_node, 'LAST_READ')
                    if new_write:
                        lexical_node.set_and_update_variable_pointer(name_node, 'LAST_WRITE')
                    else:
                        lexical_node.set_variable_pointer(name_node, 'LAST_WRITE')
                    break
                
        else:
            self.traverse_lsb(child_node, lexical_nodes, new_write)
        # Do While skipped
        # ForEach skipped
        # ThisExpr skipped (for java: this.*)
        
    
    def destack_lexical_node(self, lexical_nodes: 'list[LexicalNode]', completeLoop: bool) -> None:
        for lexical_node in lexical_nodes:
            lexical_node.destack_variable(completeLoop)
    
    
    def stack_lexical_node(self, lexical_nodes: 'list[LexicalNode]') -> None:
        for lexical_node in lexical_nodes:
            lexical_node.stack_variable()