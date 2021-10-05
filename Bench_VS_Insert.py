#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# SEREVER-Modules
from BenchImpl_ValentinaServer import Bench_ValentinaServer
from BenchRange import RangeForward, RangeBackward, RangeRandom


# **********************************************************************************************
class Bench_Valentina_Record_CRUD( Bench_ValentinaServer ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)
    
    def SetUp(self):
        self.AddArtefact('Record Count', self.ScalableValue)

        self.cursor.execute(self.cmd_DropTable)
        self.cursor.execute(self.cmd_CreateTable)

        self.insert_stmt = self.cursor.prepare(self.cmd_Insert) 
        self.update_stmt = self.cursor.prepare(self.cmd_Update) 
        self.select_stmt = self.cursor.prepare(self.cmd_Select) 
        self.delete_stmt = self.cursor.prepare(self.cmd_Delete) 

    def TearDown(self):
        self.cursor.execute(self.cmd_DropTable)

    def InsertRecords(self):
        for i in self.Range(0, self.ScalableValue):
            self.insert_stmt( i, i )

    def UpdateRecords(self):
        for i in self.Range(0, self.ScalableValue):
            self.update_stmt( i+i, i )

    def SelectRecords(self):
        for i in self.Range(0, self.ScalableValue):
            self.select_stmt( i )
    
    def DeleteRecords(self):
        for i in self.Range(0, self.ScalableValue):
            self.delete_stmt( i )

    def BenchBody(self):
        self.TimeLog( 'Insert', self.InsertRecords )
        self.TimeLog( 'Update', self.UpdateRecords )
        self.TimeLog( 'Select', self.SelectRecords )
        self.TimeLog( 'Delete', self.DeleteRecords )

Bench_Valentina_Record_CRUD.cmd_CreateTable = 'CREATE TABLE T1( fld_val LONG, fld_key LONG INDEXED);'
Bench_Valentina_Record_CRUD.cmd_DropTable = 'DROP TABLE IF EXISTS T1;'

Bench_Valentina_Record_CRUD.cmd_Insert = 'INSERT INTO T1 VALUES (:1, :2);'
Bench_Valentina_Record_CRUD.cmd_Update = 'UPDATE T1 SET fld_val = :1 WHERE fld_key = :2 ;'
Bench_Valentina_Record_CRUD.cmd_Delete = 'DELETE FROM T1 WHERE fld_key = :1 ;'
Bench_Valentina_Record_CRUD.cmd_Select = 'SELECT fld_val FROM T1 WHERE fld_key = :1 ;'


# **********************************************************************************************
def main():
    ##########
    # Valentina bench
    VS_Server_Addr = 'sa:sa@127.0.0.1/vdb_test_db'
    # VS_Server_Addr = '/home/lord/bench/Bench_VS_Insert.vdb'
    # VS_Server_Axe = [1000, 10000, 100000]
    VS_Server_Axe = [10000]
    VS_Bench = Bench_Valentina_Record_CRUD(VS_Server_Addr)
    VS_Bench.put_BenchName('VS_Record_CRUD') # optional
    VS_Bench.put_Scalable( VS_Server_Axe )

    # Forward
    VS_Bench.put_Range(RangeForward)
    VS_Bench.Run()
    
    # Backward
    VS_Bench.put_Range(RangeBackward)
    # VS_Bench.Run()
    
    # Random
    VS_Bench.put_Range(RangeRandom)
    # VS_Bench.Run()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************