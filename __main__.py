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
main_coroutine = GCodePreprocess.GCodeParser()
process_lastmoment = False
while main_loop:
	# Read the file
	character = main_file.read(1)
	# Process the last letter
	if main_file.tell() == os.fstat(main_file.fileno()).st_size:
		if process_lastmoment:
			character = ' '
			main_loop = False
		else:
			# Process the last moment next time
			process_lastmoment = True

	# Preprocess
	imsi_result = main_coroutine.send(character)

	# Postprocess - exclusively for Raspberry Pi
	print(character, end = '')
	print(imsi_result)

# Close the process
if parser_arg.input_file != None:
	main_file.close()