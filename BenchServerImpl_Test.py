#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# BENCH-Modules
from BenchServerImpl_Valentina import BenchServer_Valentina
from BenchServerImpl_Postgresql import BenchServer_PostgreSql
from BenchServerImpl_Redis import BenchServer_Redis


# **********************************************************************************************
class Bench_Valentina_Example( BenchServer_Valentina ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)
    
    def SetUp(self):
        self.AddArtefact('Insert Count', self.ScalableValue)

        self.cursor.execute(self.cmd_CreateTable)

    def TearDown(self):
        self.cursor.execute(self.cmd_DropTable)

    def BenchBody(self):
        for i in range(0, self.ScalableValue):
            self.cursor.execute( self.cmd_Insert, [i] )
            # self.cursor.execute( 'INSERT INTO T1 VALUES (' + str(i) + ');' )

Bench_Valentina_Example.cmd_CreateTable = 'CREATE TABLE T1( fld_val LONG );'
Bench_Valentina_Example.cmd_DropTable = 'DROP TABLE T1;'
Bench_Valentina_Example.cmd_Insert = 'INSERT INTO T1 VALUES (:1);'


# **********************************************************************************************
class Bench_Psql_Example( BenchServer_PostgreSql ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)

    def SetUp(self):
        self.AddArtefact('Insert Count', self.ScalableValue)

        self.db.execute(self.cmd_CreateTable)
        self.insert_cmd = self.db.prepare( self.cmd_Insert )

    def TearDown(self):
        self.db.execute(self.cmd_DropTable)

    def BenchBody(self):
        self.db.execute( 'BEGIN TRANSACTION;' )
        
        for i in range(0, self.ScalableValue):
            self.insert_cmd(i)

        self.db.execute( 'COMMIT TRANSACTION;' )

Bench_Psql_Example.cmd_CreateTable = 'CREATE TABLE T1( fld_val INTEGER );'
Bench_Psql_Example.cmd_DropTable = 'DROP TABLE T1;'
Bench_Psql_Example.cmd_Insert = 'INSERT INTO T1 VALUES ($1);'


# **********************************************************************************************
class Bench_Redis_Example( BenchServer_Redis ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)
    
    def SetUp(self):
        self.AddArtefact('Insert Count', self.ScalableValue)

    def TearDown(self):
        keys = self.db.keys()
        for key in keys:
            self.db.delete(key)

    def StoreKeys(self):
        for i in range(0, self.ScalableValue):
            self.db.set( "key_"+str(i), i )

    def ReadKeys(self):
        for i in range(0, self.ScalableValue):
            val = self.db.get( "key_"+str(i) )
            val = int(val)

    def BenchBody(self):
        self.TimeLog( 'Store', self.StoreKeys )
        self.AddArtefact('Keys Count', len(self.db.keys()))
        self.TimeLog( 'Read', self.ReadKeys )


# **********************************************************************************************
class Bench_Valentina_KV_Example( BenchServer_Valentina ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)
    
    def SetUp(self):
        self.AddArtefact('Keys Count', self.ScalableValue)

        self.cursor.execute(self.cmd_CreateTable)

    def TearDown(self):
        for i in range(0, self.ScalableValue):
            self.cursor.execute(self.cmd_Delete, ["key_"+str(i)] )
        self.cursor.execute(self.cmd_DropTable)

    def StoreKeys(self):
        for i in range(0, self.ScalableValue):
            self.cursor.execute(self.cmd_Insert, ["key_"+str(i), i] )

    def ReadKeys(self):
        for i in range(0, self.ScalableValue):
            self.cursor.execute(self.cmd_Get, ["key_"+str(i)] )
            val = self.cursor.fetchone()
            val = val[1]

    def BenchBody(self):
        self.TimeLog( 'Store', self.StoreKeys )
        # self.AddArtefact('Keys Count', len(self.db.keys()))
        self.TimeLog( 'Read', self.ReadKeys )

Bench_Valentina_KV_Example.cmd_CreateTable = 'CREATE KEYVALUE KV1;'
Bench_Valentina_KV_Example.cmd_DropTable = 'DROP KEYVALUE KV1;'
Bench_Valentina_KV_Example.cmd_Insert = 'KEYVALUE KV1 INSERT(:1 : :2);'
Bench_Valentina_KV_Example.cmd_Get = 'KEYVALUE KV1 GET(:1);'
Bench_Valentina_KV_Example.cmd_Delete = 'KEYVALUE KV1 GET(:1);'


# **********************************************************************************************
def main():
    ##########
    # Valentina bench
    VS_Server_Addr = 'sa:sa@127.0.0.1/vdb_test_db'
    VS_Server_Axe = [10, 100, 1000, 10000, 100000]
    VS_bench = Bench_Valentina_Example(VS_Server_Addr)
    VS_bench.put_Scalable( VS_Server_Axe )
    # VS_bench.Run()

    ##########
    # PostgreSql bench
    PS_Server_Addr = 'pq://postgres:pass_post@localhost:5432/psql_test_db'
    PS_Server_Axe = [10, 100, 1000, 10000, 100000]
    PS_bench = Bench_Psql_Example(PS_Server_Addr)
    PS_bench.put_Scalable( PS_Server_Axe )
    # PS_bench.Run()

    ##########
    # Redis bench
    Redis_Server_Addr = 'localhost:6379:0'
    Redis_Server_Axe = [10, 100, 1000, 10000, 100000]
    Redis_bench = Bench_Redis_Example(Redis_Server_Addr)
    Redis_bench.put_Scalable( Redis_Server_Axe )
    # Redis_bench.Run()

    ##########
    # Valentina bench
    VS_Server_Addr = 'sa:sa@127.0.0.1/vdb_test_db'
    VS_Server_Axe = [10, 100, 1000, 10000, 100000]
    # VS_Server_Axe = [10, 100, 1000, 10000]
    VS_bench = Bench_Valentina_KV_Example(VS_Server_Addr)
    VS_bench.put_Scalable( VS_Server_Axe )
    # VS_bench.Run()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************