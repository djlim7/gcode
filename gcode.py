import argparse
import GCode_object

parser_obj = argparse.ArgumentParser()
parser_obj.add_argument('input_file', nargs = '?')
parser_args = parser_obj.parse_args()

if __name__ == "__main__":
	print(parser_args.input_file)