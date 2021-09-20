#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# BENCH-Modules
from BenchServerImpl import BenchServerImpl

# SEREVER-Modules
import postgresql


# **********************************************************************************************
class BenchServer_PostgreSql( BenchServerImpl ):
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