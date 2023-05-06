from tasks.EdgeOperations.AddOperations import AddOperations
from tasks.NodeOperations.RemoveOperations import RemoveOperations


EXECUTION_GRAPH = {
    "edge": {
        "add": {
            'next_token': AddOperations.next_token,
            'next_sibling': AddOperations.next_sibling,
            'for_cfg': AddOperations.for_exec,
            'while_cfg': AddOperations.while_exec,
            'guarded_by': AddOperations.guarded_by,
            'computed_from': AddOperations.computed_from,
            'last_read_write': AddOperations.last_read_write,
            'last_lexical_use': AddOperations.last_lexical_use,
            'returns_to': AddOperations.returns_to
            },
        "remove": {}
        },
    "node": {
        "add": {},
        "remove": {
            # Path to Scala scripts that implement the logic of extracting statements
            'print': 'joern/scripts/get-print-statements.sc',
            'simple_assignment': 'joern/scripts/get-simple-assignments.sc',
            'logging': RemoveOperations.logging_statements,
            'sys_exit': RemoveOperations.sys_exit_statements,
        },
        "extract": {
            "control": 'joern/scripts/get-constrol-structures.sc'
        }
    }
}