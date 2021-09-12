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
def main():
    bench_axe = [1000, 10000, 100000]

    bench = Bench_Example()
    bench.put_Scalable( bench_axe )
    bench.Run()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************