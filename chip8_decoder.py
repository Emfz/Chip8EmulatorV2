CATEGORY0 = {
	"mask":0xFFF,
	"opcodes":{
		0x0E0:"opcode00E0",
		0x0EE:"opcode00EE"
	}
}

CATEGORY1 = {
	"opcodes":{
		0x0:"opcode1"
	}
}

CATEGORY2 = {
	"opcodes":{
		0x0:"opcode2"
	}
}

CATEGORY3 = {
	"opcodes":{
		0x0:"opcode3"
	}
}

CATEGORY4 = {
	"opcodes":{
		0x0:"opcode4"
	}
}

CATEGORY5 = {
	"opcodes":{
		0x0:"opcode5"
	}
}

CATEGORY6 = {
	"opcodes":{
		0x0:"opcode6"
	}
}

CATEGORY7 = {
	"opcodes":{
		0x0:"opcode7"
	}
}

CATEGORY8 = {
	"mask":0xF,
	"opcodes":{
		0x0:"opcode8_0",
		0x1:"opcode8_1",
		0x2:"opcode8_2",
		0x3:"opcode8_3",
		0x4:"opcode8_4",
		0x5:"opcode8_5",
		0x6:"opcode8_6",
		0x7:"opcode8_7",
		0xE:"opcode8_E"
	}
}

CATEGORY9 = {
	"opcodes":{
		0x0:"opcode9"
	}
}

CATEGORYA = {
	"opcodes":{
		0x0:"opcodeA"
	}
}

CATEGORYB = {
	"opcodes":{
		0x0:"opcodeB"
	}
}

CATEGORYC = {
	"opcodes":{
		0x0:"opcodeC"
	}
}

CATEGORYD = {
	"opcodes":{
		0x0:"opcodeD"
	}
}

CATEGORYE = {
	"mask":0xFF,
	"opcodes":{
		0x9E:"opcodeE_9E",
		0xA1:"opcodeE_A1"
	}
}

CATEGORYF = {
	"mask":0xFF,
	"opcodes":{
		0x07:"opcodeF_07",
		0x0A:"opcodeF_0A",
		0x15:"opcodeF_15",
		0x18:"opcodeF_18",
		0x1E:"opcodeF_1E",
		0x29:"opcodeF_29",
		0x33:"opcodeF_33",
		0x55:"opcodeF_55",
		0x65:"opcodeF_65"
	}
}


DECODER = {
	0x0:CATEGORY0,
	0X1:CATEGORY1,
	0X2:CATEGORY2,
	0X3:CATEGORY3,
	0X4:CATEGORY4,
	0X5:CATEGORY5,
	0X6:CATEGORY6,
	0X7:CATEGORY7,
	0X8:CATEGORY8,
	0X9:CATEGORY9,
	0XA:CATEGORYA,
	0XB:CATEGORYB,
	0XC:CATEGORYC,
	0XD:CATEGORYD,
	0XE:CATEGORYE,
	0XF:CATEGORYF
}