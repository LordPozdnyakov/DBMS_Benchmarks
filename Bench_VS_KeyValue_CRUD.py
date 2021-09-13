#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# SEREVER-Modules
from BenchServerImpl import BenchServer_Valentina
from BenchRange import RangeForward, RangeBackward, RangeRandom


# **********************************************************************************************
class Bench_Valentina_KV_Example( BenchServer_Valentina ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)
    
    def SetUp(self):
        self.AddArtefact('Keys Count', self.ScalableValue)

        self.cursor.execute(self.cmd_CreateTable)

    def TearDown(self):
        self.cursor.execute(self.cmd_DropTable)

    def StoreKeys(self):
        for i in self.Range(0, self.ScalableValue):
            self.cursor.execute(self.cmd_Insert, [self.key(i), i] )

    def ReadKeys(self):
        for i in self.Range(0, self.ScalableValue):
            self.cursor.execute(self.cmd_Get, [self.key(i)] )
            val = self.cursor.fetchone()
            val = val[1]
    
    def UpdateKeys(self):
        for i in self.Range(0, self.ScalableValue):
            self.cursor.execute(self.cmd_Update, [self.key(i), i*2] )
    
    def DropKeys(self):
        for i in self.Range(0, self.ScalableValue):
            self.cursor.execute(self.cmd_Delete, [self.key(i)] )

    def BenchBody(self):
        self.TimeLog( 'Store', self.StoreKeys )
        # self.AddArtefact('Keys Count', len(self.db.keys()))
        self.TimeLog( 'Read', self.ReadKeys )
        self.TimeLog( 'Update', self.UpdateKeys )
        self.TimeLog( 'Drop', self.DropKeys )

    def key(self, i):
        return "key_" + str(i)

Bench_Valentina_KV_Example.cmd_CreateTable = 'CREATE KEYVALUE KV1;'
Bench_Valentina_KV_Example.cmd_DropTable = 'DROP KEYVALUE KV1;'
Bench_Valentina_KV_Example.cmd_Insert = 'KEYVALUE KV1 INSERT(:1 : :2);'
Bench_Valentina_KV_Example.cmd_Get = 'KEYVALUE KV1 GET(:1);'
Bench_Valentina_KV_Example.cmd_Update = 'KEYVALUE KV1 UPDATE(:1 : :2);'
Bench_Valentina_KV_Example.cmd_Delete = 'KEYVALUE KV1 GET(:1);'



# **********************************************************************************************
def main():
    ##########
    # Valentina bench
    VS_Server_Addr = 'sa:sa@127.0.0.1/vdb_test_db'
    # VS_Server_Axe = [10, 100, 1000, 10000, 100000]
    VS_Server_Axe = [10000]
    VS_bench_KV = Bench_Valentina_KV_Example(VS_Server_Addr)
    VS_bench_KV.put_Scalable( VS_Server_Axe )
    
    # Forward
    VS_bench_KV.put_Range(RangeForward)
    VS_bench_KV.Run()
    
    # Backward
    VS_bench_KV.put_Range(RangeBackward)
    # VS_bench_KV.Run()
    
    # Random
    VS_bench_KV.put_Range(RangeRandom)
    # VS_bench_KV.Run()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************