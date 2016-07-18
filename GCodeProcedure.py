import os
import string
from . import GCodeObject

def ParseSyntax(process_string):
	"Parse the syntax, form text file to Python tuple."
	result_list = []
	main_loop = True
	idx = 0
	last_processed_type = 'space' # 'str', 'float', 'space', 'minus', 'dot'
	while main_loop:
		if idx == len(process_string):
				character = ' '
				main_loop = False
		else:
			character = process_string[idx]

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

		idx += 1

	return tuple(result_list)