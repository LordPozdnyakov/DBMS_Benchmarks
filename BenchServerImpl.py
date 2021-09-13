#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# BENCH-Modules
from BenchImpl import BenchImpl

# SEREVER-Modules
import postgresql
import valentina
from redis import Redis


# **********************************************************************************************
class BenchServerImpl( BenchImpl ):
    def __init__(self):
        super().__init__()
    
    def EngineInit(self):
        pass
    def EngineShutdown( self ):
        pass

    def Run( self ):
        self.EngineInit()

        BenchImpl.Run(self)

        self.EngineShutdown()


# **********************************************************************************************
class BenchServer_Valentina( BenchServerImpl ):
    def __init__(self, inServerAddres):
        super().__init__()
        self.ServerAddr = inServerAddres

    def EngineInit(self):
        self.connection = valentina.connect(self.ServerAddr)
        self.cursor = self.connection.cursor()

    def EngineShutdown( self ):
        self.cursor.close()
        self.connection.close()


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