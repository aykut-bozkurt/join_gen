from config.config import *

def getTableData():
    tables = getConfig().targetTables
    dataGenerationSql = ''
    for table in tables:
        # generate unique rows
        targetNullRows = int(table.rowCount * table.nullRate)
        targetNotNullRows = table.rowCount - targetNullRows
        dataGenerationSql += _genData(table.name, 0, targetNotNullRows)
        dataGenerationSql += '\n'

        # generate null rows
        dataGenerationSql += _genData(table.name, 0, targetNullRows, isNull=True)
        dataGenerationSql += '\n'

        # generate duplicate rows
        targetDuplicateRows = int(targetNotNullRows * table.duplicateRate)
        dataGenerationSql += _genData(table.name, 0, targetDuplicateRows)
        dataGenerationSql += '\n\n'
    return dataGenerationSql

def _genData(tableName, fromVal, toVal, isNull=False):
    '''returns string to fill table with the series of integers inside given range'''
    dataGenerationSql = ''
    dataGenerationSql += 'INSERT INTO ' + tableName
    dataGenerationSql += ' SELECT ' + ('NULL' if isNull else 'i') + ' FROM generate_series(' + str(fromVal) + ',' + str(toVal) + ') i;'
    return dataGenerationSql
