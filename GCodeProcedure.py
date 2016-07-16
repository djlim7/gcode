import os
import string
import GCodeObject

def GCodeSyntaxParser(file_name):
	with open(file_name, 'r') as file_stream:
		main_loop = True
		process_lastmoment = False
		result_list = []
		last_processed_type = 'space'
		while main_loop:
			character = (file_stream.read(1)).upper()

			if file_stream.tell() == os.fstat(file_stream.fileno()).st_size:
				if process_lastmoment:
					character = ' '
					main_loop = False
				else:
					process_lastmoment = True

			if character in string.ascii_letters: # 'str'
				result_list.append(character)

				last_processed_type = 'str'
			elif character.isdigit(): # 'int'
				if last_processed_type == 'str':
					result_list.append(int(character))
				elif last_processed_type == 'int':
					result_list[-1] = int(result_list[-1]) * 10 + int(character)
				elif last_processed_type == 'space':
					result_list.append(int(character))

				last_processed_type = 'int'
			elif character.isspace(): # 'space'
				last_processed_type = 'space'
			else:
				raise GCodeObject.GCodeSyntaxError \
					('The file contains unsupported character.')

	return tuple(result_list)