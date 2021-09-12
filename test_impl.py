#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules
from random import randint

# BENCH-Modules
from bench import Bench_Impl
from bench_server import BenchServer_Valentina
from bench_server import BenchServer_PostgreSql


# **********************************************************************************************
class Bench_Example( Bench_Impl ):
    def __init__(self):
        super().__init__()

        self.arr = list()
    
    def SetUp( self ):
        arr_size = self.ScalableValue
        self.AddArtefact('arr.size()', arr_size)

        for i in range(0, arr_size):
            x = randint(0, 1000)
            self.arr.append( x*x*x )

    def TearDown( self ):
        self.arr.clear()

    def BenchBody( self ):
        sorted(self.arr)


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
def main():
    ##########
    # Simple bench
    bench_axe = [1000, 10000, 100000]
    bench = Bench_Example()
    bench.put_Scalable( bench_axe )
    # bench.Run()

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


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************