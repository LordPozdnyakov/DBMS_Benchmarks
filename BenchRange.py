#!/usr/bin/python3


# **********************************************************************************************
# BOX-Modules
from random import shuffle


# **********************************************************************************************

class RangeImpl:
	def __init__( self, start, stop ):
		self.start = start
		self.stop = stop

	def __iter__(self):
		return self

	def __next__(self):
		pass


# **********************************************************************************************
class RangeForward( RangeImpl ):
	def __init__( self, start, stop ):
		super().__init__(start, stop)
		self.current = start-1

	def __next__(self):
		self.current += 1
		if self.current < self.stop:
			return self.current
		raise StopIteration


# **********************************************************************************************
class RangeBackward( RangeImpl ):
	def __init__( self, start, stop ):
		super().__init__(start, stop)
		self.current = stop

	def __next__(self):
		self.current -= 1
		if self.current >= self.start:
			return self.current
		raise StopIteration


# **********************************************************************************************
class RangeRandom( RangeImpl ):
	def __init__( self, start, stop ):
		super().__init__(start, stop)
		self.numbers = [ i for i in range(start,stop) ]
		shuffle(self.numbers)
		self.iter = iter(self.numbers)

	def __iter__(self):
		return self.iter

	def __next__(self):
		return next(self.iter)


# **********************************************************************************************
def main():
	for i in RangeForward(0,5):
		print(i, end=', ')
	print()

	for i in RangeBackward(0,5):
		print(i, end=', ')
	print()

	for i in RangeRandom(0,5):
		print(i, end=', ')
	print()


# **********************************************************************************************
if (__name__ == '__main__'):
    main()


# **********************************************************************************************