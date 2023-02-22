import pytest
import numpy
import time
from chip8_control_unit import Chip8ControlUnit

TEST_SIZE = 300

white = 0xFFFFFF

# Keyboard input and timers are not tested here

def test_draw_screen():
	chip8vm = Chip8ControlUnit()
	sprite = numpy.array([0xAA, 0x55, 0xAA, 0x55])
	
	# Load sprite into registers
	chip8vm.decode_and_execute(0x60AA)
	chip8vm.decode_and_execute(0x6155)
	chip8vm.decode_and_execute(0x62AA)
	chip8vm.decode_and_execute(0x6355)

	assert chip8vm.machine.read_register(0) == 0xAA
	assert chip8vm.machine.read_register(1) == 0x55
	assert chip8vm.machine.read_register(2) == 0xAA
	assert chip8vm.machine.read_register(3) == 0x55

	# Load the I register with 0x345
	chip8vm.decode_and_execute(0xA345)
	assert chip8vm.machine.read_memory_register() == 0x345

	# Load registers (sprite data) into memory
	chip8vm.decode_and_execute(0xF355)
	assert numpy.array_equal(chip8vm.machine.read_memory_range(0x345, 0x345 + 0x4), sprite)

	# Load register 10 with the (x,y) coordinates where the sprite will be drawn
	chip8vm.decode_and_execute(0x6A00)
	assert chip8vm.machine.read_register(0xA) == 0

	# Draw sprite on screen
	chip8vm.decode_and_execute(0xDAA4)
	chip8vm.machine.update_screen()
	
	manual_array = numpy.zeros(shape=(chip8vm.machine.get_screen_width(), chip8vm.machine.get_screen_height()), dtype=int)
	manual_array[0,0] = white
	manual_array[2,0] = white
	manual_array[4,0] = white
	manual_array[6,0] = white

	manual_array[1,1] = white
	manual_array[3,1] = white
	manual_array[5,1] = white
	manual_array[7,1] = white

	manual_array[0,2] = white
	manual_array[2,2] = white
	manual_array[4,2] = white
	manual_array[6,2] = white

	manual_array[1,3] = white
	manual_array[3,3] = white
	manual_array[5,3] = white
	manual_array[7,3] = white

	assert numpy.array_equal(chip8vm.machine.get_screen_state(), manual_array)
	
	# Clear the screen
	chip8vm.decode_and_execute(0x00E0)
	chip8vm.machine.update_screen()
	assert numpy.array_equal(chip8vm.machine.get_screen_state(), numpy.zeros(shape=(chip8vm.machine.get_screen_width(), chip8vm.machine.get_screen_height())))

def test_load_program():
	chip8vm = Chip8ControlUnit()
	
	chip8vm.load_file("octojam1title.ch8")

	program = numpy.fromfile("octojam1title.ch8", dtype='B')

	assert numpy.array_equal(chip8vm.machine.read_memory_range(0x200, 0x200 + len(program)), program)

def test_flow_control():
	chip8vm = Chip8ControlUnit()

	# Jump to random address
	random_address1 = numpy.random.randint(0x0, 0x1000)
	code = 0x1000 | random_address1
	chip8vm.decode_and_execute(code)
	assert chip8vm.program_counter == random_address1

	# Call subroutine at random address
	random_address2 = numpy.random.randint(0x0, 0x1000)
	code = 0x2000 | random_address2
	chip8vm.decode_and_execute(code)
	assert chip8vm.program_counter == random_address2

	# Return from subroutine
	chip8vm.decode_and_execute(0x00EE)
	assert chip8vm.program_counter == random_address1

	# Jump to addresss plus V0
	# Load register V0 with an offset
	random_offset = numpy.random.randint(0x0, 0x100)
	code = 0x6000 | random_offset	
	chip8vm.decode_and_execute(code)
	# Create a random address with a max value 0xFF places below 0xFFF (to avoid going out of the memory range)
	random_address3 = numpy.random.randint(0x0, 0x1000 - 0xFF)
	code = 0xB000 | random_address3
	chip8vm.decode_and_execute(code)

	assert chip8vm.program_counter == random_address3 + random_offset

def test_flow_control_if_statements():
	chip8vm = Chip8ControlUnit()

	# Make the screen white before the test begins
	white_screen = numpy.full(shape=(chip8vm.machine.get_screen_width(), chip8vm.machine.get_screen_height()), fill_value=white)
	chip8vm.machine._screen.set_pixels(white_screen)

	# This program will evaluate if the conditional opcodes (0x3XNN, 0x4XNN, 0x5XY0, 0x9XY0) are working properly. If they are,
	# the screen will remain white, otherwise, it'll be cleared.
	with open("test.ch8", "wb") as program_file:
		# The program is as follows:
		# 1) Load 0xA0 into register 0
		program_as_string = "60 A0 "
		# 2) Load 0xFF into register F
		program_as_string += "6F FF "
		# 3) Load 0x55 into register 1
		program_as_string += "61 55 "
		# 4) Load 0x55 into register E
		program_as_string += "6E 55 "
		# 5) Load 0xAA into register 2
		program_as_string += "62 AA "
		# 6) Load 0x33 into register D
		program_as_string += "6D 33 "
		# 7) If V0 == A0, don't clear the screen
		program_as_string += "30 A0 00 E0 "
		# 8) If VF != 0x33, don't clear the screen
		program_as_string += "4F 33 00 E0 "
		# 9) If V1 == VE, don't clear the screen
		program_as_string += "51 E0 00 E0 "
		# 10) If V2 != VD, don't clear the screen
		program_as_string += "92 D0 00 E0"

		program = bytes.fromhex(program_as_string)
		program_file.write(program)
	
	chip8vm.load_file("test.ch8")
	for i in range(10):
		chip8vm.execute_instruction()
		assert numpy.array_equal(chip8vm.machine.get_screen_state(), white_screen)

def test_memory_register_opcodes():
	chip8vm = Chip8ControlUnit()

	# Test for code ANNN (I = NNN)
	# Set the memory register to a random address
	random_address1 = numpy.random.randint(0x0, 0x1000)
	code = 0xA000 | random_address1
	chip8vm.decode_and_execute(code)
	assert chip8vm.machine.read_memory_register() == random_address1

	# ------------------------------------------------------------------------
	# Test for code FX1E (I += Vx)

	# Generate a random number
	random_number2 = numpy.random.randint(0x0, 0x100)
	
	# Store the random number into a random register, excluding VF
	random_register2 = numpy.random.randint(0x0, 0xF)
	code = 0x6000 | (random_register2 << 0x8) | random_number2
	chip8vm.decode_and_execute(code)
	
	# Set the memory register to a random address, accounting for the maximum possibble random offset (0xFF) given by random_number2
	random_address2 = numpy.random.randint(0x0, 0x1000 - 0xFF)
	code = 0xA000 | random_address2
	chip8vm.decode_and_execute(code)

	# Set register VF to 0xAA
	chip8vm.decode_and_execute(0x6FAA)

	# Do I += Vx
	code = 0xF01E | (random_register2 << 0x8)
	chip8vm.decode_and_execute(code)
	
	# Check that I was incremented properly and VF was unaffected
	assert chip8vm.machine.read_register(0xF) == 0xAA
	assert chip8vm.machine.read_memory_register() == random_address2 + random_number2

	# -----------------------------------------------------------------------
	# Test for code 0xFX33 (Store the binary-coded decimal representation of the value of register X 
	# in register memory, starting at address I)
	
	random_register3 = numpy.random.randint(0x0, 0x10)
	random_address3 = numpy.random.randint(0x0, 0x1000)

	# Load the random address into I
	code = 0xA000 | random_address3
	chip8vm.decode_and_execute(code)
	assert chip8vm.machine.read_memory_register() == random_address3

	# Create the bcd representation
	code = 0xF033 | (random_register3 << 0x8)
	chip8vm.decode_and_execute(code)

	number = chip8vm.machine.read_register(random_register3)
	first_digit = number % 10
	second_digit = number // 10 % 10
	third_digit = number // 100 % 10
	assert chip8vm.machine.read_memory(chip8vm.machine.read_memory_register()) == third_digit
	assert chip8vm.machine.read_memory(chip8vm.machine.read_memory_register() + 1) == second_digit
	assert chip8vm.machine.read_memory(chip8vm.machine.read_memory_register() + 2) == first_digit


def test_codeF_55_and_F_65():
	chip8vm = Chip8ControlUnit()

	# ---------------------------------------------
	# Load all registers with a random number
	random_numbers = numpy.random.randint(0x0, 0x100, size=0xF)
	for i in range(0xF):
		code = 0x6000 | (i << 0x8) | random_numbers[i]
		chip8vm.decode_and_execute(code)
	
	# Save all registers to memory starting at address 0x200
	# Set I = 0x200
	chip8vm.decode_and_execute(0xA200)
	# Save the registers
	chip8vm.decode_and_execute(0xFF55)
	# Check that I was unaffected
	assert chip8vm.machine.read_memory_register() == 0x200
	# Check that the registers were saved
	for i in range(0xF):
		assert chip8vm.machine.read_register(i) == random_numbers[i]

	# -------------------------------------------
	# Load memory with random values starting at address 0x400
	random_numbers2 = numpy.random.randint(0x0, 0x100, size=0xF)
	# Set I = 0x400
	chip8vm.decode_and_execute(0xA400)
	for i in range(len(random_numbers2)):
		chip8vm.machine.write_memory(chip8vm.machine.read_memory_register() + i, random_numbers2[i])

	# Load registers from memory
	chip8vm.decode_and_execute(0xFF65)
	# Check that I was unaffected
	assert chip8vm.machine.read_memory_register() == 0x400
	# Check the values
	for i in range(len(random_numbers2)):
		assert chip8vm.machine.read_register(i) == random_numbers2[i]

def test_math_opcodes():
	chip8vm = Chip8ControlUnit()
	# Set V0=0xAA, V1=0x55
	chip8vm.decode_and_execute(0x60AA)
	chip8vm.decode_and_execute(0x6155)
	assert chip8vm.machine.read_register(0) == 0xAA
	assert chip8vm.machine.read_register(1) == 0x55

	# V0 += 0x55
	chip8vm.decode_and_execute(0x7055)
	assert chip8vm.machine.read_register(0) == 0xFF

	# V0=0xAA
	chip8vm.decode_and_execute(0x60AA)
	# V0=V1
	chip8vm.decode_and_execute(0x8010)
	assert chip8vm.machine.read_register(0) == 0x55

	# V0 = 0xAA
	chip8vm.decode_and_execute(0x60AA)
	# V0 |= V1
	chip8vm.decode_and_execute(0x8011)
	assert chip8vm.machine.read_register(0) == 0xFF

	# V0 = 0xAA
	chip8vm.decode_and_execute(0x60AA)
	# V0 &= V1
	chip8vm.decode_and_execute(0x8012)
	assert chip8vm.machine.read_register(0) == 0x0

	# V0 = 0xAA
	chip8vm.decode_and_execute(0x60AA)
	# V0 ^= V0
	chip8vm.decode_and_execute(0x8003)
	assert chip8vm.machine.read_register(0) == 0x0

	# V0 = 0xAA
	chip8vm.decode_and_execute(0x60AA)
	# V0+=V1
	chip8vm.decode_and_execute(0x8014)
	assert chip8vm.machine.read_register(0) == 0xFF
	# Check the flag is unset
	assert chip8vm.machine.read_register(0xF) == 0
	# V0+=V1
	chip8vm.decode_and_execute(0x8014)
	assert chip8vm.machine.read_register(0) == 0x54
	# Check the flag is set
	assert chip8vm.machine.read_register(0xF) == 1

	# V0=0xAA
	chip8vm.decode_and_execute(0x60AA)
	# V0-=V1
	chip8vm.decode_and_execute(0x8015)
	# Check the value is correct and the flag was set to 1
	assert chip8vm.machine.read_register(0) == 0x55
	assert chip8vm.machine.read_register(0xF) == 1

	# Subtract V0-=V1 twice to force a borrow
	chip8vm.decode_and_execute(0x8015)
	chip8vm.decode_and_execute(0x8015)
	assert chip8vm.machine.read_register(0) == 0xAB
	assert chip8vm.machine.read_register(0xF) == 0

	# V0=0x55
	chip8vm.decode_and_execute(0x6055)
	# V0>>=1
	chip8vm.decode_and_execute(0x8016)
	assert chip8vm.machine.read_register(0) == 0x2A
	assert chip8vm.machine.read_register(0xF) == 1

	# V0=0x0
	chip8vm.decode_and_execute(0x6000)
	# V0=V1-V0, flag unset (borrow)
	chip8vm.decode_and_execute(0x8017)
	assert chip8vm.machine.read_register(0) == 0xAB
	assert chip8vm.machine.read_register(0xF) == 0x0

	# V0=0xFF
	chip8vm.decode_and_execute(0x60FF)
	# V0=V1-V0, flag set (no borrow)
	chip8vm.decode_and_execute(0x8017)
	assert chip8vm.machine.read_register(0) == 0xAA
	assert chip8vm.machine.read_register(0xF) == 0x1

	# V0=0xAA
	chip8vm.decode_and_execute(0x60AA)
	# VF=0x0
	chip8vm.decode_and_execute(0x6F00)
	# V0<<=1
	chip8vm.decode_and_execute(0x801E)
	assert chip8vm.machine.read_register(0) == 0x54
	assert chip8vm.machine.read_register(0xF) == 0x1


