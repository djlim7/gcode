import functools
import string
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
	process_list_initial = ['', 0]
	process_list = process_list_initial[:]
	process_result = None

	while True:
		input_char = (yield process_result).upper()

		if process_status == 'r':
			process_list = process_list_initial[:]
			process_result = None
			process_status = 'p'

		if input_char in string.ascii_letters:
			if process_status == 'p':
				process_list[0] = input_char
				process_status = 'i'
			elif process_status == 'i':
				process_status = 'r'
		elif input_char.isdigit():
			if process_status == 'p':
				raise GCodeObject.GCodeSyntaxError()
			elif process_status == 'i':
				process_list[1] = process_list[1] * 10 + int(input_char)
		elif input_char.isspace():
			if process_status == 'p':
				pass
			elif process_status == 'i':
				process_status = 'r'
		else:
			raise GCodeObject.GCodeSyntaxError()

		if process_status == 'r':
			process_result = process_list[:]