#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules
from random import randint

# BENCH-Modules
from bench import Bench_Impl
from bench_server import BenchServer_Valentina


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
        self.AddArtefact('repeatCount', self.ScalableValue)

    def BenchBody(self):
        for i in range(0, self.ScalableValue):
            self.cursor.execute( self.cmdGetBenchList )
            for bench in self.cursor.fetchall():
                x = bench[1]

Bench_Valentina_Example.cmdGetBenchList = """
        SELECT tblBenches.RecID, tblBenches.fldBench
        FROM tblBenches;
        """

# **********************************************************************************************
def main():
    ##########
    # Simple bench
    bench_axe = [1000, 10000, 100000]
    bench = Bench_Example()
    bench.put_Scalable( bench_axe )
    bench.Run()

    ##########
    # Valentina bench
    VS_Server_Addr = 'sa:sa@127.0.0.1/vdb_bench_results_debug'
    VS_Server_Axe = [10, 100, 1000, 10000]
    VS_bench = Bench_Valentina_Example(VS_Server_Addr)
    VS_bench.put_Scalable( VS_Server_Axe )
    VS_bench.Run()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************