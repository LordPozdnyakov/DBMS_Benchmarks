#!/usr/bin/python3


# **********************************************************************************************
#BOX-Modules
from time import time

#BOX-Modules
from BenchRange import RangeForward


# **********************************************************************************************
class Bench_Interface:
    def Run( self ):
        pass
    def SetUp( self ):
        pass
    def TearDown( self ):
        pass
    def BenchBody( self ):
        pass

    def AddSystemArtefacts(self):
        pass
    def AddArtefact( self, inName, inValue ):
        pass
    def PrintArtefacts( self ):
        pass
    def put_BenchName( self, inBenchName ):
        pass

    def TimeLog( self, inName, inCallable ):
        pass

    def put_Scalable( self, inValueList ):
        pass


# **********************************************************************************************
class BenchImpl( Bench_Interface ):
    def __init__(self):
        super().__init__()

        self.artefact = dict()
        self.ValueList = [0]
        self.Range = RangeForward
        self.BenchName = type(self).__name__
        self.art_type = 'Before:'

    def TimeLog( self, inName, inCallable ):
        Time = time()
        inCallable()
        Time = time() - Time
        self.AddArtefact( inName, Time )

    def AddSystemArtefacts(self):
        self.AddArtefact( 'BenchName', self.BenchName )
        self.AddArtefact( 'RangeType', self.Range.__name__ )

    def Run( self ):
        for val in self.ValueList:
            self.ScalableValue = val

            self.art_type = 'System:'
            self.AddSystemArtefacts()

            self.art_type = 'Before:'
            self.TimeLog( 'SetUp', self.SetUp )

            self.art_type = 'Inner:'
            self.TimeLog( 'BenchTime', self.BenchBody )

            self.art_type = 'After:'
            self.TimeLog( 'TearDown', self.TearDown )

            self.PrintArtefacts()
            self.artefact.clear()
            print()
    
    def AddArtefact( self, inName, inValue ):
        self.artefact[self.art_type.ljust(8)+inName] = inValue # TODO: Make it beautiful

    def PrintArtefacts( self ):
        artefacts = [ (key, self.artefact[key]) for key in self.artefact ]
        for key, val in artefacts:
            if( isinstance(val, float) ):
                print( 'Artefact:', key.ljust(20), "{:.3f}".format(round(val,3)) )
            else:
                print( 'Artefact:', key.ljust(20), val )

    def put_BenchName( self, inBenchName ):
        self.BenchName = inBenchName

    def put_Scalable( self, inValueList ):
        self.ValueList = inValueList
    
    def put_Range( self, inBenchRange ):
        self.Range = inBenchRange


# **********************************************************************************************
def main():
    pass


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************