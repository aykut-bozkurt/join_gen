from enum import Enum

class JoinType(Enum):
    INNER = 1
    LEFT = 2
    RIGHT = 3
    FULL = 4

class RTEType(Enum):
    RELATION = 1
    SUBQUERY = 2

_target_join_types = [JoinType.INNER, JoinType.LEFT, JoinType.RIGHT, JoinType.FULL] 
_target_rte_types = [RTEType.RELATION, RTEType.SUBQUERY] 
_target_tables = ['ref1', 'dist1']
_target_dist_col = 'id'
_target_rte_count = 5

def getDistCol():
    return _target_dist_col

def getTargetRteTypes():
    return _target_rte_types

def getTargetJoinTypes():
    return _target_join_types

def getTargetTables():
    return _target_tables

def getTargetRteCount():
    return _target_rte_count
