from typing import Any
from utils.last_write_read.EdgeType import EdgeType


class ExtraNodeProps:
    
    def __init__(self, identifier: str, nx_node_id: str) -> None:
        self.other_nodes: dict[EdgeType, set[Any]] = {et:set() for et in {'LAST_READ', 'LAST_WRITE'}} # Works because we care about LAST_WRITE and LAST_READ only, not AST edges.
        self.identifier = identifier
        self.nx_node_id = nx_node_id
        
    def get_other_nodes(self) -> 'dict[EdgeType, set[Any]]':
        return self.other_nodes
    
    def get_identifier(self) -> str:
        return self.identifier
    
    def get_nx_id(self) -> str:
        return self.nx_node_id