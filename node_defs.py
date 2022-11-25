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
