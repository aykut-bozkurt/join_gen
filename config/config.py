from node_defs import *
from config.config_parser import *

import random
import yaml

class Config:
    def __init__(self):
        configObj = Config.parseConfigFile('config/config.yaml')

        self.targetTables = parseTableArray(configObj['targetTables'])
        self.targetJoinTypes = parseJoinTypeArray(configObj['targetJoinTypes'])
        self.targetRteTypes = parseRteTypeArray(configObj['targetRteTypes'])
        self.targetRestrictOps = parseRestrictOpArray(configObj['targetRestrictOps'])
        self.targetCol = configObj['targetCol']
        self.targetRteCount = configObj['targetRteCount']
        self.targetCteCount = configObj['targetCteCount']
        self.targetCteRteCount = configObj['targetCteRteCount']
        #print(self)

    def __repr__(self):
        rep = "targetRteCount: {}\n".format(self.targetRteCount)
        rep += "targetCteCount: {}\n".format(self.targetCteCount)
        rep += "targetCteRteCount: {}\n".format(self.targetCteRteCount)

        rep += "targetRteTypes:\n"
        for rteType in self.targetRteTypes:
            rep += "\t{}\n".format(rteType)

        rep += "targetJoinTypes:\n"
        for joinType in self.targetJoinTypes:
            rep += "\t{}\n".format(joinType)

        rep += "restrictOps:\n"
        for restrictOp in self.targetRestrictOps:
            rep += "\t{}\n".format(restrictOp)

        return rep

    @staticmethod
    def parseConfigFile(path):
        try:
            with open(path, 'r') as configFile:
                return yaml.load(configFile, yaml.Loader)
        except:
            raise BaseException('cannot parse config.yaml')

_config = None
def resetConfig():
    global _config
    _config = Config()

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
    restrictOp = random.choice(restrictOps)
    opText = ''
    if restrictOp == RestrictOp.EQ:
        opText = '='
    elif restrictOp == RestrictOp.LT:
        opText = '<'
    elif restrictOp == RestrictOp.GT:
        opText = '>'
    else:
        raise BaseException('Unknown restrict op')

    return ' ' + opText + ' '
