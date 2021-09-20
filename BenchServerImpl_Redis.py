#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# BENCH-Modules
from BenchServerImpl import BenchServerImpl

# SEREVER-Modules
from redis import Redis


# **********************************************************************************************
class BenchServer_Redis( BenchServerImpl ):
    def __init__(self, inServerAddres):
        super().__init__()
        self.ServerAddr = inServerAddres
    
    def EngineInit(self):
        adr = self.ServerAddr.split(':')
        self.db = Redis(adr[0], adr[1], adr[2])

    def EngineShutdown( self ):
        self.db.close()


# **********************************************************************************************
def main():
    pass


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************