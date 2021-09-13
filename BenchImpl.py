#!/usr/bin/python3


# **********************************************************************************************
#BOX-Modules
from time import time


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

    def AddArtefact( self, inName, inValue ):
        pass
    def PrintArtefacts( self ):
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
        self.ValueList = list()

    def TimeLog( self, inName, inCallable ):
        Time = time()
        inCallable()
        Time = time() - Time
        self.AddArtefact( inName, Time )

    def Run( self ):
        if(not self.ValueList):
            self.ValueList.append(0)

        for val in self.ValueList:
            self.ScalableValue = val

            self.art_type = 'Before:'
            self.TimeLog( 'SetUp', self.SetUp )

            self.art_type = 'Inner:'
            self.TimeLog( 'BenchTime', self.BenchBody )

            self.art_type = 'After:'
            self.TimeLog( 'TearDown', self.TearDown )

            self.PrintArtefacts()
            print()
    
    def AddArtefact( self, inName, inValue ):
        self.artefact[self.art_type.ljust(8)+inName] = inValue # TODO: Make it beautiful

    def PrintArtefacts( self ):
        artefacts = [ (key, self.artefact[key]) for key in self.artefact ]
        for key, val in artefacts:
            print( 'Artefact:', key.ljust(20), val )

    def put_Scalable( self, inValueList ):
        self.ValueList = inValueList


# **********************************************************************************************
def main():
    pass


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************