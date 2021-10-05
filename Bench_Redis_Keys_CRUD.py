#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# SERVER-Modules
from BenchImpl_Redis import Bench_Redis
from BenchRange import RangeForward, RangeBackward, RangeRandom


# **********************************************************************************************
class Bench_Redis_Keys_CRUD( Bench_Redis ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)
    
    def SetUp(self):
        self.AddArtefact('Insert Count', self.ScalableValue)

    def TearDown(self):
        keys = self.db.keys()
        for key in keys:
            self.db.delete(key)

    def StoreKeys(self):
        for i in self.Range(0, self.ScalableValue):
            self.db.set( self.key(i), i )

    def ReadKeys(self):
        for i in self.Range(0, self.ScalableValue):
            val = self.db.get( self.key(i) )
            val = int(val)
    
    def UpdateKeys(self):
        for i in self.Range(0, self.ScalableValue):
            self.db.set( self.key(i), i*2 )
    
    def DropKeys(self):
        for i in self.Range(0, self.ScalableValue):
            self.db.delete( self.key(i) )

    def BenchBody(self):
        # db_backup = self.db
        # self.db = self.db.pipeline()

        self.TimeLog( 'Store', self.StoreKeys )
        self.AddArtefact('Keys Count', len(self.db.keys()))
        self.TimeLog( 'Read', self.ReadKeys )
        self.TimeLog( 'Update', self.UpdateKeys )
        self.TimeLog( 'Drop', self.DropKeys )

        # self.TimeLog('pipe', self.db.execute)
        # self.db = db_backup
    
    def key(self, i):
        return "key_" + str(i)


# **********************************************************************************************
def main():
    ##########
    # Redis bench
    Redis_Server_Addr = 'localhost:6379:0'
    # Redis_Server_Axe = [10, 100, 1000, 10000, 100000]
    Redis_Server_Axe = [10000]
    Redis_bench = Bench_Redis_Keys_CRUD(Redis_Server_Addr)
    Redis_bench.put_Scalable( Redis_Server_Axe )

    # Forward
    Redis_bench.put_Range(RangeForward)
    Redis_bench.Run()
    # Backward

    Redis_bench.put_Range(RangeBackward)
    # Redis_bench.Run()
    
    # Random
    Redis_bench.put_Range(RangeRandom)
    # Redis_bench.Run()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************