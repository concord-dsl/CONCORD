import logging
import operator, os

from conditions.CodeCondition import CodeCondition
from conditions.StructuralCondition import StructuralCondition
from server.queries import concord_query_builder
from tasks.ExecutionGraph import EXECUTION_GRAPH
from utils.statements import delete_statements, filter_statements

class Task:
    
    def __init__(self, *args, **kwargs):
        for attr, val in kwargs.items():
            setattr(self, attr, val)

    
    def evaluate_files(self, joern_client, output_path):
        logging.info(f'[{self.__class__.__name__.upper()}] Evaluating {self.name}: File Level Operations')
        # Grab Node Deletion operations
        deletion_ops = list(filter(lambda op: op.operation_type == 'remove', self.operations))
        if len(deletion_ops) == 0:
            logging.info(f'[{self.__class__.__name__.upper()}] No File Level Operations for {self.name}, skipping...')
            return False
        for delete_op in deletion_ops:
            statements_name = delete_op.graph_element_type
            logging.info(f'[{self.__class__.__name__.upper()}] Extracting {statements_name} statements')
            scala_script = os.path.abspath(EXECUTION_GRAPH["node"]["remove"][statements_name])
            joern_query = concord_query_builder(scala_script, output=output_path)
            result = joern_client.execute(joern_query)
            if not len(result['stdout']):
                logging.error(f'[{self.__class__.__name__.upper()}] Something went wrong when extracting {statements_name} statements')
                continue
        # Grab Code Conditions
        code_conditions = list(filter(lambda c: isinstance(c, CodeCondition), self.conditions))
        if len(code_conditions):
            logging.info(f'[{self.__class__.__name__.upper()}] Extracting Control Structure statements')
            code_blocks = list(map(lambda x: x.code_block, code_conditions))
            code_blocks_param = ','.join(code_blocks)
            scala_script = os.path.abspath(EXECUTION_GRAPH["node"]["extract"]["control"])
            joern_query = concord_query_builder(scala_script, csTypes=code_blocks_param, output=output_path)
            result = joern_client.execute(joern_query)
        # Perform the deletion
        logging.info(f'[{self.__class__.__name__.upper()}] Performing statement deletion')
        delete_statements(output_path)

        # Close CPG at joern level
        logging.info(f'[{self.__class__.__name__.upper()}] Persisting CPG at disk to save memory')
        query = "close(workspace.projectByCpg(cpg).map(_.name).get)"
        result = joern_client.execute(query)
        if not len(result['stdout']):
            logging.error(f'[{self.__class__.__name__.upper()}] Something went wrong persisting CPG')
        
        return True
        
        
            
    def evaluate(self, graph):
        logging.info(f'[{self.__class__.__name__.upper()}] Evaluating {self.name}: Graph Level Operations')
        graph_ops = list(filter(lambda op: op.operation_type != 'remove', self.operations))
        for graph_op in graph_ops:
            graph = graph_op.evaluate(graph)
        return graph
        