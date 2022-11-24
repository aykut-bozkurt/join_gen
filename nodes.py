from config import *

import random

# grammar syntax
# 
# ======Assumptions======
# 1. Targetlist is firstable.*
# 2. Tables has common dist col
# 3. WHERE clause consists of 1 restriction e.g. WHERE dist1 (< | > | =) Const
#
# TODO: RTE_FUNCTION, RTE_TABLEFUNC, RTE_VALUES, SEMIJOIN, ANTIJOIN, ORDER BY, LIMIT 
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
#   RestrictList
#   Restrict
#   CteRte
#   CteList
#   Cte
#
# ===Terminals===
#   e 'SELECT' 'FROM' 'INNER JOIN' 'LEFT JOIN' 'RIGHT JOIN' 'FULL JOIN' 'WHERE' '*' ',' ';'
#
# ===Rules===
# Start -> Query ';' || 'WITH' CteList Query ';'
# Query -> SelectExpr FromExpr
# SelectExpr -> 'SELECT' '*'
# FromExpr -> 'FROM' (Rte JoinList JoinOp Rte Using || RteList) ['WHERE' 'nextRandomAlias()' '.' DistColName ('<' || '>' || '=') Int]
# JoinList ->  JoinOp Rte Using JoinList || e
# Using -> 'USING' '(' DistColName ')'
# RteList -> Rte [, RteList] || Rte
# Rte -> SubqueryRte 'AS' 'nextRandomAlias()' || RelationRte 'AS' 'nextRandomAlias()' || CteRte
# SubqueryRte -> '(' Query ')'
# RelationRte -> 'nextRandomTableName()'
# CteRte -> 'nextRandomCteName()'
# CteList -> Cte [',' CteList] || Cte
# Cte -> 'nextRandomAlias()' 'AS' '(' Query ')'
# JoinOp -> 'INNER JOIN' || 'LEFT JOIN' || 'RIGHT JOIN' || 'FULL JOIN'
# DistColName -> 'hardwired(get from config)'

def nextRandomRte():
    tables = getTargetTables()
    return ' ' + random.choice(tables) + ' '

def nextRandomRteType():
    rtes = getTargetRteTypes()
    return random.choice(rtes)

def nextRandomJoinOp():
    # 'INNER JOIN' || 'LEFT JOIN' || 'RIGHT JOIN' || 'FULL JOIN'
    joinTypes = getTargetJoinTypes()
    return ' ' + random.choice(joinTypes).name + ' JOIN'

def nextRandomRestrictOp():
    restrictOps = getTargetRestrictOps()
    return ' ' + random.choice(restrictOps) + ' '

# each level's last table is used in WHERE clause for the level
_aliasStack = []

# we should not refer cte inside cte
_insideCte = False

_totalRteCount = 0
_currentRteCount = 0
def curAlias():
    global _totalRteCount
    return ' table_' + str(_totalRteCount) + ' '

_currentCteCount = 0
_currentCteRteCount = 0
def curCteAlias():
    global _currentCteCount
    return ' cte_' + str(_currentCteCount) + ' '

def nextRandomCteName():
    global _currentCteCount
    randCteRef = random.randint(0, _currentCteCount-1)
    return ' cte_' + str(randCteRef)

def hasAnyCte():
    return _currentCteCount > 0

def canGenerateNewRte():
    return _currentRteCount < getTargetRteCount()

def canGenerateNewCte():
    return _currentCteCount < getTargetCteCount()

def canGenerateNewRteInsideCte():
    return _currentCteRteCount < getTargetCteRteCount()

def getQuery():
    # Query ';' || 'WITH' CteList Query ';'
    global _insideCte
    query = ''
    if random.randint(0,1):
        query += genQuery()
    else:
        _insideCte = True
        query += ' WITH '
        query += genCteList()
        _insideCte = False
        query += genQuery()
    query += ';'
    return query

def genQuery():
    # SelectExpr FromExpr
    query = ''
    query += genSelectExpr()
    query += genFromExpr()
    return query

def genSelectExpr():
    # 'SELECT' 'nextRandomAlias()'
    query = ''
    query += ' SELECT ' + curAlias().strip() + '.* '
    return query

def genFromExpr():
    # 'FROM' (Rte JoinList JoinOp Rte Using || RteList) ['WHERE' 'nextRandomAlias()' '.' DistColName ('<' || '>' || '=') Int]
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

    alias = _aliasStack.pop()
    if random.randint(0,1):
        query += ' WHERE '
        query += alias + '.' + getDistCol()
        query += nextRandomRestrictOp()
        query += str(random.randint(-1000, 1000))
    return query

def genCteList():
    # Cte [',' CteList] || Cte
    query = ''

    if random.randint(0,1):
        query += genCte()
        if not canGenerateNewCte():
            return query
        query += ','
        query += genCteList()
    else:
        query += genCte()
    return query

def genCte():
    # 'nextRandomAlias()' 'AS' '(' Query ')'
    global _currentCteCount
    query = ''
    query += curCteAlias().strip()
    _currentCteCount += 1
    query += ' AS '
    query += ' ( '
    query += genQuery()
    query += ' ) '
    return query

def genRteList():
    # RteList -> Rte [, RteList] || Rte
    global _insideCte
    query = ''
    if random.randint(0,1):
        query += genRte()
        if not canGenerateNewRte():
            return query
        if _insideCte and not canGenerateNewRteInsideCte():
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
        if _insideCte and not canGenerateNewRteInsideCte():
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
    # SubqueryRte as 'nextRandomAlias()' || RelationRte as 'nextRandomAlias()' || CteRte
    global _currentRteCount, _currentCteRteCount, _totalRteCount
    alias = curAlias().strip()
    if _insideCte:
        _currentCteRteCount += 1
    else:
        _currentRteCount += 1
    _totalRteCount += 1
    
    # donot dive into recursive subquery further if we hit into rte limit, replace it with relation rte
    rteType = nextRandomRteType()
    if not canGenerateNewRte():
        rteType = RTEType.RELATION

    # donot dive into recursive subquery further if we hit into rte in cte limit, replace it with relation rte
    if _insideCte and not canGenerateNewRteInsideCte():
        rteType = RTEType.RELATION

    # we cannot refer to cte if we are inside it or we donot have any cte
    if (_insideCte or not hasAnyCte()) and rteType == RTEType.CTE:
        rteType = RTEType.RELATION

    query = ''
    if rteType == RTEType.SUBQUERY:
        query += genSubqueryRte()
    elif rteType == RTEType.RELATION:
        query += genRelationRte()
    elif rteType == RTEType.CTE:
        query += genCteRte()
    else:
        raise BaseException("unknown RTE type")

    query += ' AS '
    query += alias
    _aliasStack.append(alias)
        
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

def genCteRte():
    # 'nextRandomCteName()'
    query = ''
    query += nextRandomCteName()
    return query
