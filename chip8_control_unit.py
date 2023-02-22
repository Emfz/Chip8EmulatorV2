from chip8_machine import Chip8Machine
from chip8_decoder import *
import numpy
import time


class Chip8ControlUnit():
	def __init__(self) -> None:
		self.machine = Chip8Machine()
		self.program_counter = 0x200
		
	def load_file(self, file_path:str):
		"""
		Load a Chip8 (*.ch8) file into the virtual machine's memory.

		Parameters
		----------
		file_path : A string containing the path to the file
		"""
		with open(file_path, 'rb') as file:
			file_contents = numpy.fromfile(file, dtype='B')
		self.machine.write_memory(0x200, file_contents)

	def execute_instruction(self):
		bytes = self.machine.read_memory_range(self.program_counter, self.program_counter + 2)
		code = bytes[0]
		code <<= 0x8
		code |= bytes[1]
		self.decode_and_execute(code)

	def tick_timers(self):
		if self.machine.get_remaining_time() > 0:
			self.machine.timer_tick()

		if self.machine.get_remaining_sound_time() > 0:
			self.machine.sound_timer_tick()

	def decode_and_execute(self, code:int):
		"""
		Decode and execute an opcode.

		Parameters
		----------
		code : The 2 byte integer (0x0,0xFFFF) for the opcode to be executed.
		"""
		# Get the broad category of the code, which corresponds to the most significant four bits.
		opcode_category = (code & 0xF000) >> 12

		# The remainder will be used to get the specific opcode and send arguments if required
		remainder = code & 0xFFF
		
		# Get the complete set of opcodoes corresponding to the opcode_category
		category = DECODER[opcode_category]
		# Get the mask corresponding to this opcode_category, to identify the specific opcode
		category_mask = category.get("mask")
		if category_mask is None:
			# If there's no mask for this category, then there's only a single opcode
			opcode = category["opcodes"][0x0]
		else:
			# Otherwise, find the specific opcode by using the category's mask
			opcode = category["opcodes"][remainder & category_mask]
		
		# Finally, call the specific opcode and send its arguments
		self.__getattribute__(opcode)(remainder)

		self.program_counter += 0x2
	

	# Opcodes
	def opcode00E0(self, remainder:int):
		"""
		Clear the screen.
		"""
		self.machine.clear_screen()

	def opcode00EE(self, remainder:int):
		"""
		Return from subroutine
		"""
		# 0x2 is subtracted because decode_and_execute increments the program counter by 0x2
		self.program_counter = self.machine.pop_stack() -0x2
	
	def opcode1(self, remainder:int):
		"""
		Jump to an address in the range (0x0,0xFFF)
		"""
		# 0x2 is subtracted because decode_and_execute increments the program counter by 0x2
		self.program_counter = remainder - 0x2

	def opcode2(self, remainder:int):
		"""
		Call the subroutine at an address in the range (0x0,0xFFF)
		"""
		self.machine.push_stack(self.program_counter)
		# 0x2 is subtracted because decode_and_execute increments the program counter by 0x2
		self.program_counter = remainder - 0x2

	def opcode3(self, remainder:int):
		"""
		Skip the next instruction if register Vx == NN, NN is a 1 byte constant (0x0,0xFF)
		"""
		value = self.read_one_register(remainder)
		constant = remainder & 0xFF
		
		if value == constant:
			self.program_counter += 0x2
	
	def opcode4(self, remainder:int):
		"""
		Skip the next instruction if register Vx != NN, NN is a 1 byte constant (0x0,0xFF)
		"""
		value = self.read_one_register(remainder)
		constant = remainder & 0xFF

		if value != constant:
			self.program_counter += 0x2

	def opcode5(self, remainder:int):
		"""
		Skip the next instruction if registers Vx == Vy.
		"""
		value1, value2 = self.read_two_registers(remainder)

		if value1 == value2:
			self.program_counter += 0x2

	def opcode6(self, remainder:int):
		"""
		Set register Vx = NN, NN is a 1 byte constant (0x0,0xFF)
		"""
		self.machine.write_register((remainder & 0xF00) >> 8, remainder & 0xFF)

	def opcode7(self, remainder:int):
		"""
		Set register Vx += NN, NN is a 1 byte constant (0x0,0xFF), without changing the carry flag.
		"""
		register_value = self.read_one_register(remainder)
		self.machine.write_register((remainder & 0xF00) >> 8, register_value + (remainder & 0xFF))

	def opcode8_0(self, remainder:int):
		"""
		Set register Vx = Vy
		"""
		self.machine.write_register((remainder & 0xF00) >> 8, self.machine.read_register((remainder & 0xF0) >> 4))

	def opcode8_1(self, remainder:int):
		"""
		Set register Vx |= Vy (bitwise or)
		"""
		value1, value2 = self.read_two_registers(remainder)
		self.machine.write_register((remainder & 0xF00) >> 8, value1 | value2)

	def opcode8_2(self, remainder:int):
		"""
		Set register Vx &= Vy (bitwise and)
		"""
		value1, value2 = self.read_two_registers(remainder)
		self.machine.write_register((remainder & 0xF00) >> 8, value1 & value2)
	
	def opcode8_3(self, remainder:int):
		"""
		Set register Vx ^= Vy (bitwise xor)
		"""
		value1, value2 = self.read_two_registers(remainder)
		self.machine.write_register((remainder & 0xF00) >> 8, value1 ^ value2)

	def opcode8_4(self, remainder:int):
		"""
		Set register Vx += Vy. Sets a carry flag in register Vf.
		"""
		value1, value2 = self.read_two_registers(remainder)
		result = value1 + value2
		self.machine.write_register((remainder & 0xF00) >> 8, result)
		if result > 0xFF:
			self.set_registerF(0x1)
		else:
			self.set_registerF(0x0)
	
	def opcode8_5(self, remainder:int):
		"""
		Set register Vx -= Vy. Sets a borrow flag in register Vf.
		"""
		value1, value2 = self.read_two_registers(remainder)
		result = value1 - value2
		self.machine.write_register((remainder & 0xF00) >> 8, result)
		if result < 0x0:
			self.set_registerF(0x0)
		else:
			self.set_registerF(0x1)

	def opcode8_6(self, remainder:int):
		"""
		Store the least significant bit of Vx in Vf and shift Vx >> 1
		"""
		value = self.read_one_register(remainder)
		self.set_registerF(value & 0x1)
		self.machine.write_register((remainder & 0xF00) >> 8, value >> 0x1)
	
	def opcode8_7(self, remainder:int):
		"""
		Set register Vx -= Vy. Set a borrow flag in register Vf.
		"""
		value1, value2 = self.read_two_registers(remainder)
		result = value1 - value2
		self.machine.write_register((remainder & 0xF00) >> 8, result)
		if result < 0:
			self.set_registerF(0x0)
		else:
			self.set_registerF(0x1)

	def opcode8_E(self, remainder:int):
		"""
		Store the most significant bit of Vx in Vf, then shift Vx << 1
		"""
		value = self.read_one_register(remainder)
		self.set_registerF((value & 0x80) >> 0x7)
		self.machine.write_register((remainder & 0xF00) >> 8, value << 0x1)

	def opcode9(self, remainder:int):
		"""
		Skip the next instruction if Vx != Vy
		"""
		value1, value2 = self.read_two_registers(remainder)
		if value1 != value2:
			self.program_counter += 0x2
		
	def opcodeA(self, remainder:int):
		"""
		Set register I to a constant NNN (0x0,0xFFF)
		"""
		self.machine.write_memory_register(remainder)
	
	def opcodeB(self, remainder:int):
		"""
		Jump to address V0 + NNN
		"""
		# 0x2 is subtracted because decode_and_execute increments the program counter by 0x2
		self.program_counter = self.machine.read_register(0x0) + remainder - 0x2
	
	def opcodeC(self, remainder:int):
		"""
		Set register Vx = rand() & NN, NN is a constant in the range (0x0,0xFF)
		"""
		random_number = numpy.random.randint(0, 0x100)
		self.machine.write_register((remainder & 0xF00) >> 8, (random_number) & (remainder & 0xFF))

	def opcodeD(self, remainder:int):
		"""
		Draw sprite according to the rules described in the screen module.
		"""
		start_address = self.machine.read_memory_register()
		sprite_height = remainder & 0xF
		sprite = self.machine.read_memory_range(start_address, start_address + sprite_height)
		x, y = self.read_two_registers(remainder)
		print(f"The values before drawing are.")
		print(f"startadrress:{hex(start_address)}, spriteheight:{hex(sprite_height)}, x:{x}, y:{y}, sprite:{sprite}")
		pixels_flipped = self.machine.draw_sprite(sprite, x, y)
		if pixels_flipped:
			self.set_registerF(0x1)
		else:
			self.set_registerF(0x0)
		
		self.machine.update_screen()

	def opcodeE_9E(self, remainder:int):
		"""
		Skip the next instruction if the given key is pressed.
		"""
		key = self.read_one_register(remainder)
		if self.machine.is_key_pressed(key):
			self.program_counter += 0x2
	
	def opcodeE_A1(self, remainder:int):
		"""
		Skip the next instruction if the given key is not pressed
		"""
		key = self.read_one_register(remainder)
		if not self.machine.is_key_pressed(key):
			self.program_counter += 0x2

	def opcodeF_07(self, remainder:int):
		"""
		Set register Vx to the value of the timer
		"""
		self.machine.write_register((remainder & 0xF00) >> 8, self.machine.get_remaining_time())

	def opcodeF_0A(self, remainder:int):
		"""
		Wait for an input and store it in Vx, halt all operations meanwhile.
		"""
		self.machine.write_register((0xF00) >> 8, self.machine.wait_for_input())
	
	def opcodeF_15(self, remainder:int):
		"""
		Set the timer to the value stored in register Vx.
		"""
		self.machine.set_timer(self.read_one_register(remainder))
	
	def opcodeF_18(self, remainder:int):
		"""
		Set the sound timer to the value stored in register Vx.
		"""
		self.machine.set_sound_timer(self.read_one_register(remainder))

	def opcodeF_1E(self, remainder:int):
		"""
		Set register I += Vx, without affecting the flag register (VF).
		"""
		self.machine.write_memory_register(self.read_one_register(remainder) + self.machine.read_memory_register())

	def opcodeF_29(self, remainder:int):
		"""
		Set register I to the location of the char whose value is stored in Vx.
		"""
		# TODO: Implement font
		pass

	def opcodeF_33(self, remainder:int):
		"""
		Store the binary-coded representation of the value stored in Vx, in register I
		"""
		starting_address = self.machine.read_memory_register()
		value = self.read_one_register(remainder)
		
		print(f"The value i got is {value}")
		self.machine.write_memory(starting_address, value // 100 % 10)
		self.machine.write_memory(starting_address + 1, value // 10 % 10)
		self.machine.write_memory(starting_address + 2, value % 10)

	
	def opcodeF_55(self, remainder:int):
		"""
		Store the values stored in registers V0 to Vx (inclusive) in memory, starting at address I.
		"""
		starting_address = self.machine.read_memory_register()
		number_of_registers = (remainder & 0xF00) >> 0x8
		print(f"numberofregisters: {number_of_registers}")
		for i in range(number_of_registers + 1):
			print(f"starting address:{starting_address}, i:{i}, numberofregisters:{number_of_registers}, remainder:{hex(remainder)}")
			self.machine.write_memory(starting_address + i, self.machine.read_register(i))
		
	def opcodeF_65(self, remainder:int):
		"""
		Fill registers V0 to Vx (inclusive) in memory, from values in memory starting from address I.
		"""
		starting_address = self.machine.read_memory_register()
		print(f"My starting address is  {starting_address}")
		number_of_registers = (remainder & 0xF00) >> 0x8
		for i in range(number_of_registers + 1):
			self.machine.write_register(i, self.machine.read_memory(starting_address + i))


	# Helper methods
	def read_one_register(self, remainder:int) -> int:
		"""
		This method is designed to work alongside Chip 8 opcodes. Reads the value of a single register.

		Parameters
		----------
		remainder : The 12 least significant bits of the opcode (opcode & 0x0FFF). The register number is given by ((remainder & 0xF00) >> 8)
		"""
		return self.machine.read_register((remainder & 0xF00) >> 8)

	def read_two_registers(self, remainder:int) -> int:
		"""
		This method is designed to work alongside Chip 8 opcodes. Reads the value of two registers.

		Parameters
		----------
		remainder : The 12 least significant bits of the opcode (opcode & 0x0FFF). The first register number is ((remainder & 0xF00) >> 8).
		The second register number is (remainder & 0xF0)
		"""
		return self.machine.read_register((remainder & 0xF00) >> 8), self.machine.read_register((remainder & 0xF0) >> 0x4)

	def set_registerF(self, value:int):
		"""
		This methos is a shortcut for self.machine.write_register(15, value), because registerF is used as a helper for some
		opcodes.
		"""
		self.machine.write_register(15, value)

