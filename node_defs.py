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
    TABLEFUNC = 4
    VALUES = 5

class RestrictOp(Enum):
    LT = 1
    GT = 2
    EQ = 3

class CitusType(Enum):
    DISTRIBUTED = 1
    REFERENCE = 2

class Table:
    def __init__(self, name, citusType, distCol, maxCount, 
                 rowCount, nullRate, duplicateRate, columns, dupCount):
        self.name = name
        self.citusType = citusType
        self.distCol = distCol
        self.maxCount = maxCount
        self.rowCount =  rowCount
        self.nullRate =  nullRate
        self.duplicateRate =  duplicateRate
        self.columns = columns
        self.dupCount = dupCount

class Column:
    def __init__(self, name, type):
        self.name = name
        self.type = type
