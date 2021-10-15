#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# BENCH-Modules
from BenchTools.BenchImpl import BenchImpl

# SEREVER-Modules
import valentina


# **********************************************************************************************
class Bench_Valentina( BenchImpl ):
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
class Bench_ValentinaCreate( BenchImpl ):
    def __init__(self, inDbAddres, inIsRam=False, inIsRemoveAfter=False):
        super().__init__()

        self.DbAddres = inDbAddres + '?ram=' + str(inIsRam).lower()
        self.DbName = inDbAddres.split('/')[-1]

        self.isRam = inIsRam
        self.isRemoveAfter = inIsRemoveAfter

    def EngineInit(self):
        self.connection = valentina.create(self.DbAddres)
        self.cursor = self.connection.cursor()
    
    def EngineShutdown( self ):
        if(self.isRemoveAfter):
            self.cursor.execute('DROP DATABASE IF EXISTS ' + self.DbName )

        self.cursor.close()
        self.connection.close()


# **********************************************************************************************
def main():
    pass


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************