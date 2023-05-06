class StructuralCondition:
    
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
            
    def evaluate(self):
        return vars(self)