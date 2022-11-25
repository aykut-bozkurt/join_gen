from config.config import *
from node_defs import *

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
# CteRte -> 'randomCteName()'
# CteList -> Cte [',' CteList] || Cte
# Cte -> 'nextRandomAlias()' 'AS' '(' Query ')'
# JoinOp -> 'INNER JOIN' || 'LEFT JOIN' || 'RIGHT JOIN' || 'FULL JOIN'
# DistColName -> 'hardwired(get from config)'

class GeneratorContext:
    '''context to store some variables which should be available during generation'''

    def __init__(self):
        # each level's last table is used in WHERE clause for the level
        self.aliasStack = []
        # tracks if we are inside cte as we should not refer cte inside cte
        self.insideCte = False
        # total rtes in cte + non-cte parts
        self.totalRteCount = 0
        # rte count in non-cte part to enforce non-cte rte limit
        self.currentRteCount = 0
        # cte count to enforce cte limit
        self.currentCteCount = 0
        # rte count in cte part to enforce rte limit in cte
        self.currentCteRteCount = 0

    def randomCteName(self):
        '''returns a randomly selected cte name'''
        randCteRef = random.randint(0, self.currentCteCount-1)
        return ' cte_' + str(randCteRef)

    def curAlias(self):
        '''returns current alias name to be used for the current table'''
        return ' table_' + str(self.totalRteCount)

    def curCteAlias(self):
        '''returns current alias name to be used for the current cte'''
        return ' cte_' + str(self.currentCteCount)

    def hasAnyCte(self):
        '''returns if context has any cte'''
        return self.currentCteCount > 0

    def canGenerateNewRte(self):
        '''checks if context exceeds allowed rte count'''
        return self.currentRteCount < getConfig().targetRteCount

    def canGenerateNewCte(self):
        '''checks if context exceeds allowed cte count'''
        return self.currentCteCount < getConfig().targetCteCount

    def canGenerateNewRteInsideCte(self):
        '''checks if context exceeds allowed rte count inside a cte'''
        return self.currentCteRteCount < getConfig().targetCteRteCount

    def addAlias(self, alias):
        self.aliasStack.append(alias)

    def removeLastAlias(self):
        return self.aliasStack.pop()

def newQuery():
    genCtx = GeneratorContext()
    return _start(genCtx)

def _start(genCtx):
    '''returns generated query'''
    # Query ';' || 'WITH' CteList Query ';'
    query = ''
    if random.randint(0,1):
        query += _genQuery(genCtx)
    else:
        genCtx.insideCte = True
        query += ' WITH '
        query += _genCteList(genCtx)
        genCtx.insideCte = False
        query += _genQuery(genCtx)
    query += ';'
    return query

def _genQuery(genCtx):
    # SelectExpr FromExpr
    query = ''
    query += _genSelectExpr(genCtx)
    query += _genFromExpr(genCtx)
    return query

def _genSelectExpr(genCtx):
    # 'SELECT' 'curAlias()'
    query = ''
    query += ' SELECT ' + genCtx.curAlias() + '.* '
    return query

def _genFromExpr(genCtx):
    # 'FROM' (Rte JoinList JoinOp Rte Using || RteList) ['WHERE' 'nextRandomAlias()' '.' DistColName ('<' || '>' || '=') Int]
    query = ''
    query += ' FROM '

    if random.randint(0,1):
        query += _genRte(genCtx)
        query += _genJoinList(genCtx)
        query += randomJoinOp()
        query += _genRte(genCtx)
        query += _genUsing(genCtx)
    else:
        query += _genRteList(genCtx)

    alias = genCtx.removeLastAlias()
    if random.randint(0,1):
        query += ' WHERE '
        query += alias + '.' + getConfig().targetCol
        query += randomRestrictOp()
        query += str(random.randint(-1000, 1000))
    return query

def _genCteList(genCtx):
    # Cte [',' CteList] || Cte
    query = ''

    if random.randint(0,1):
        query += _genCte(genCtx)
        if not genCtx.canGenerateNewCte():
            return query
        query += ','
        query += _genCteList(genCtx)
    else:
        query += _genCte(genCtx)
    return query

def _genCte(genCtx):
    # 'nextRandomAlias()' 'AS' '(' Query ')'
    query = ''
    query += genCtx.curCteAlias()
    genCtx.currentCteCount += 1
    query += ' AS '
    query += ' ( '
    query += _genQuery(genCtx)
    query += ' ) '
    return query

def _genRteList(genCtx):
    # RteList -> Rte [, RteList] || Rte
    query = ''
    if random.randint(0,1):
        query += _genRte(genCtx)
        if not genCtx.canGenerateNewRte():
            return query
        if genCtx.insideCte and not genCtx.canGenerateNewRteInsideCte():
            return query
        query += ','
        query += _genRteList(genCtx)
    else:
        query += _genRte(genCtx)
    return query

def _genJoinList(genCtx):
    # JoinOp Rte Using JoinList || e
    query = ''

    if random.randint(0,1):
        if not genCtx.canGenerateNewRte():
            return query
        if genCtx.insideCte and not genCtx.canGenerateNewRteInsideCte():
            return query
        query += randomJoinOp()
        query += _genRte(genCtx)
        query += _genUsing(genCtx)
        query += _genJoinList(genCtx)
    return query

def _genUsing(genCtx):
    # 'USING' '(' DistColName ')'
    query = ''
    query += ' USING (' + getConfig().targetCol + ' ) '
    return query

def _genRte(genCtx):
    # SubqueryRte as 'nextRandomAlias()' || RelationRte as 'curAlias()' || CteRte
    alias = genCtx.curAlias()
    if genCtx.insideCte:
        genCtx.currentCteRteCount += 1
    else:
        genCtx.currentRteCount += 1
    genCtx.totalRteCount += 1
    
    # donot dive into recursive subquery further if we hit into rte limit, replace it with relation rte
    rteType = randomRteType()
    if not genCtx.canGenerateNewRte():
        rteType = RTEType.RELATION

    # donot dive into recursive subquery further if we hit into rte in cte limit, replace it with relation rte
    if genCtx.insideCte and not genCtx.canGenerateNewRteInsideCte():
        rteType = RTEType.RELATION

    # we cannot refer to cte if we are inside it or we donot have any cte
    if (genCtx.insideCte or not genCtx.hasAnyCte()) and rteType == RTEType.CTE:
        rteType = RTEType.RELATION

    query = ''
    if rteType == RTEType.SUBQUERY:
        query += _genSubqueryRte(genCtx)
    elif rteType == RTEType.RELATION:
        query += _genRelationRte(genCtx)
    elif rteType == RTEType.CTE:
        query += _genCteRte(genCtx)
    else:
        raise BaseException("unknown RTE type")

    query += ' AS '
    query += alias
    genCtx.addAlias(alias)
        
    return query

def _genSubqueryRte(genCtx):
    # '(' Query ')'
    query = ''
    query += ' ( '
    query += _genQuery(genCtx)
    query += ' ) '
    return query

def _genRelationRte(genCtx):
    # 'randomAvailableTableName()'
    query = ''
    query += randomAvailableTableName()
    return query

def _genCteRte(genCtx):
    # 'randomCteName()'
    query = ''
    query += genCtx.randomCteName()
    return query
