#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# BENCH-Modules
from BenchServerImpl import BenchServerImpl

# SEREVER-Modules
import valentina


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
def main():
    pass


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************