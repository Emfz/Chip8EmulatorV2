import numpy

class Chip8Memory:
	def __init__(self) -> None:
		self.memory = numpy.zeros(shape=(4096), dtype=int)
	
	def read(self, address:int) -> int:
		"""
		Read the value stored at the given address.

		Parameters
		----------
		address : int in the range 0x0, 0xFFF
		"""
		return self.memory[address & 0xFFF]

	def read_range(self, start:int, finish:int) -> numpy.ndarray:
		"""
		Read a chunk of memory. Start inclusive, finish non-inclusive.

		Parameters
		----------
		start : int in the range (0x0,0xFFF)
		finish : int in the range (0x0,0xFFF)

		Returns
		-------
		A numpy.ndarray containing a copy of the memory in the specified range.
		"""
		return self.memory[start:finish]
	
	def write(self, address:int, value:int|numpy.ndarray) -> None:
		"""
		Write a value into the given address. The Chip 8 memory has 1 byte cells, therefore, attempting to store a value larger than 0xFF
		will result in data loss.

		Parameters
		----------
		address : int in the range [0x0,0xFFF] where the value will be inserted.
		value : int in the range [0x0,0xFF] OR a numpy.ndarray whose elements are ints within the range [0x0,0xFF]
		"""
		if type(value) is numpy.ndarray:
			self.memory.put([address + i for i in range(len(value))], value & 0xFF)
		else:
			self.memory[address] = value & 0xFF