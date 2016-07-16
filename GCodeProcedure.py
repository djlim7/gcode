import os
import string
import GCodeObject

def GCodeSyntaxParser(file_name):
	with open(file_name, 'r') as file_stream:
		main_loop = True
		process_lastmoment = False
		result_list = []
		last_processed_type = 'str'
		while main_loop:
			character = file_stream.read(1)

			if file_stream.tell() == os.fstat(file_stream.fileno()).st_size:
				if process_lastmoment:
					character = ' '
					main_loop = False
				else:
					process_lastmoment = True

			if character in string.ascii_letters:
				if last_processed_type == 'str':
					pass
				elif last_processed_type == 'int':
					pass
				elif last_processed_type == 'space':
					pass

				last_processed_type = 'str'
			elif character.isdigit():
				if last_processed_type == 'str':
					pass
				elif last_processed_type == 'int':
					pass
				elif last_processed_type == 'space':
					pass

				last_processed_type = 'int'
			elif character.isspace():
				if last_processed_type == 'str':
					pass
				elif last_processed_type == 'int':
					pass
				elif last_processed_type == 'space':
					pass

				last_processed_type = 'int'
			else:
				raise GCodeObject.GCodeSyntaxError \
					('The file contains unsupported character.')