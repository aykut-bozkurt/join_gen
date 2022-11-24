from config import *

import random

# grammar syntax
# 
# ======Assumptions======
# 1. Targetlist is firstable.*
# 2. Tables has common dist col
# 3. No WHERE clause
#
# ====SYNTAX====
# ===Nonterminals===
#   Query
#   SelectExpr
#   FromExpr
#   FromWithJoin
#   RteList
#   Rte
#   SubqueryRte
#   RelationRte
#   JoinList
#   JoinOp
#   Using
#
# ===Terminals===
#   e 'SELECT' 'FROM' 'INNER JOIN' 'LEFT JOIN' 'RIGHT JOIN' 'FULL JOIN' '*' ',' ';'
#
# ===Rules===
# Start -> Query ';'
# Query -> SelectExpr FromExpr
# SelectExpr -> 'SELECT' '*'
# FromExpr -> 'FROM' (Rte JoinList JoinOp Rte Using || RteList)
# JoinList ->  JoinOp Rte Using JoinList || e
# Using -> 'USING' '(' DistColName ')'
# RteList -> Rte [, RteList] || Rte
# Rte -> SubqueryRte as 'nextRandomAlias()' || RelationRte as 'nextRandomAlias()'
# SubqueryRte -> '(' Query ')'
# RelationRte -> 'nextRandomTableName()'
# JoinOp -> 'INNER JOIN' || 'LEFT JOIN' || 'RIGHT JOIN' || 'FULL JOIN'
# DistColName -> 'hardwired(get from config)'
#

def nextRandomRte():
    tables = getTargetTables()
    return ' ' + random.choice(tables) + ' '

def nextRandomRteType():
    rtes = getTargetRteTypes()
    return random.choice(rtes)

def nextRandomJoinOp():
    # 'INNER JOIN' || 'LEFT JOIN' || 'RIGHT JOIN' || 'FULL JOIN'
    joinTypes = getTargetJoinTypes()
    return random.choice(joinTypes).name + ' JOIN'

_current_rte_count = 0
def curAlias():
    global _current_rte_count
    return ' table_' + str(_current_rte_count) + ' '

def canGenerateNewRte():
    # we are guaranteed to generate 2 more rtes when we call here
    return _current_rte_count < getTargetRteCount()

def getQuery():
    query = genQuery()
    query += ';'
    return query

def genQuery():
    # SelectExpr FromExpr
    query = ''
    query += genSelectExpr()
    query += genFromExpr()
    return query

def genSelectExpr():
    # 'SELECT' '*'
    query = ''
    query += ' SELECT ' + curAlias().strip() + '.* '
    return query

def genFromExpr():
    # 'FROM' Rte Rte JoinList JoinOp Rte Using
    query = ''
    query += ' FROM '

    if random.randint(0,1):
        query += genRte()
        query += genJoinList()
        query += nextRandomJoinOp()
        query += genRte()
        query += genUsing()
    else:
        query += genRteList()
    return query

def genRteList():
    # RteList -> Rte [, RteList] || Rte
    query = ''
    if random.randint(0,1):
        query += genRte()
        if not canGenerateNewRte():
            return query
        query += ','
        query += genRteList()
    else:
        query += genRte()
    return query

def genJoinList():
    # JoinOp Rte Using JoinList || e
    query = ''

    if random.randint(0,1):
        if not canGenerateNewRte():
            return query
        query += nextRandomJoinOp()
        query += genRte()
        query += genUsing()
        query += genJoinList()
    return query

def genUsing():
    # 'USING' '(' DistColName ')'
    query = ''
    query += ' USING (' + getDistCol() + ' ) '
    return query

def genRte():
    # SubqueryRte as 'nextRandomAlias()' || RelationRte as 'nextRandomAlias()'
    global _current_rte_count 
    alias = curAlias()
    _current_rte_count += 1
    
    # donot dive into recursive subquery further if we hit into rte limit, replace it with relation rte
    rteType = nextRandomRteType()
    if not canGenerateNewRte():
        rteType = RTEType.RELATION

    query = ''
    if rteType == RTEType.SUBQUERY:
        query += genSubqueryRte()
    elif rteType == RTEType.RELATION:
        query += genRelationRte()
    else:
        raise BaseException("unknown RTE type")

    query += ' AS '
    query += alias
        
    return query

def genSubqueryRte():
    # '(' Query ')'
    query = ''
    query += ' ( '
    query += genQuery()
    query += ' ) '
    return query

def genRelationRte():
    # 'nextRandomTableName()'
    query = ''
    query += nextRandomRte()
    return query
