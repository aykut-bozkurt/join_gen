from config.config import *

def getTableData():
    dataGenerationSql = ''

    (fromVal, toVal) = getConfig().dataRange
    tables = getConfig().targetTables
    for table in tables:
        # generate unique rows
        dataGenerationSql += _genData(table.name, fromVal, toVal, table.rowCount)
        dataGenerationSql += '\n'

        # generate null rows
        targetNullRows = int(table.rowCount * table.nullRate)
        dataGenerationSql += _genNullData(table.name, targetNullRows)
        dataGenerationSql += '\n'

        # generate duplicate rows
        targetDuplicateRows = int(table.rowCount * table.duplicateRate)
        dataGenerationSql += _genDupData(table.name, targetDuplicateRows)
        dataGenerationSql += '\n\n'
    return dataGenerationSql

def _genData(tableName, fromVal, toVal, rowCount):
    '''returns string to fill table with random integers inside given range'''
    dataGenerationSql = ''
    dataGenerationSql += 'INSERT INTO ' + tableName

    dataRange = toVal - fromVal
    randomData = '({0} + {1} * random())::int'.format(str(fromVal), str(dataRange))
    dataGenerationSql += ' SELECT ' + randomData + ' FROM generate_series(0,' + str(rowCount) + ') i;'
    return dataGenerationSql

def _genNullData(tableName, nullCount):
    '''returns string to fill table with NULLs'''
    dataGenerationSql = ''
    dataGenerationSql += 'INSERT INTO ' + tableName
    dataGenerationSql += ' SELECT NULL FROM generate_series(0,' + str(nullCount) + ') i;'
    return dataGenerationSql

def _genDupData(tableName, dupRowCount):
    '''returns string to fill table with duplicate integers which are fetched from given table'''
    dataGenerationSql = ''
    dataGenerationSql += 'INSERT INTO ' + tableName
    dataGenerationSql += ' SELECT * FROM ' + tableName + ' LIMIT ' + str(dupRowCount) + ';'
    return dataGenerationSql
