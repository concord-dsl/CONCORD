import networkx as nx
from utils.last_write_read.ExtraNodeProps import ExtraNodeProps
from utils.last_write_read.NodeType import NodeType

MDG = nx.MultiDiGraph


class NodeUtils:

    @staticmethod
    def get_node_type(graph: MDG, node) -> NodeType:
        label: list[str] = graph.nodes[node]['label'][1:-1].split(',')
        if len(label) == 2:
            if label[0] == 'METHOD':
                return NodeType.METHOD_DECLARATION
            elif label[0] == 'LOCAL':
                return NodeType.LOCAL_DECLARATION
            elif label[0] == 'METHOD_RETURN':
                return NodeType.METHOD_RETURN
            elif label[0] == 'PARAM':
                return NodeType.PARAMETER
            elif label[0] == '<operator>.assignment':
                return NodeType.OP_ASSIGNMENT
            elif label[0] == '<operator>.lessThan':
                return NodeType.OP_LESS_THAN
            elif label[0] == '<operator>.greaterThan':
                return NodeType.OP_GREATER_THAN
            elif label[0] == '<operator>.greaterEqualsThan':
                return NodeType.OP_GREATER_EQUALS_THAN
            elif label[0] == '<operator>.lessEqualsThan':
                return NodeType.OP_LESS_EQUALS_THAN
            elif label[0] == '<operator>.equals':
                return NodeType.OP_EQUALS
            elif label[0] == '<operator>.postDecrement':
                return NodeType.OP_POST_DECREMENT
            elif label[0] == '<operator>.postIncrement':
                return NodeType.OP_POST_INCREMENT
            elif label[0] == '<operator>.preDecrement':
                return NodeType.OP_PRE_DECREMENT
            elif label[0] == '<operator>.preIncrement':
                return NodeType.OP_PRE_INCREMENT
            elif label[0] == "<operator>.and":
                return NodeType.OP_ADD
            elif label[0] == "<operator>.elvis":
                return NodeType.OP_ELVIS
            elif label[0] == "<operator>.addressOf":
                return NodeType.OP_ADDRR_OF
            elif label[0] == "<operator>.instanceOf":
                return NodeType.OP_INSTANCE_OF
            elif label[0] == "<operator>.indirectFieldAccess":
                return NodeType.OP_INDIR_FIELD_ACC
            elif label[0] == "<operator>.not":
                return NodeType.OP_NOT
            elif label[0] == "<operator>.sizeOf":
                return NodeType.OP_SIZE_OF
            elif label[0] == "<operators>.assignmentModulo":
                return NodeType.OPS_ASSIGN_MOD
            elif label[0] == "<operator>.fieldAccess":
                return NodeType.OP_FIELD_ACC
            elif label[0] == "<operator>.multiplication":
                return NodeType.OP_MULT
            elif label[0] == "<operator>.subtraction":
                return NodeType.OP_SUB
            elif label[0] == "<operator>.addition":
                return NodeType.OP_ADD
            elif label[0] == "<operator>.xor":
                return NodeType.OP_XOR
            elif label[0] == "<operator>.formattedValue":
                return NodeType.OP_FORMATTED_VAL
            elif label[0] == "<operator>.pointerShift":
                return NodeType.OP_PTR_SHIFT
            elif label[0] == "<operator>.range":
                return NodeType.OP_RANGE
            elif label[0] == "<operator>.arithmeticShiftRight":
                return NodeType.OP_ARITH_SHIFT_RIGHT
            elif label[0] == "<operator>.assignmentMinus":
                return NodeType.OP_ASSIGN_MINUS
            elif label[0] == "<operator>.logicalOr":
                return NodeType.OP_LOGICAL_OR
            elif label[0] == "<operators>.assignmentExponentiation":
                return NodeType.OPS_ASSIGN_EXP
            elif label[0] == "<operator>.cast":
                return NodeType.OP_CAST
            elif label[0] == "<operator>.is":
                return NodeType.OP_IS
            elif label[0] == "<operators>.assignmentAnd":
                return NodeType.OPS_ASSIGN_AND
            elif label[0] == "<operators>.assignmentLogicalShiftRight":
                return NodeType.OPS_ASSIGN_LOGICAL_SHIFT_RIGHT
            elif label[0] == "<operator>.arrayInitializer":
                return NodeType.OP_ARRAY_INITALIZE
            elif label[0] == "<operator>.in":
                return NodeType.OP_IN
            elif label[0] == "<operator>.getElementPtr":
                return NodeType.OP_GET_ELT_PTR
            elif label[0] == "<operator>.assignmentDivision":
                return NodeType.OP_ASSIGN_DIV
            elif label[0] == "<operator>.minus":
                return NodeType.OP_MINUS
            elif label[0] == "<operator>.logicalShiftRight":
                return NodeType.OP_LOGICAL_SHIFT_RIGHT
            elif label[0] == "<operator>.logicalAnd":
                return NodeType.OP_LOGICAL_AND
            elif label[0] == "<operator>.logicalNot":
                return NodeType.OP_LOGICAL_NOT
            elif label[0] == "<operator>.formatString":
                return NodeType.OP_FORMAT_STR
            elif label[0] == "<operator>.notEquals":
                return NodeType.OP_NOT_EQUALS
            elif label[0] == "<operator>.assignmentPlus":
                return NodeType.OP_ASSIGN_PLUS
            elif label[0] == "<operator>.exponentiation":
                return NodeType.OP_EXP
            elif label[0] == "<operator>.notIn":
                return NodeType.OP_NOT_IN
            elif label[0] == "<operator>.plus":
                return NodeType.OP_PLUS
            elif label[0] == "<operator>.indirectComputedMemberAccess":
                return NodeType.OP_INDIRECTED_COMPUTED_MEMBER_ACCESS
            elif label[0] == "<operator>.indirection":
                return NodeType.OP_INDIRECTION
            elif label[0] == "<operator>.delete":
                return NodeType.OP_DELETE
            elif label[0] == "<operator>.indexAccess":
                return NodeType.OP_IDX_ACCESS
            elif label[0] == "<operator>.indirectMemberAccess":
                return NodeType.OP_INDIRECT_MEMBER_ACCESS
            elif label[0] == "<operator>.modulo":
                return NodeType.OP_MOD
            elif label[0] == "<operators>.assignmentOr":
                return NodeType.OPS_ASSIGN_OR
            elif label[0] == "<operator>.memberAccess":
                return NodeType.OP_MEMBER_ACCESS
            elif label[0] == "<operator>.conditional": # Ternary Operator, e.g: a ? consequent : alternate (taken from shiftleft's repo).
                return NodeType.OP_CONDITIONAL
            elif label[0] == "<operator>.or":
                return NodeType.OP_OR
            elif label[0] == "<operator>.computedMemberAccess":
                return NodeType.OP_COMPUTED_MEMBER_ACCESS
            elif label[0] == "<operator>.division":
                return NodeType.OP_DIV
            elif label[0] == "<operator>.shiftLeft":
                return NodeType.OP_SHIFT_LEFT
            elif label[0] == "<operator>.compare": # Comparison between two arguments with the results: 0 == equal, negative == left < right, positive == left > right (taken from shiftleft's repo).
                return NodeType.OP_COMPARE
            elif label[0] == "<operator>.lengthOf":
                return NodeType.OP_LENGTH_OF
            elif label[0] == "<operators>.assignmentArithmeticShiftRight":
                return NodeType.OPS_ASSIGN_ARITH_SHIFT_RIGHT
            elif label[0] == "<operator>.indirectIndexAccess":
                return NodeType.OP_INDIRECT_INDEX_ACCESS
            elif label[0] == "<operators>.assignmentXor":
                return NodeType.OPS_ASSIGN_XOR
            elif label[0] == "<operator>.notNullAssert":
                return NodeType.OP_NOT_NULL_ASSERT
            elif label[0] == "<operator>.safeNavigation":
                return NodeType.OP_SAFE_NAVIGATION
            elif label[0] == "<operators>.assignmentShiftLeft":
                return NodeType.OPS_ASSIGN_SHIFT_LEFT
            elif label[0] == "<operator>.assignmentMultiplication":
                return NodeType.OP_ASSIGN_MUL
            elif label[0] == "<operator>.isNot":
                return NodeType.OP_IS_NOT
            elif graph.nodes[node]['type'] == 'CALL':
                return NodeType.METHOD_CALL

        elif len(label) == 3:
            if label[0] == 'BLOCK' and label[1] == '<empty>' and label[2] == '<empty>':
                return NodeType.BLOCK_STATEMENT
            elif label[0] == 'IDENTIFIER':
                return NodeType.IDENTIFIER
            elif label[0] == 'LITERAL':
                return NodeType.LITERAL
            elif label[0] == 'FIELD_IDENTIFIER':
                return NodeType.FIELD_IDENTIFIER
            elif label[0] == 'CONTROL_STRUCTURE':
                control_struct_type = label[1].split(' ')[0]
                if control_struct_type == 'if':
                    return NodeType.IF_STATEMENT
                elif control_struct_type == 'while':
                    return NodeType.WHILE_STATEMENT
                elif control_struct_type == 'for':
                    return NodeType.FOR_STATEMENT
                elif control_struct_type == 'else':
                    return NodeType.ELSE_STATEMENT
                elif control_struct_type == 'try':
                    return NodeType.TRY_STATEMENT
            elif label[0] == "RETURN":
                return NodeType.RETURN_STATEMENT

        return NodeType.UNKNOWN

    @staticmethod
    def label_splitter(graph: MDG, node) -> 'list[str]':
        return graph.nodes[node]['label'][1:-1].split(',')

    @staticmethod
    def get_method_block_node(graph: MDG, method_node) -> str:
        children = list(graph.successors(method_node))
        block_node = None
        for c in children:
            if NodeUtils.get_node_type(graph, c) == NodeType.BLOCK_STATEMENT:
                block_node = c
                break

        return block_node

    @staticmethod
    def get_method_parameters(graph: MDG, method_node) -> 'list[ExtraNodeProps]':
        children = list(graph.successors(method_node))
        params = []
        for c in children:
            if NodeUtils.get_node_type(graph, c) == NodeType.PARAMETER:
                params.append(c)

        return params

    @staticmethod
    def get_variable_name_from_local(graph: MDG, node: str) -> str:
        result = NodeUtils.label_splitter(graph, node)
        return result[1].split(':')[0].split(' ')[1]

    @staticmethod
    def get_for_loop_initializations(graph: MDG, node: str) -> 'list[str]':
        for_loop_children = list(graph.successors(node))
        for_inits = []
        comparators = {
            NodeType.OP_GREATER_THAN,
            NodeType.OP_GREATER_EQUALS_THAN,
            NodeType.OP_LESS_THAN,
            NodeType.OP_LESS_EQUALS_THAN,
            NodeType.OP_EQUALS
        }
        # Traversal of nodes is LR, when we reach a comparison node, init statements are done
        for child in for_loop_children:
            if NodeUtils.get_node_type(graph, node) in comparators:
                break
            if NodeUtils.get_node_type(graph, node) == NodeType.OP_ASSIGNMENT:
                for_inits.append(child)

        return for_inits

    @staticmethod
    def get_for_loops_compares(graph: MDG, node: str) -> 'list[str]':
        for_loop_children = list(graph.successors(node))
        for_compares = []
        is_block_exists = False

        comparators = {
            NodeType.OP_GREATER_THAN,
            NodeType.OP_GREATER_EQUALS_THAN,
            NodeType.OP_LESS_THAN,
            NodeType.OP_LESS_EQUALS_THAN,
            NodeType.OP_EQUALS
        }

        for child in for_loop_children:
            if NodeUtils.get_node_type(graph, child) == NodeType.BLOCK_STATEMENT:
                is_block_exists = True
                break

            if NodeUtils.get_node_type(graph, child) in comparators:
                for_compares.append(child)

        return for_compares

    @staticmethod
    def get_for_loop_body(graph: MDG, node: str) -> str:

        for_loop_children = list(graph.successors(node))
        is_there_block = False
        block_node = None

        for child in for_loop_children:
            if NodeUtils.get_node_type(graph, child) == NodeType.BLOCK_STATEMENT:
                is_there_block = True
                block_node = child
                break

        if is_there_block:
            return block_node

        else:
            return for_loop_children[-1]

    @staticmethod
    def get_for_loop_updates(graph: MDG, node: str) -> 'list[str]':

        for_loop_children = list(graph.successors(node))
        for_loop_children.pop()
        for_loop_children.reverse()
        comparators = {
            NodeType.OP_GREATER_THAN,
            NodeType.OP_GREATER_EQUALS_THAN,
            NodeType.OP_LESS_THAN,
            NodeType.OP_LESS_EQUALS_THAN,
            NodeType.OP_EQUALS
        }
        updates = []
        for child in for_loop_children:
            if NodeUtils.get_node_type(graph, child) in comparators:
                break
            updates.append(child)

        return updates

    @staticmethod
    def get_while_statement_condition(graph: MDG, node: str) -> 'list[str]':
        while_cond_children = list(graph.successors(node))
        # First child is the condition, the rest is the body
        return while_cond_children[0]
    
    @staticmethod
    def get_while_statement_body(graph: MDG, node: str) -> 'list[str]':
        while_cond_children = list(graph.successors(node))
        return while_cond_children[-1]
    
    @staticmethod
    def get_assign_expr_target_val(graph: MDG, node: str) -> 'list[str]':
        assign_children = list(graph.successors(node))
        lhs = assign_children[0]
        rhs = assign_children[-1]
        
        return [lhs, rhs]
        
    @staticmethod
    def get_identifier_name(graph: MDG, node: str) -> str:
        label = NodeUtils.label_splitter(graph, node)
        # could receive a parameter
        aux = label[1].split(':')[0]
        l_aux = aux.split(' ')
        if len(l_aux) == 1:
            return aux

        return l_aux[1]
    
    @staticmethod
    def get_if_then(graph: MDG, node: str) -> str:
        if_children_children = list(graph.successors(node))
        then_blk = None
        for c in if_children_children:
            if NodeUtils.get_node_type(graph, c) == NodeType.BLOCK_STATEMENT:
                then_blk = c
        if not then_blk:
            return if_children_children[-1]
        
        return then_blk
    
    @staticmethod
    def get_if_condition(graph: MDG, node: str) -> str:
        if_children_children = list(graph.successors(node))
        condition_node = None
        comparators = {
            NodeType.OP_GREATER_THAN,
            NodeType.OP_GREATER_EQUALS_THAN,
            NodeType.OP_LESS_THAN,
            NodeType.OP_LESS_EQUALS_THAN,
            NodeType.OP_EQUALS,
            NodeType.OP_NOT_EQUALS,
            NodeType.OP_LOGICAL_AND,
            NodeType.OP_LOGICAL_OR,
            NodeType.OP_LOGICAL_NOT
        }
        for c in if_children_children:
            if NodeUtils.get_node_type(graph, c) in comparators:
                condition_node = c
        
        return condition_node

    @staticmethod
    def get_if_else(graph: MDG, node: str) -> str:
        if_children_children = list(graph.successors(node))
        else_node = None
        for c in if_children_children:
            if NodeUtils.get_node_type(graph, c) == NodeType.ELSE_STATEMENT:
                else_node = c
        
        return else_node
    
    @staticmethod
    def get_variable_init(graph: MDG, var: str) -> str:
        
        nodes = list(graph.nodes())
        var_name = None
        assignment = None
        for n in nodes:
            if NodeUtils.get_node_type(graph, n) == NodeType.OP_ASSIGNMENT:
                split_node = NodeUtils.label_splitter(graph, n)
                lhs = split_node[1].split(' = ')[0]
                print(lhs, var)
                if lhs == var:
                    _chidren = list(graph.successors(n))
                    var_name = _chidren[0]
                    assignment = _chidren[1]
                    break
                
        return var_name, assignment
    
    @staticmethod
    def identifier_collector(graph: MDG, root: str) -> 'list[str]':
        # Method that returns all identifiers in the tree
        children = nx.algorithms.traversal.bfs_tree(graph, root).nodes()
        identifiers = list(filter(lambda n: NodeUtils.get_node_type(graph, n) == NodeType.IDENTIFIER, children))
        
        return identifiers
                