import networkx as nx
from utils.last_write_read.NodeUtils import NodeUtils
from utils.last_write_read.LexicalNode import LexicalNode
from utils.last_write_read.NodeType import NodeType


class LexicalNodeFactory:
    MDG = nx.MultiDiGraph
    @staticmethod
    def getLexicalNode(graph: MDG, node):
        
        if NodeUtils.get_node_type(graph, node) == NodeType.METHOD_DECLARATION:
            block_node = NodeUtils.get_method_block_node(graph, node)
            if not block_node:
                raise ValueError("Method is part of an interface")
            
            lexicalNode = LexicalNode(graph, block_node)
            params = NodeUtils.get_method_parameters(graph, node)
            
            for p in params:
                lexicalNode.add_parameter(p)
            
            return lexicalNode
        
        if NodeUtils.get_node_type(graph, node) == NodeType.BLOCK_STATEMENT:
            return LexicalNode(graph, node)
        
        if NodeUtils.get_node_type(graph, node) == NodeType.FOR_STATEMENT:
            return LexicalNode(graph, node)
        
        else:
            raise ValueError('Not Implemented')
            # Missing LambdaExpressions
            