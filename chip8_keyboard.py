import keyboard

class Chip8Keyboard:
	"""
	Chip 8 keyboard. The key mapping is as follows:

	Original->Virtual:\\
	0x1->1\\
	0x2->2\\
	0x3->3\\
	0xC->4\\
	0x4->q\\
	0x5->w\\
	0x6->e\\
	0xD->r\\
	0x7->a\\
	0x8->s\\
	0x9->d\\
	0xE->f\\
	0xA->z\\
	0x0->x\\
	0xB->c\\
	0xF->v
	"""
	def __init__(self) -> None:
		self.valid_inputs = ['1','2','3','4','q','w','e','r','a','s','d','f','z','x','c','v']
		self.input_to_hex = {'1':0x1,
							'2':0x2,
							'3':0x3,
							'4':0xC,
							'q':0x4,
							'w':0x5,
							'e':0x6,
							'r':0xD,
							'a':0x7,
							's':0x8,
							'd':0x9,
							'f':0xE,
							'z':0xA,
							'x':0,
							'c':0xB,
							'v':0xF			
							}
		
	def is_key_pressed(self, input:str) -> bool:
		"""
		Check if the input key is pressed. Valid inputs are: '1','2','3','4','q','w','e','r','a','s','d','f','z','x','c' and 'v'.

		Parameters
		----------
		input : A string of one of the valid inputs.

		Returns
		-------
		True if the key is pressed, False otherwise.
		"""
		if (keyboard.is_pressed(input)) and (input in self.valid_inputs):
			return True
		return False
	
	def wait_for_input(self) -> int:
		"""
		Waits until a key press. Valid inputs are: '1','2','3','4','q','w','e','r','a','s','d','f','z','x','c' and 'v'.

		Returns
		-------
		An integer corresponding to the hex value of the key that was pressed.
		"""
		while True:
			pressed_key = keyboard.read_key()
			if pressed_key in self.valid_inputs:
				return self.input_to_hex[pressed_key]
