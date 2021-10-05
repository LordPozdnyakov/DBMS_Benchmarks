#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# SEREVER-Modules
from BenchTools.BenchImpl_PostgreSql import Bench_PostgreSql
from BenchTools.BenchRange import RangeForward, RangeBackward, RangeRandom


# **********************************************************************************************
class Bench_Psql_Example( Bench_PostgreSql ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)

    def SetUp(self):
        self.AddArtefact('Insert Count', self.ScalableValue)

        self.db.execute('DROP TABLE IF EXISTS T1')
        self.db.execute(self.cmd_CreateTable)
        self.db.execute(self.cmd_CreateIndex)
        self.insert_cmd = self.db.prepare( self.cmd_Insert )
        self.update_cmd = self.db.prepare( self.cmd_Update )
        self.delete_cmd = self.db.prepare( self.cmd_Delete )
        self.select_cmd = self.db.prepare( self.cmd_Select )

    def TearDown(self):
        self.db.execute(self.cmd_DropTable)

    def InsertRecords(self):
        self.db.execute( 'BEGIN TRANSACTION;' )
        for i in self.Range(0, self.ScalableValue):
            self.insert_cmd(i, i)
        self.db.execute( 'COMMIT TRANSACTION;' )

    def UpdateRecords(self):
        self.db.execute( 'BEGIN TRANSACTION;' )
        for i in self.Range(0, self.ScalableValue):
            self.update_cmd(i+i, i)
        self.db.execute( 'COMMIT TRANSACTION;' )

    def DropRecords(self):
        self.db.execute( 'BEGIN TRANSACTION;' )
        for i in self.Range(0, self.ScalableValue):
            self.delete_cmd(i)
        self.db.execute( 'COMMIT TRANSACTION;' )
    
    def SelectRecords(self):
        self.db.execute( 'BEGIN TRANSACTION;' )
        for i in self.Range(0, self.ScalableValue):
            self.select_cmd(i)
        self.db.execute( 'COMMIT TRANSACTION;' )

    def BenchBody(self):
        self.TimeLog( 'Insert', self.InsertRecords )
        self.TimeLog( 'Select', self.SelectRecords )
        self.TimeLog( 'Update', self.UpdateRecords )
        self.TimeLog( 'Drop', self.DropRecords )

Bench_Psql_Example.cmd_CreateTable = 'CREATE TABLE T1( fld_val INTEGER, fld_key INTEGER);'
Bench_Psql_Example.cmd_CreateIndex = 'CREATE INDEX T1_index1 ON T1 (fld_key);'

Bench_Psql_Example.cmd_DropTable = 'DROP TABLE T1;'

Bench_Psql_Example.cmd_Insert = 'INSERT INTO T1 VALUES ($1, $2);'
Bench_Psql_Example.cmd_Update = 'UPDATE T1 SET fld_val = $1 WHERE fld_key = $2 ;'
Bench_Psql_Example.cmd_Delete = 'DELETE FROM T1 WHERE fld_key = $1 ;'
Bench_Psql_Example.cmd_Select = 'SELECT fld_val FROM T1 WHERE fld_key = $1 ;'


# **********************************************************************************************
def main():
    ##########
    # PostgreSql bench
    PS_Server_Addr = 'pq://postgres:pass_post@localhost:5432/psql_test_db'
    # PS_Server_Axe = [10, 100, 1000, 10000, 100000]
    PS_Server_Axe = [1000]
    PS_bench = Bench_Psql_Example(PS_Server_Addr)
    PS_bench.put_Scalable( PS_Server_Axe )

    # Forward
    PS_bench.put_Range(RangeForward)
    PS_bench.Run()
    
    # Backward
    PS_bench.put_Range(RangeBackward)
    # PS_bench.Run()
    
    # Random
    PS_bench.put_Range(RangeRandom)
    # PS_bench.Run()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************