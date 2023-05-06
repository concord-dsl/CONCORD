import itertools
import more_itertools
import networkx as nx

import inspect
import logging
from utils.last_write_read.ExtraNodeProps import ExtraNodeProps
from utils.last_write_read.LastReadWritePreProcessor import LastReadWriteProcessor
from utils.last_write_read.NodeType import NodeType
from utils.last_write_read.NodeUtils import NodeUtils

from utils.variables import get_variable_occurences
from utils.graph import get_ast, get_local_variables, get_method_parameters, get_parent_nodes_mapping, get_token_nodes, get_variable_assignments, save
from utils.statements import get_for_statements, get_if_statements, get_return_statements, get_while_statements

class AddOperations:
    
    @staticmethod
    def last_lexical_use(graph: nx.MultiDiGraph):
        if not graph:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Null graph, skipping')
            return graph
        ast = get_ast(graph)  
        if not ast:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph
           
        _vars = get_local_variables(ast) + get_method_parameters(ast)
        
        for v in _vars:
            v_occ = get_variable_occurences(graph, v)
            if v_occ:
                v_occ_edges = list(more_itertools.pairwise(v_occ))
                graph.add_edges_from(v_occ_edges, label="LAST_LEXICAL_USE")
            
        logging.info(f'{inspect.currentframe().f_code.co_name} [OK]')
        return graph
            
    
    @staticmethod
    def computed_from(graph: nx.MultiDiGraph):
        if not graph:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Null graph, skipping')
            return graph
        ast = get_ast(graph)  
        if not ast:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph
        
        # get assignment statements
        ast_nodes = ast.nodes()
        assignment_ops = {
            NodeType.OP_ASSIGNMENT, NodeType.OP_ASSIGN_PLUS, 
            NodeType.OP_ASSIGN_MINUS, NodeType.OP_ASSIGN_MUL, 
            NodeType.OP_ASSIGN_DIV, NodeType.OPS_ASSIGN_AND, 
            NodeType.OPS_ASSIGN_OR, NodeType.OPS_ASSIGN_XOR, 
            NodeType.OPS_ASSIGN_MOD, NodeType.OPS_ASSIGN_SHIFT_LEFT, 
            NodeType.OPS_ASSIGN_ARITH_SHIFT_RIGHT, NodeType.OPS_ASSIGN_LOGICAL_SHIFT_RIGHT
            }
        
        assginment_nodes = set(filter(lambda n: NodeUtils.get_node_type(ast, n) in assignment_ops, ast_nodes))
        # links lhs node to rhs identifier nodes
        c=0
        for a_node in assginment_nodes:
            lhs, rhs = NodeUtils.get_assign_expr_target_val(ast, a_node)
            rhs_nodes = NodeUtils.identifier_collector(ast, rhs)
            for rhs_node in rhs_nodes:
                graph.add_edge(lhs, rhs_node, label="COMPUTED_FROM", key=f'CF{c}')
                c+=1
                        
        return graph
    
    @staticmethod
    def next_token(graph: nx.MultiDiGraph):
        # Extract AST
        ast = get_ast(graph)
        # If the AST cannot be extracted we return the graph as is
        if not ast:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph
        # Get token nodes
        token_nodes = get_token_nodes(ast)
        # Sort the nodes (note that the nodes are returned in the following format (<NODE-ID>, 0))
        token_nodes.sort(key=lambda x: x[0])
        # Method signature node is added at the end of the list, so I need to re-insert at the start.
        last_node = token_nodes.pop()
        token_nodes.insert(0, last_node)
        # Add edges between token nodes
        n = len(token_nodes) - 1
        label = "NCS"
        for i in range(n):
            graph.add_edge(token_nodes[i][0], token_nodes[i+1][0], label=label)
            
        logging.info(f'{inspect.currentframe().f_code.co_name} [OK]')
        
        return graph
    
    @staticmethod
    def next_sibling(graph: nx.MultiDiGraph):
        if not graph:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Null graph, skipping')
            return graph
        ast = get_ast(graph)
        if not ast:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph

        p_c_mapping = get_parent_nodes_mapping(graph)
                
        if not p_c_mapping:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract Parent-Children Mapping, skipping')
            return graph
        
        p_c_mapping_values = p_c_mapping.values()
        next_sib_edges = list(itertools.chain.from_iterable(list(map(lambda x: list(more_itertools.pairwise(x)), p_c_mapping_values))))
        
        graph.add_edges_from(next_sib_edges, label="NEXT_SIB")        
        logging.info(f'{inspect.currentframe().f_code.co_name} [OK]')
        
        return graph
    
    
    @staticmethod
    def for_exec(graph: nx.MultiDiGraph):
        if not graph:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Null graph, skipping')
            return graph
        ast = get_ast(graph)  
        if not ast:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph
        # Get for loops
        for_loops = get_for_statements(ast)
        
        if not for_loops:
            logging.warn(f'{inspect.currentframe().f_code.co_name} No For loops were found, skipping')
            return graph
        
        c1 = 0
        c2 = 0
        for fl in for_loops:
            fl_children = list(ast.successors(fl)) 
            for_body_node = None
            for_control_nodes = []
            
            for fl_c in fl_children:
                _type = ast.nodes[fl_c]['label']
                if "BLOCK,<empty>,<empty>" in _type:
                    for_body_node = fl_c
                else:
                    for_control_nodes.append(fl_c)
                    
            # Special case:
            # for(<CONTROL-STATEMENTS>) <statement> --> there's no BLOCK node since there no braces {} after the for statement.
            if not for_body_node:
                # <statement> is the last node in for_control_nodes
                for_body_node = for_control_nodes.pop()
                
            # Add edges (adding key for safety, although since it's an AST no edge should exist between these nodes)
            for fcn in for_control_nodes:
                if not fcn or not for_body_node:
                    continue
                graph.add_edge(fcn, for_body_node, key=f'for{c1}', label='FOR_EXEC')
                graph.add_edge(for_body_node, fcn, key=f'for{c2}', label='FOR_NEXT')
            
                c1 += 1
                c2 += 1            
                    
        
        logging.info(f'{inspect.currentframe().f_code.co_name} [OK]')
        return graph
    
    @staticmethod
    def while_exec(graph: nx.MultiDiGraph):
        if not graph:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Null graph, skipping')
            return graph
        ast = get_ast(graph)  
        if not ast:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph
        # Get while loops
        while_loops = get_while_statements(ast)
        
        if not while_loops:
            logging.warn(f'{inspect.currentframe().f_code.co_name} No While loops were found, skipping')
            return graph
        
        c1 = 0
        c2 = 0
        for wl in while_loops:
            wl_children = list(ast.successors(wl)) # We are using the AST so we can be sure that the while loop root node has only two
                                                   # successors: the while condition and the while body block.
            while_body_node = None
            while_condition_node = None
            
            for wl_c in wl_children:
                _type = ast.nodes[wl_c]['label']
                if "BLOCK,<empty>,<empty>" in _type:
                    while_body_node = wl_c
                else:
                    while_condition_node = wl_c
            if not while_body_node or not while_condition_node:
                continue
            # Add edges (adding key for safety, although since it's an AST no edge should exist between these nodes)
            graph.add_edge(while_body_node, while_condition_node, key=f'while{c1}', label='WHILE_NEXT')
            graph.add_edge(while_condition_node, while_body_node, key=f'while{c2}', label='WHILE_EXEC')
            
            c1 += 1
            c2 += 1            
                    
        
        logging.info(f'{inspect.currentframe().f_code.co_name} [OK]')
        return graph
    
    @staticmethod
    def guarded_by(graph: nx.MultiDiGraph):
        if not graph:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Null graph, skipping')
            return graph
        ast = get_ast(graph)  
        if not ast:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph
        # Get if statements
        ifs = get_if_statements(ast)
        
        if not ifs:
            logging.warn(f'{inspect.currentframe().f_code.co_name} No If statements were found, skipping')
            return graph
        
        for if_node in ifs:
            if_guard = NodeUtils.get_if_condition(ast, if_node)
            if not if_guard:
                continue
            if_guard_identifiers = NodeUtils.identifier_collector(ast, if_guard)
            # Create a map for faster lookups later on
            # <identifier-name, node-id>
            if_guard_identifiers = {NodeUtils.get_identifier_name(ast, node):node for node in if_guard_identifiers}
            then_stmnt = NodeUtils.get_if_then(ast, if_node)
           
            # This mapping is the opposite for then-statements identifiers: <node-id, identifier-name>
            then_identifiers = NodeUtils.identifier_collector(ast, then_stmnt)
            then_identifiers = {identifier:NodeUtils.get_identifier_name(ast, identifier) for identifier in then_identifiers}
            
            gb_key = 0
            
            for then_id, then_id_val in then_identifiers.items():
                
                if then_id_val in if_guard_identifiers:
                    # Add edge
                    graph.add_edge(then_id, if_guard_identifiers[then_id_val], key=f'GB{gb_key}' ,label='GUARDED_BY')
                    gb_key += 1
                
            else_stmnt = NodeUtils.get_if_else(ast, if_node)
            gbn_key = 0
            
            if else_stmnt:
                else_identifiers = NodeUtils.identifier_collector(ast, else_stmnt)
                else_identifiers = {identifier:NodeUtils.get_identifier_name(ast, identifier) for identifier in else_identifiers}
                for else_id, else_id_val in else_identifiers.items():
                    if else_id_val in if_guard_identifiers:
                        graph.add_edge(else_id, if_guard_identifiers[else_id_val], key=f'GBN{gbn_key}', label='GURADED_BY_NEGATION')
                        gbn_key += 1
                        
        logging.info(f'{inspect.currentframe().f_code.co_name} [OK]')
        return graph
        
    @staticmethod
    def last_read_write(graph: nx.MultiDiGraph):
        
        if not graph:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Null graph, skipping')
            return graph
        ast = get_ast(graph)  
        if not ast:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph
        
        nodes = ast.nodes()
        lrwp = LastReadWriteProcessor(ast)
        lrwp.preprocess()
        lrwp.process(nodes[0])
        
        for n in nodes:
            if 'ExtraNodeProps' in ast.nodes[n]:
                enp: ExtraNodeProps = ast.nodes[n]['ExtraNodeProps']
                
                u = enp.get_nx_id()
                other_nodes = enp.get_other_nodes()
                c=0
                c2=0
                for v in other_nodes['LAST_WRITE']:
                    graph.add_edge(u,v.get_nx_id(), label='LAST_WRITE', key=f'LW_{c}')
                    c+=1
                    
                for v in other_nodes['LAST_READ']:
                    graph.add_edge(u,v.get_nx_id(), label='LAST_WRITE', key='LR_{c2}')
                    c2+=1    
        
        logging.info(f'{inspect.currentframe().f_code.co_name} [OK]')
        return graph
    
    @staticmethod
    def returns_to(graph: nx.MultiDiGraph):
        
        if not graph:
            logging.warn(f'{inspect.currentframe().f_code.co_name} Null graph, skipping')
            return graph
        ast = get_ast(graph)  
        if not ast:
            #logging.warn(f'{inspect.currentframe().f_code.co_name} Could not extract AST, skipping')
            return graph
        
        nodes = ast.nodes()
        # Get return statements
        returns = get_return_statements(ast)
        if not returns:
            logging.warn(f'{inspect.currentframe().f_code.co_name} No return statements found, skipping')
            return graph
        # Get method name node
        method_name = list(filter(lambda node: NodeUtils.get_node_type(ast, node) == NodeType.METHOD_DECLARATION, nodes))[0]
        # Get method return node
        method_return = list(filter(lambda node: NodeUtils.get_node_type(ast, node) == NodeType.METHOD_RETURN, nodes))[0]
        c = 0
        for rn in returns:
            graph.add_edge(rn, method_name, label="RETURNS_TO", key=f'RTN{c}')
            graph.add_edge(rn, method_return, label="RETURNS_TO", key=f'RTR{c}')
            c += 1
        
        logging.info(f'{inspect.currentframe().f_code.co_name} [OK]')
        return graph