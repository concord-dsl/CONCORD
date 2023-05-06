import networkx as nx
from utils.last_write_read.ExtraNodeProps import ExtraNodeProps
from utils.last_write_read.EdgeType import EdgeType
from utils.last_write_read.NodeUtils import NodeUtils


class LexicalNode:
    MDG = nx.MultiDiGraph
    def __init__(self, graph: MDG, general_node: str) -> None:
        self.graph = graph
        self.node = general_node
        self.variableLastOccurence: dict[str, dict[EdgeType, list[VariableSet]]] = {}
        
    def add_variable(self, iden_node: str):
        
        node: ExtraNodeProps = self.graph.nodes[iden_node]['ExtraNodeProps']
        hmap: dict[EdgeType, list[VariableSet]] = {}
        hmap['LAST_READ'] = LexicalNode.create_stack_of_variable_set(self.graph, iden_node)
        hmap['LAST_WRITE'] = LexicalNode.create_stack_of_variable_set(self.graph, iden_node)
        self.variableLastOccurence[node.get_identifier()] = hmap
        
    def add_parameter(self, parameter: str):
        self.add_variable(parameter)
        
    def has_variable(self, var_name: str):
        return NodeUtils.get_identifier_name(self.graph, var_name) in self.variableLastOccurence
    
    def set_and_update_variable_pointer(self, nx_node: str, link_type: str):
       
        name_node: ExtraNodeProps = self.graph.nodes[nx_node]['ExtraNodeProps']
        otherLinkTypeListMap: dict[str, list[VariableSet]] = self.variableLastOccurence.get(name_node.get_identifier())
        simpleNames: list[VariableSet] = otherLinkTypeListMap.get(link_type)
        variableSet: VariableSet = simpleNames[-1]
        for old_name in variableSet.get_simple_name_set():
            name_node.get_other_nodes().get(link_type).add(old_name)

        variableSet.replace(name_node)
       
    def set_variable_pointer(self, nx_node: str, link_type: str):
        
        name_node: ExtraNodeProps = self.graph.nodes[nx_node]['ExtraNodeProps']
        other_link_type_list_map: dict[EdgeType, list[VariableSet]] = self.variableLastOccurence.get(name_node.get_identifier())
        simple_names: list[VariableSet] = other_link_type_list_map.get(link_type)
        vset: VariableSet = simple_names[-1]
        for old_name_node in vset.get_simple_name_set():
            name_node.get_other_nodes().get(link_type).add(old_name_node)
                
    def stack_variable(self):
        for variable in self.variableLastOccurence.values():
            for stack in variable.values():
                stack.append(LexicalNode.create_variable_set(self.graph,stack[-1]))
                
    def shuffle_stack_variable(self):
        for variable in self.variableLastOccurence.values():
            for stack in variable.values():
                vset1 = stack.pop()
                vset2 = stack.pop()
                stack.append(vset1)
                stack.append(vset2)
    
    def destack_variable(self, close_loop: bool):
        for variable in self.variableLastOccurence.values():
            for k,v in variable.items():
                stack = v
                vset_pop = stack.pop()
                first_accessed = None
                if hasattr(vset_pop, 'first_name_node'):
                    first_accessed: ExtraNodeProps = self.graph.nodes[vset_pop.get_first_name_node()]['ExtraNodeProps']
                if close_loop and not first_accessed == None:
                    simple_names: list[ExtraNodeProps] = list(vset_pop.get_simple_name_set())
                    last_accessed: ExtraNodeProps = simple_names[-1]
                    first_accessed.get_other_nodes().get(k).add(last_accessed)
                for name_node in vset_pop.get_simple_name_set():
                    if len(stack) == 0:
                        raise ValueError("Not Expected.")
                    vset_peek = stack[-1]
                    vset_peek.add(name_node)
                    
    def get_node(self):
        return self.node
    
        
    @staticmethod
    def get_ordered_set():
        return set()
     
    @staticmethod
    def create_name_node_set(graph: MDG,nx_node: str) -> 'set[str]':
        if isinstance(nx_node, ExtraNodeProps):
            nx_node = nx_node.nx_node_id
        nameNode: ExtraNodeProps = graph.nodes[nx_node]['ExtraNodeProps']
        treeSet = LexicalNode.get_ordered_set()
        treeSet.add(nameNode)
        
        return treeSet
    
    @staticmethod
    def create_variable_set(graph: MDG, variableSet):
        if isinstance(variableSet, VariableSet):
            treeSet: set = LexicalNode.get_ordered_set()
            treeSet.update(variableSet.get_simple_name_set())
            return VariableSet(graph, treeSet)
        else:
            return VariableSet(graph, variableSet)

    @staticmethod
    def create_stack_of_variable_set(graph: MDG, iden_node: str):
        last_read_stack: list[VariableSet] = []
        
        node: ExtraNodeProps = graph.nodes[iden_node]['ExtraNodeProps']
        last_read_stack.append(LexicalNode.create_variable_set(graph, iden_node))
        return last_read_stack
    
class VariableSet:
    MDG = nx.MultiDiGraph
    # SimpleName = identifier
    def __init__(self, graph: MDG, simple_name):
        self.graph = graph
        if type(simple_name) is set:
             self.simple_name_set = simple_name
        if type(simple_name) == str:
            self.simple_name_set = LexicalNode.create_name_node_set(self.graph, simple_name)
        
        
        
    def replace(self, simple_name: str):
        if isinstance(simple_name,ExtraNodeProps):
            simple_name = simple_name.get_nx_id()
            
        if not hasattr(self, 'first_name_node'):
            self.first_name_node = simple_name
        
        self.simple_name_set = LexicalNode.create_name_node_set(self.graph, simple_name)
        
    def add(self, simple_name) -> bool:
        l = len(self.simple_name_set)
        self.simple_name_set.add(simple_name)
        return l == len(self.simple_name_set)
    
    def get_simple_name_set(self) -> 'list[ExtraNodeProps]':
        return self.simple_name_set
    
    def get_first_name_node(self) -> ExtraNodeProps:
        return self.first_name_node