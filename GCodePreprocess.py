import functools
import GCodeObject

def custom_coroutine_wrapper(func):
	@functools.wraps(func)
	def init(*args, **kwargs):
		cr_obj = func(*args, **kwargs)
		next(cr_obj)
		return cr_obj
	return init

@custom_coroutine_wrapper
def GCodePreprocessor():
	input_list = list()
	process_status = 'r' # b -> p -> i
	process_result = None
	while True:
		input_char = (yield process_result)
		if input_char.isalpha():
			if process_status == 'b':
				process_status = 'p'
				input_list.append(input_char)
		if input_char.isdigit():
			if process_status == 'p':
				process_status = 'i'
				input_list.append(input_char)
		if input_char.isspace():
			if process_status == 'i':
				process_status = 'b'
				print(input_list)