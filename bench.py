#!/usr/bin/python3


# **********************************************************************************************
#BOX-Modules
from time import time


# **********************************************************************************************
class Bench_Interface:
    def hello( self ):
        pass

    def Run( self ):
        pass
    def SetUp( self ):
        pass
    def TearDown( self ):
        pass
    def BenchBody( self ):
        pass

    def AddArtefact( self, inName, inValue ):
        pass
    def PrintArtefacts( self ):
        pass


# **********************************************************************************************
class Bench_Impl( Bench_Interface ):
    def __init__(self):
        super().__init__()

        self.arttfact = dict()

    def Run( self ):
        self.art_type = 'Before:\t'
        SetTime = time()
        self.SetUp()
        SetTime = time() - SetTime
        self.AddArtefact( 'SetUp', SetTime )

        self.art_type = 'Inner:\t'
        BenchTime = time()
        self.BenchBody()
        BenchTime = time() - BenchTime
        self.AddArtefact( 'BenchTime', BenchTime )

        self.art_type = 'After:\t'
        TearTime = time()
        self.TearDown()
        TearTime = time() - TearTime
        self.AddArtefact( 'TearDown', TearTime )

        self.PrintArtefacts()
    
    def AddArtefact( self, inName, inValue ):
        self.arttfact[self.art_type+inName] = inValue

    def PrintArtefacts( self ):
        artefacts = [ (key, self.arttfact[key]) for key in self.arttfact ]
        for key, val in artefacts:
            print( 'Artefact:', key, '\t:', val )


# **********************************************************************************************
def main():
    pass


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************