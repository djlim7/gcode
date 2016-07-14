'''A main logic for Raspberry Pi with GPIO(gpiozero).'''

import argparse
import os
import GCodeObject
import GCodePreprocess

# Parse the arguments
parser_obj = argparse.ArgumentParser()
parser_obj.add_argument('input_file', type = str ,nargs = '?')
parser_arg = parser_obj.parse_args()

# Load the input_file
if parser_arg.input_file != None:
	main_file = open(parser_arg.input_file, 'r')

# Process
main_loop = True
main_coroutine = GCodePreprocess.GCodePreprocessor()
character_lastletter = False
while main_loop:
	# Read the file
	if parser_arg.input_file != None:
		character = main_file.read(1)
		# Process the last letter
		if main_file.tell() == os.fstat(main_file.fileno()).st_size:
			character_lastletter = True
			main_loop = False

	# Preprocess
	main_coroutine.send(character)

	# Postprocess - exclusively for Raspberry Pi
	print(character, end = '')

# Close the process
if parser_arg.input_file != None:
	main_file.close()