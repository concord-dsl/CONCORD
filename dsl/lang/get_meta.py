import os

from textx import metamodel_from_file

from main.Main import Main
from representations.Representation import Representation
from tasks.Operation import Operation
from tasks.Task import Task
from conditions.CodeCondition import CodeCondition
from conditions.StructuralCondition import StructuralCondition

def get_meta_model():
    _classes = (Main ,Representation, Task, Operation, CodeCondition, StructuralCondition)
    _spec_path = os.path.join(os.getcwd(), 'lang' ,'lang.tx')
    metamodel = metamodel_from_file(_spec_path, classes=_classes)
    
    return metamodel