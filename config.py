from enum import Enum

class JoinType(Enum):
    INNER = 1
    LEFT = 2
    RIGHT = 3
    FULL = 4

class RTEType(Enum):
    RELATION = 1
    SUBQUERY = 2
    CTE = 3

class ValueType(Enum):
    INT = 1
    TEXT = 2

class CitusType(Enum):
    DISTRIBUTED = 1
    REFERENCE = 2

class Pkey:
    def __init__(self):
        self.table = None
        self.column = None

class Fkey:
    def __init__(self):
        self.referencingTable = None
        self.referencingColumn = None
        self.referencedTable = None
        self.referencedColumn = None

class Table:
    def __init__(self, name, citusType, distCol, columns, pkey, fkeys):
        self.name = name
        self.citusType = citusType
        self.distCol = distCol
        self.columns = columns
        self.pkey = pkey
        self.fkeys = fkeys

class Column:
    def __init__(self, name, type):
        self.name = name
        self.type = type

def createTargetTables():
    col = Column('id', ValueType.INT)
    distTable = Table('dist', CitusType.DISTRIBUTED, col, [col], None, None)
    refTable = Table('ref', CitusType.REFERENCE, None, [col], None, None)
    return [distTable, refTable], col

class Config:
    targetJoinTypes = []
    targetRteTypes = []
    targetRestrictOps = []
    targetTables = []
    targetCol = None
    targetRteCount = 0
    targetCteCount = 0
    targetCteRteCount = 0

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

def getDistCol():
    return _config.targetCol.name

def getTargetRteTypes():
    return _config.targetRteTypes

def getTargetJoinTypes():
    return _config.targetJoinTypes

def getTargetRestrictOps():
    return _config.targetRestrictOps

def getTargetTables():
    return _config.targetTables

def getTargetRteCount():
    return _config.targetRteCount

def getTargetCteCount():
    return _config.targetCteCount

def getTargetCteRteCount():
    return _config.targetCteRteCount
