#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# SEREVER-Modules
from BenchServerImpl import BenchServer_Valentina
from BenchRange import RangeForward, RangeBackward, RangeRandom


# **********************************************************************************************
class Bench_Valentina_Record_CRUD( BenchServer_Valentina ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)
    
    def SetUp(self):
        self.AddArtefact('Insert Count', self.ScalableValue)

        self.cursor.execute('DROP TABLE IF EXISTS T1')
        self.cursor.execute(self.cmd_CreateTable)

    def TearDown(self):
        self.cursor.execute(self.cmd_DropTable)

    def InsertRecords(self):
        for i in self.Range(0, self.ScalableValue):
            self.cursor.execute( self.cmd_Insert, [i, i] )
            # self.cursor.execute( 'INSERT INTO T1 VALUES (' + str(i) + ');' )

    def UpdateRecords(self):
        for i in self.Range(0, self.ScalableValue):
            self.cursor.execute( self.cmd_Update, [i+i, i] )

    def DropRecords(self):
        for i in self.Range(0, self.ScalableValue):
            self.cursor.execute( self.cmd_Delete, [i] )
    
    def SelectRecords(self):
        for i in self.Range(0, self.ScalableValue):
            self.cursor.execute( self.cmd_Select, [i] )

    def BenchBody(self):
        self.TimeLog( 'Insert', self.InsertRecords )
        # self.AddArtefact('Keys Count', len(self.db.keys()))
        self.TimeLog( 'Select', self.SelectRecords )
        self.TimeLog( 'Update', self.UpdateRecords )
        self.TimeLog( 'Drop', self.DropRecords )

Bench_Valentina_Record_CRUD.cmd_CreateTable = 'CREATE TABLE T1( fld_val LONG, fld_key LONG INDEXED);'
Bench_Valentina_Record_CRUD.cmd_DropTable = 'DROP TABLE T1;'
Bench_Valentina_Record_CRUD.cmd_Insert = 'INSERT INTO T1 VALUES (:1, :2);'
Bench_Valentina_Record_CRUD.cmd_Update = 'UPDATE T1 SET fld_val = :1 WHERE fld_key = :2 ;'
Bench_Valentina_Record_CRUD.cmd_Delete = 'DELETE FROM T1 WHERE fld_key = :1 ;'
Bench_Valentina_Record_CRUD.cmd_Select = 'SELECT fld_val FROM T1 WHERE fld_key = :1 ;'


# **********************************************************************************************
def main():
    ##########
    # Valentina bench
    VS_Server_Addr = 'sa:sa@127.0.0.1/vdb_test_db'
    # VS_Server_Axe = [10, 100, 1000, 10000, 100000]
    VS_Server_Axe = [100000]
    VS_Bench = Bench_Valentina_Record_CRUD(VS_Server_Addr)
    VS_Bench.put_Scalable( VS_Server_Axe )

    # Forward
    VS_Bench.put_Range(RangeForward)
    VS_Bench.Run()
    
    # Backward
    VS_Bench.put_Range(RangeBackward)
    VS_Bench.Run()
    
    # Random
    VS_Bench.put_Range(RangeRandom)
    VS_Bench.Run()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************