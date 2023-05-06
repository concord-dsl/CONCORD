import logging
from tasks.ExecutionGraph import EXECUTION_GRAPH

OP_TYPE_PRIORITY = {
    'remove': 1,
    'add': 0
    # In the future, "edit" could be added.
}

class Operation:
    
    def __init__(self, *args, **kwargs):
        for attr, val in kwargs.items():
            setattr(self, attr, val)
        # Add priority to each operation:
        # Remove : 1
        # Add : 0
        # where the higher value refers to higher priority. This is important because wrong order of execution
        # can lead to wrong results. For instance if we define two ops: add next_token (edges) and remove simple_assigment
        # and execute the addition first and then the removal, the final result will be incorrect, in other words, we may find
        # tokens not linked by next_token.
        self.priority = OP_TYPE_PRIORITY[self.operation_type.lower()]
                    
    def evaluate(self, graph):
        ge, ot, get = (self.graph_element.lower(), self.operation_type.lower(), self.graph_element_type.lower())
        if not get in EXECUTION_GRAPH[ge][ot]:
            logging.warn(f'[{self.__class__.__name__.upper()}] Unsupported, skipping.')
        else:
            graph = EXECUTION_GRAPH[ge][ot][get](graph)
        
        return graph