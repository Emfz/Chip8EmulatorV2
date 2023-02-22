from pygame import SCALED, FULLSCREEN, PixelArray, time
from pygame.display import init, set_mode, get_surface, get_init, flip
from pygame.pixelcopy import array_to_surface, surface_to_array
import numpy

white = 0xFFFFFF

class Chip8Screen:
	def __init__(self) -> None:
		self.initialize()

	def initialize(self) -> None:
		"""
		Initializes the screen by setting its width, height, "scaled and fullscreen" flags, storing
		the surface in aa variable and creaating a pixel array to modify each individual pixel.
		"""
		self.width = 64
		self.height = 32
		init()
		set_mode(size=(self.width, self.height), flags = SCALED | FULLSCREEN)
		self.surface = get_surface()
		self.pixel_array = PixelArray(self.surface)
	
	def get_init(self) -> bool:
		"""
		Get the init state of the pygame display.

		Returns
		-------
		True if the display is initialized, False otherwise.
		"""
		return get_init()
	
	def update(self) -> None:
		"""
		Display the pixels inside the surface in the display.
		"""
		flip()

	def set_pixels(self, pixel_array:numpy.ndarray) -> None:
		"""
		Send a complete buffer to the screen. This method is for testing and development, because this funcionality
		isn't part of the Chip 8 standard.

		Parameters
		------------
		pixel_array : A numpy.ndarray of dimensions (64, 32) with the color of each pixel represented 
		by an integer hexadecimal number 0xNNNNNN.
		"""
		array_to_surface(self.surface, pixel_array)

	def clear(self) -> None:
		"""
		Sets all pixels of the screen to black.
		"""
		array_to_surface(self.surface, numpy.zeros(shape=(self.width, self.height), dtype=int))

	def get_state(self) -> numpy.ndarray:
		"""
		Get the current state of the pixels of the screen.

		Returns
		-------
		A numpy.ndarray of dimensions (64,32) containing the current value of every pixel.
		"""
		state_array = numpy.ndarray(shape=(self.width, self.height), dtype=int)
		surface_to_array(state_array, self.surface)
		return state_array
	
	def draw_sprite(self, sprite:numpy.ndarray, x:int, y:int) -> bool:
		"""
		Draw a sprite 8 pixels wide and specifiable height at coordinates (x,y). The pixels of the screen are xor'd with the sprite's pixels,
		so if the current sprite bit = 1, the screen pixel is toggled. If the sprite's bit = 0, the screen pixel is left unchanged.

		Parameters
		----------
		sprite : A numpy.ndarray 1-D array that meets the following conditions.
		1) Each element of the array is a hexadecimal integer number 0xNN, representing 8 pixels (a byte) in a row.
		2) The value of each of the 8 bits of the number 0xNN dictates whether the corresponding pixel screen will be toggled 
		(sprite bit = 1) or left alone (sprite bit = 0).
		3) The height of the sprite is specified by the number of elements of the array.
		
		x : Horizontal coordinate where the top left corner of the sprite will be located.
		y : Vertical coordinate where the top left corner of the sprite will be located.

		Returns
		-------
		True if any of the screen pixels were toggled from 1 to 0, False otherwise

		Example
		-------
		draw_sprite(numpy.array([0xFF, 0xAA]), 2, 10) will draw a sprite 8 pixels wide and 2 pixels tall at coordinates (2,10).
		The sprite will have the following pattern:\\
		■ ■ ■ ■ ■ ■ ■ ■ \\
		■ □ ■ □ ■ □ ■ □

		"""
		# Logic (not bitwise) xor function to toggle screen pixels
		xor = lambda a,b : (a and not b) or (b and not a)

		state = self.get_state()
		result_array = numpy.copy(state)
		screen_pixel_flipped = False
		for byte in sprite:
			mask = 0b10000000
			iteration = 0
			while mask > 0:
				try:
					# Get a single bit from the sprite's byte
					bit = byte & mask
					# Toggle the current screen pixel if the sprite's bit = 1, set to 0 otherwise.
					result_array[x + iteration, y] = xor(bit, state[x + iteration, y]) and white
					# Check if the current screen pixel was toggled from 1 to 0
					if bit and state[x + iteration, y]:
						screen_pixel_flipped = True
				except IndexError:
					# If the current pixel is outside of the screen, do nothing
					pass
				finally:
					mask >>= 1
					iteration += 1
			y += 1

		array_to_surface(self.surface, result_array)
		return screen_pixel_flipped