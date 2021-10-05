#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# SEREVER-Modules
from BenchServerImpl_Valentina import BenchServer_Valentina
from BenchRange import RangeForward, RangeBackward, RangeRandom


# **********************************************************************************************
class Bench_Valentina_KV_CRUD( BenchServer_Valentina ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)
    
    def SetUp(self):
        self.AddArtefact('Keys Count', self.ScalableValue)

        self.cursor.execute(self.cmd_DropTable)
        self.cursor.execute(self.cmd_CreateTable)

        self.insert_stmt = self.cursor.prepare( self.cmd_Insert )
        self.update_stmt = self.cursor.prepare( self.cmd_Update )
        self.get_stmt    = self.cursor.prepare( self.cmd_Get )
        self.delete_stmt = self.cursor.prepare( self.cmd_Delete )

    def TearDown(self):
        self.cursor.execute(self.cmd_DropTable)

    def InsertKeys(self):
        for i in self.Range(0, self.ScalableValue):
            # self.cursor.execute(self.cmd_Insert, [self.key(i), i] )
            self.insert_stmt( self.key(i), i )

    def UpdateKeys(self):
        for i in self.Range(0, self.ScalableValue):
            # self.cursor.execute(self.cmd_Update, [self.key(i), i*2] )
            self.update_stmt( self.key(i), i )

    def GetKeys(self):
        for i in self.Range(0, self.ScalableValue):
            # self.cursor.execute(self.cmd_Get, [self.key(i)] )
            self.get_stmt( self.key(i) )
            val = self.cursor.fetchone()
            val = val[1]
    
    def DeleteKeys(self):
        for i in self.Range(0, self.ScalableValue):
            # self.cursor.execute(self.cmd_Delete, [self.key(i)] )
            self.delete_stmt( self.key(i) )

    def BenchBody(self):
        self.TimeLog( 'Insert', self.InsertKeys )
        self.TimeLog( 'Update', self.UpdateKeys )
        self.TimeLog( 'Get',    self.GetKeys )
        self.TimeLog( 'Delete', self.DeleteKeys )

    def key(self, i):
        return "key_" + str(i)

Bench_Valentina_KV_CRUD.cmd_CreateTable = 'CREATE KEYVALUE KV1;'
Bench_Valentina_KV_CRUD.cmd_DropTable = 'DROP KEYVALUE IF EXISTS KV1;'

Bench_Valentina_KV_CRUD.cmd_Insert = 'KEYVALUE KV1 INSERT(:1 : :2);'
Bench_Valentina_KV_CRUD.cmd_Get = 'KEYVALUE KV1 GET(:1);'
Bench_Valentina_KV_CRUD.cmd_Update = 'KEYVALUE KV1 UPDATE(:1 : :2);'
Bench_Valentina_KV_CRUD.cmd_Delete = 'KEYVALUE KV1 DELETE(:1);'



# **********************************************************************************************
def main():
    ##########
    # Valentina bench
    # VS_Server_Addr = 'sa:sa@127.0.0.1/vdb_test_db'
    VS_Server_Addr = '/home/lord/bench/Bench_VS_Insert.vdb'
    # VS_Server_Axe = [10, 100, 1000, 10000, 100000]
    VS_Server_Axe = [100000]
    VS_bench_KV = Bench_Valentina_KV_CRUD(VS_Server_Addr)
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