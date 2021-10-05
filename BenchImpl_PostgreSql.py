#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# BENCH-Modules
from BenchImpl import BenchImpl

# SEREVER-Modules
import postgresql


# **********************************************************************************************
class Bench_PostgreSql( BenchImpl ):
    def __init__(self, inServerAddres):
        super().__init__()
        self.ServerAddr = inServerAddres

    def EngineInit(self):
        self.db = postgresql.open(self.ServerAddr)

    def EngineShutdown( self ):
        pass


# **********************************************************************************************
def main():
    pass


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************