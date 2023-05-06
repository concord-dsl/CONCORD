class CodeCondition:
    
    mapper = {
        "exclude": True,
        "include": False
    }
    
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
        
    
    def evaluate(self):
        # Convert the conditions to a dictionary.
        # CodeCoditions are basically filters: they dictate what parts of code should remain
        # intact and what parts shouldn't.
        return {self.code_block:self.mapper[self.action]}