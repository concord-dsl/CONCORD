from enum import Enum

class NodeType(Enum):
    METHOD_DECLARATION = 1
    BLOCK_STATEMENT = 2
    FOR_STATEMENT = 3
    LOCAL_DECLARATION = 4
    IDENTIFIER = 5
    IF_STATEMENT = 6
    WHILE_STATEMENT = 7
    METHOD_RETURN = 8
    PARAMETER = 9
    OP_ASSIGNMENT = 10
    OP_LESS_THAN = 11
    OP_GREATER_THAN = 12
    OP_GREATER_EQUALS_THAN = 13
    OP_LESS_EQUALS_THAN = 14
    OP_EQUALS = 15
    OP_POST_DECREMENT = 16
    OP_POST_INCREMENT = 17
    OP_PRE_DECREMENT = 18
    OP_PRE_INCREMENT = 19
    OP_AND = 20
    OP_ELVIS = 21
    OP_ADDRR_OF = 22
    OP_INSTANCE_OF = 23
    OP_INDIR_FIELD_ACC = 24
    OP_NOT = 25
    OP_SIZE_OF = 26
    OPS_ASSIGN_MOD = 27
    OP_FIELD_ACC = 28
    OP_MULT = 29
    OP_SUB = 30
    OP_ADD = 31
    OP_XOR = 32
    OP_FORMATTED_VAL = 33
    OP_PTR_SHIFT = 34
    OP_RANGE = 35
    OP_ARITH_SHIFT_RIGHT = 36
    OP_ASSIGN_MINUS = 37
    OP_LOGICAL_OR = 38
    OPS_ASSIGN_EXP = 39
    OP_CAST = 40
    OP_IS = 41
    OPS_ASSIGN_AND = 42
    OPS_ASSIGN_LOGICAL_SHIFT_RIGHT = 43
    OP_ARRAY_INITALIZE = 44
    OP_IN = 45
    OP_GET_ELT_PTR = 46
    OP_ASSIGN_DIV = 47
    OP_MINUS = 48
    OP_LOGICAL_SHIFT_RIGHT = 49
    OP_LOGICAL_AND = 50
    OP_LOGICAL_NOT = 51
    OP_FORMAT_STR = 52
    OP_NOT_EQUALS = 53
    OP_ASSIGN_PLUS = 54
    OP_EXP = 55
    OP_NOT_IN = 56
    OP_PLUS = 57
    OP_INDIRECTED_COMPUTED_MEMBER_ACCESS = 58
    OP_INDIRECTION = 59
    OP_DELETE = 60
    OP_IDX_ACCESS = 61
    OP_INDIRECT_MEMBER_ACCESS = 62
    OP_MOD = 63
    OPS_ASSIGN_OR = 64
    OP_MEMBER_ACCESS = 65
    OP_CONDITIONAL = 66
    OP_OR = 67
    OP_COMPUTED_MEMBER_ACCESS = 68
    OP_DIV = 69
    OP_SHIFT_LEFT = 70
    OP_COMPARE = 71
    OP_LENGTH_OF = 72
    OPS_ASSIGN_ARITH_SHIFT_RIGHT = 73
    OP_INDIRECT_INDEX_ACCESS = 74
    OPS_ASSIGN_XOR = 75
    OP_NOT_NULL_ASSERT = 76
    OP_SAFE_NAVIGATION = 77
    OPS_ASSIGN_SHIFT_LEFT = 78
    OP_ASSIGN_MUL = 79
    OP_IS_NOT = 80
    LITERAL = 81
    ELSE_STATEMENT = 82
    RETURN_STATEMENT = 83
    TRY_STATEMENT = 84
    FIELD_IDENTIFIER = 85
    METHOD_CALL = 86
    UNKNOWN = 99
    
    