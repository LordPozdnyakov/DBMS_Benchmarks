#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules

# SEREVER-Modules
from BenchServerImpl_Valentina import BenchServer_Valentina

import valentina


# **********************************************************************************************
class Bench_ValentinaLocal_No_Stmt( BenchServer_Valentina ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)

    def EngineInit(self):
        # self.connection = valentina.create(self.ServerAddr)
        self.connection = valentina.connect(self.ServerAddr)
        self.cursor = self.connection.cursor()
    
    def SetUp(self):
        self.AddArtefact('Record Count', self.ScalableValue)

        self.cursor.execute(self.cmd_DropTable)
        self.cursor.execute(self.cmd_CreateTable)

    def TearDown(self):
        self.cursor.execute(self.cmd_DropTable)
        # pass

    def InsertRecords(self):
        for i in self.Range(0, self.ScalableValue):
            self.cursor.execute( self.cmd_Insert, [i+1, i+2, i+3, i+4, i+5, i+6, i+7, i+8, i+9, i+10] )

    def BenchBody(self):
        self.TimeLog( 'Insert', self.InsertRecords )

# Bench_ValentinaLocal_No_Stmt.cmd_CreateTable = 'CREATE TABLE T2( fld_val LONG, fld_key LONG INDEXED);'
Bench_ValentinaLocal_No_Stmt.cmd_DropTable = 'DROP TABLE IF EXISTS T2;'
Bench_ValentinaLocal_No_Stmt.cmd_CreateTable = """
CREATE TABLE T2(
    fld_1 LONG,
    fld_2 LONG,
    fld_3 LONG,
    fld_4 LONG,
    fld_5 LONG,
    fld_6 LONG,
    fld_7 LONG,
    fld_8 LONG,
    fld_9 LONG,
    fld_10 LONG
);"""


Bench_ValentinaLocal_No_Stmt.cmd_Insert = """
INSERT INTO T2 VALUES (
    :1, :2, :3, :4, :5, :6, :7, :8, :9, :10
);"""


# **********************************************************************************************
class Bench_ValentinaLocal_With_Stmt( Bench_ValentinaLocal_No_Stmt ):
    def __init__(self, inServerAddres):
        super().__init__(inServerAddres)
    
    def SetUp(self):
        self.AddArtefact('Record Count', self.ScalableValue)

        self.cursor.execute(self.cmd_DropTable)
        self.cursor.execute(self.cmd_CreateTable)
        self.insert_stmt = self.cursor.prepare(self.cmd_Insert) 

    def InsertRecords(self):
        for i in self.Range(0, self.ScalableValue):
            self.insert_stmt( i+1, i+2, i+3, i+4, i+5, i+6, i+7, i+8, i+9, i+10 )


# **********************************************************************************************
def main():
    
    ##########
    # Prepare params
    # VS_Addr = 'test.vdb?ram=true'
    # VS_Addr = '/home/lord/bench/Bench_VS_Insert.vdb'
    VS_Addr = 'sa:sa@127.0.0.1/vdb_test_db'
    # VS_Bench_Axe = [1000, 10000, 100000]
    VS_Bench_Axe = [100000]
    
    ##########
    # Stmt NOT USED
    Bench_No_Stmt = Bench_ValentinaLocal_No_Stmt(VS_Addr)
    Bench_No_Stmt.put_Scalable( VS_Bench_Axe )
    Bench_No_Stmt.Run()
    
    ##########
    # Stmt USED
    Bench_Use_Stmt = Bench_ValentinaLocal_With_Stmt(VS_Addr)
    Bench_Use_Stmt.put_Scalable( VS_Bench_Axe )
    Bench_Use_Stmt.Run()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************