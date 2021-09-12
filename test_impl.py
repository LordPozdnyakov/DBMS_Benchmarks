#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules
from random import randint

# BENCH-Modules
from bench import Bench_Impl


# **********************************************************************************************
class Bench_Example( Bench_Impl ):
    def __init__(self):
        super().__init__()

        self.arr = list()
    
    def SetUp( self ):
        arr_size = 100000
        self.AddArtefact('arr.size()', arr_size)

        for i in range(0, arr_size):
            self.arr.append( randint(0, i) )

    def TearDown( self ):
        self.arr.clear()

    def BenchBody( self ):
        sorted(self.arr)


# **********************************************************************************************
def main():
    bench = Bench_Example()
    bench.Run()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************