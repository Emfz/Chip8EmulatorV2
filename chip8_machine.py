import numpy
from chip8_screen import Chip8Screen
from chip8_keyboard import Chip8Keyboard
from chip8_register import Chip8Register, Chip8MemoryRegister
from chip8_stack import Chip8Stack
from chip8_timer import Chip8Timer
from chip8_memory import Chip8Memory
from chip8_font import font

class Chip8Machine:
	def __init__(self) -> None:
		self._screen = Chip8Screen()
		self._registers = [Chip8Register() for i in range(17)]
		self._memory_register = Chip8MemoryRegister()
		self._memory = Chip8Memory()
		self._keyboard = Chip8Keyboard()
		self._stack = Chip8Stack()
		self._timer = Chip8Timer()
		self._sound_timer = Chip8Timer()

		# Load the font into memory
		for key, value in font.items():
			self._memory.write(key * 0x5, numpy.array(value))

	def draw_sprite(self, sprite:numpy.ndarray, x:int, y:int) -> bool:
		return self._screen.draw_sprite(sprite, x, y)

	def update_screen(self) -> None:
		self._screen.update()

	def clear_screen(self) -> None:
		self._screen.clear()

	def get_screen_state(self) -> numpy.ndarray:
		return self._screen.get_state()
	
	def get_screen_width(self) -> int:
		return self._screen.width
	
	def get_screen_height(self) -> int:
		return self._screen.height

	def read_register(self, register_number:int) -> int:
		return self._registers[register_number].get_state()
	
	def write_register(self, register_number:int, value:int) -> None:
		self._registers[register_number].set(value)

	def read_memory_register(self) -> int:
		return self._memory_register.get_state()

	def write_memory_register(self, value:int) -> None:
		self._memory_register.set(value)
	
	def read_memory(self, address:int) -> int:
		return self._memory.read(address)

	def read_memory_range(self, start:int, finish:int):
		return self._memory.read_range(start, finish)

	def write_memory(self, address:int, value:int|numpy.ndarray) -> None:
		self._memory.write(address, value)
	
	def is_key_pressed(self, input:int) -> bool:
		return self._keyboard.is_key_pressed(input)

	def wait_for_input(self) -> int:
		return self._keyboard.wait_for_input()
	
	def push_stack(self, value:int) -> None:
		self._stack.push(value)

	def pop_stack(self) -> int:
		return self._stack.pop()

	def get_remaining_time(self) -> int:
		return self._timer.get_remaining_time()

	def set_timer(self, value:int) -> None:
		self._timer.set(value)
	
	def timer_tick(self) -> None:
		self._timer.tick()

	def get_remaining_sound_time(self) -> int:
		return self._sound_timer.get_remaining_time()

	def set_sound_timer(self, value:int) -> None:
		self._sound_timer.set(value)

	def sound_timer_tick(self) -> None:
		self._sound_timer.tick()