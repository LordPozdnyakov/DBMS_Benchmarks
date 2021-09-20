#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# BENCH-Modules
from BenchImpl import BenchImpl


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
def main():
    pass


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************