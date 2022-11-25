from node_defs import *
from config.config import *

def tableDDLs():
    ddls = ''
    tables = getConfig().targetTables
    for table in tables:
        ddls += _tableDDL(table)
        ddls += '\n'
    return ddls

def _tableDDL(table):
    ddl = ''
    ddl += 'CREATE TABLE ' + table.name + '('

    for column in table.columns[:-1]:
        ddl += _columnDDL(column)
        ddl += ',\n'
    if len(table.columns) > 0:
        ddl += _columnDDL(table.columns[-1])

    ddl += ');\n'
    
    if table.citusType == CitusType.DISTRIBUTED:
        ddl += 'SELECT create_distributed_table(' + '\'' + table.name + '\',\'' + table.distCol + '\'' + ');'
    else:
        ddl += 'SELECT create_reference_table(' + '\'' + table.name + '\'' + ');'
    ddl += '\n'
    return ddl
        
def _columnDDL(column):
    ddl = ''
    ddl += column.name
    ddl += ' '
    ddl += column.type
    return ddl
