'''A main logic for Raspberry Pi with GPIO(gpiozero).'''

import argparse
import GCodeObject
import GCodeProcedure

# Parse the arguments
parser_obj = argparse.ArgumentParser()
parser_obj.add_argument('input_file', type = str ,nargs = '?')
parser_arg = parser_obj.parse_args()

# Process
with open(parser_arg.input_file, 'r') as file_stream:
	s = file_stream.read()

element_tuple = GCodeObject.GCodeElementHandler(GCodeProcedure.ParseSyntax(s))
element_tuple.ValidateGrammer()