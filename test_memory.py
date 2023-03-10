import pytest
import numpy
from chip8_memory import Chip8Memory

TEST_SIZE = 60

memory = Chip8Memory()

@pytest.fixture
def valid_addresses():
	return numpy.random.randint(0, 0x1000, size=TEST_SIZE)

@pytest.fixture
def valid_values():
	return numpy.random.randint(0, 0xFF, size=TEST_SIZE)

@pytest.fixture
def invalid_addresses1():
	return numpy.random.randint(0x1000, 0x10000, size=TEST_SIZE)

@pytest.fixture
def invalid_addresses2():
	return numpy.random.randint(-0xFFF, 0, size=TEST_SIZE)

@pytest.fixture
def invalid_values():
	return numpy.random.randint(0x100, 0x1000, TEST_SIZE)

@pytest.fixture
def array_of_values():
	return numpy.random.randint(0x0, 0xFF, size=TEST_SIZE)



def test_read_write_memory(valid_addresses, valid_values):
	for address, value in zip(valid_addresses, valid_values):
		memory.write(address, value)

		assert memory.read(address) == value

def test_invalid_addresses(invalid_addresses1, invalid_addresses2):
	with pytest.raises(IndexError):
		for address in invalid_addresses1:
			memory.write(address, 0x0)
		
		for address in invalid_addresses2:
			memory.write(address, 0x0)

def test_data_loss_for_invalid_values(valid_addresses, invalid_values):
	for address, value in zip(valid_addresses, invalid_values):
		memory.write(address, value)
		assert memory.read(address) != value

def test_insert_array(array_of_values):
	address = numpy.random.randint(0x0, 0xFFF)
	memory.write(address, array_of_values)

	assert numpy.array_equal(memory.read_range(address, address + TEST_SIZE), array_of_values)

def test_read_range():
	start_address = numpy.random.randint(0x0,0xFF)
	values = numpy.random.randint(0x0, 0xFF, size=1000)
	memory.write(start_address, values)
	range = memory.read_range(start_address, start_address + len(values))
	assert numpy.array_equal(values, range)