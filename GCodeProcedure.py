import os
import string
import GCodeObject

def GCodeSyntaxParser(file_name):
	with open(file_name, 'r') as file_stream:
		main_loop = True
		process_lastmoment = False
		result_list = []
		last_processed_type = 'space' # 'str', 'float', 'space', 'minus', 'dot'
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
			elif character.isdigit(): # 'float'
				if last_processed_type == 'str':
					result_list.append(float(character))
				elif last_processed_type == 'float':
					result_list[-1] = float(result_list[-1]) * 10 + float(character)
				elif last_processed_type == 'space':
					result_list.append(float(character))

				last_processed_type = 'float'
			elif character.isspace(): # 'space'
				last_processed_type = 'space'
			else:
				raise GCodeObject.GCodeSyntaxError \
					('The file contains unsupported character.')

	return tuple(result_list)