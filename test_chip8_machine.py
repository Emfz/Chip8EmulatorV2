from chip8_machine import Chip8Machine
import pytest
import numpy

TEST_SIZE = 50

machine = Chip8Machine()

@pytest.fixture
def sprite1():
	return numpy.array([0xAA, 0x55])

@pytest.fixture
def valid_memory_addresses():
	return numpy.random.randint(0x0, 0x1000, size=TEST_SIZE)

def test_screen(sprite1):
	x = 7
	y = 5

	white = 0xFFFFFF

	manual_array = numpy.zeros(shape=(machine.get_screen_width(), machine.get_screen_height()), dtype=int)

	manual_array[7,5] = white
	manual_array[8,5] = 0
	manual_array[9,5] = white
	manual_array[10,5] = 0
	manual_array[11,5] = white
	manual_array[12,5] = 0
	manual_array[13,5] = white
	manual_array[14,5] = 0

	manual_array[7,6] = 0
	manual_array[8,6] = white
	manual_array[9,6] = 0
	manual_array[10,6] = white
	manual_array[11,6] = 0
	manual_array[12,6] = white
	manual_array[13,6] = 0
	manual_array[14,6] = white

	machine.draw_sprite(sprite1, x, y)

	assert numpy.array_equal(machine.get_screen_state(), manual_array)

	machine.clear_screen()
	assert numpy.array_equal(machine.get_screen_state(), numpy.zeros(shape=(machine.get_screen_width(), machine.get_screen_height()), dtype=int))

def test_read_write_registers():
	for i in range(16):
		number = numpy.random.randint(0,0x100)
		machine.write_register(i, number)
		assert machine.read_register(i) == number

def test_read_write_memory_register():
	number = numpy.random.randint(0, 0xFFF)
	machine.write_memory_register(number)
	assert machine.read_memory_register() == number

def test_overflow_underflow_registers():
	for i in range(16):
		machine.write_register(i, 0xAAA)
		assert machine.read_register(i) == 0xAA

		machine.write_register(i, -0x1)
		assert machine.read_register(i) == 0xFF

		machine.write_memory_register(0x11111)
		assert machine.read_memory_register() == 0x1111

		machine.write_memory_register(-0x1)
		assert machine.read_memory_register() == 0xFFFF

def test_read_write_memory():
	address = numpy.random.randint(0, 0x1001)
	number = numpy.random.randint(0,0x100)
	machine.write_memory(address, number)
	assert machine.read_memory(address) == number

def test_stack(valid_memory_addresses):
	for address in valid_memory_addresses:
		machine.push_stack(address)
		
	for i in range(TEST_SIZE):
		assert machine.pop_stack() == valid_memory_addresses[-i-1]


def test_timers():
	machine.set_timer(0xAA)
	machine.timer_tick()
	assert machine.get_remaining_time() == 0xA9

	machine.set_sound_timer(0x1)
	machine.sound_timer_tick()
	assert machine.get_remaining_sound_time() == 0x0