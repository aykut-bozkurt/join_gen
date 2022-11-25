from join_gen import *
from ddl_gen import *

import signal
import sys

def _signal_handler(sig, frame):
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, _signal_handler)

    resetConfig()

    ddls = tableDDLs()
    print(ddls)

    while True:
        res = input('Press x to exit or Enter to generate more')
        if res.lower() == 'x':
            print('Exit from query generation mode!')
            sys.exit(0)

        query = newQuery()
        print(query)

        resetConfig()
