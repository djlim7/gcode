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
def GCodeParser():
	process_status = 'p' # 'p'refix -> 'i'ntegar -> 'r'esult
	process_result = ['', 0]

	while True:
		input_char = (yield process_result)

		if input_char.isalpha():
			if process_status == 'p':
				process_result[0] = input_char
				process_status = 'i'
		elif input_char.isdigit():
			if process_status == 'i':
				process_result[1] = process_result[1] * 10 + int(input_char)
				pass