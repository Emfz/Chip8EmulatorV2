import pytest
import numpy
from chip8_stack import Chip8Stack

stack = Chip8Stack()

@pytest.fixture
def memory_addresses():
	return numpy.random.randint(0x0, 0xFFF, size=10)

def test_stack(memory_addresses):
	for address in memory_addresses:
		stack.push(address)

	for i in range(len(memory_addresses)):
		assert stack.pop() == memory_addresses[-i-1]

def test_empty_exception():
	with pytest.raises(IndexError):
		stack.pop()