'''A main logic for Raspberry Pi with GPIO(gpiozero).'''

import argparse
import GCodeObject

# Parse the arguments
parser_obj = argparse.ArgumentParser()
parser_obj.add_argument('input_file', type = str ,nargs = '?')
parser_arg = parser_obj.parse_args()

# Load the input_file
if parser_arg.input_file != None:
	main_file = open(parser_arg.input_file, 'r')

# Process
main_loop = True
while main_loop:
	print(GCodeObject.GCodeX(100))
	main_loop = False

# Close the process
if parser_arg.input_file != None:
	main_file.close()