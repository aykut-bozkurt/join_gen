from nodes import *
from config import *
from ddl_gen import *

import signal
import sys

def signal_handler(sig, frame):
    sys.exit(0)

def prepareForNewQuery():
    resetConfig()
    resetGeneratorContext()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    prepareForNewQuery()
    ddls = tableDDLs(getTargetTables())
    print(ddls)

    while True:
        res = input('Press x to exit or Enter to generate more')
        if res.lower() == 'x':
            print('Exit from query generation mode!')
            sys.exit(0)

        query = getQuery()
        print(query)

        prepareForNewQuery()
