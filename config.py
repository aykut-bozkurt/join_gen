from node_defs import *

import random

def createTargetTables():
    col = Column('id', ValueType.INT)
    distTable = Table('dist', CitusType.DISTRIBUTED, col, [col], None, None)
    refTable = Table('ref', CitusType.REFERENCE, None, [col], None, None)
    return [distTable, refTable], col

class Config:
    def __init__(self):
        self.targetJoinTypes = []
        self.targetRteTypes = []
        self.targetRestrictOps = []
        self.targetTables = []
        self.targetCol = None
        self.targetRteCount = 0
        self.targetCteCount = 0
        self.targetCteRteCount = 0

_config = None
def resetConfig():
    global _config
    config = Config()
    config.targetJoinTypes = [JoinType.INNER, JoinType.LEFT, JoinType.RIGHT, JoinType.FULL] 
    config.targetRteTypes = [RTEType.RELATION, RTEType.SUBQUERY, RTEType.CTE]
    config.targetRestrictOps = ['<','>','=']
    config.targetTables, config.targetCol = createTargetTables()
    config.targetRteCount = 5
    config.targetCteCount = 2
    config.targetCteRteCount = 3
    _config = config

def getConfig():
    return _config

def randomAvailableTableName():
    '''returns a randomly selected table name from target tables given at config'''
    tables = getConfig().targetTables
    return ' ' + random.choice(tables).name + ' '

def randomRteType():
    '''returns a randomly selected RteType given at config'''
    rtes = getConfig().targetRteTypes
    return random.choice(rtes)

def randomJoinOp():
    '''returns a randomly selected JoinOp given at config'''
    joinTypes = getConfig().targetJoinTypes
    return ' ' + random.choice(joinTypes).name + ' JOIN'

def randomRestrictOp():
    '''returns a randomly selected RestrictOp given at config'''
    restrictOps = getConfig().targetRestrictOps
    return ' ' + random.choice(restrictOps) + ' '
