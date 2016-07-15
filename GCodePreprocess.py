import string
import GCodeObject

@GCodeObject.CustomCoroutineWrapper
def GCodeParser():
	#
	#                   --- < ---
	#                   |        |
	# process_head --> 'p'refix  |
	#                   |        |
	#                  'i'ntegar |
	#                   |        |
	# process_tail --> 'r'esult  |
	#                   |        |
	#                   --- > ---
	#
	process_head = 'p'
	process_tail = 'r'
	process_list_initial = ['', 0]
	process_list = process_list_initial[:]
	process_result = None

	while True:
		#
		#    process_head: |    'p'    |    'i'    |    'r'
		# process_tail:
		#    ---
		#    'p'
		#    ---
		#    'i'
		#    ---
		#    'r'
		#
		#
		#
		#

		# Pre-process the 'r' head
		if process_head == 'r':
			process_result = process_list[:]

		input_char = (yield process_result).upper()

		# Post-process the 'r' head
		if process_head == 'r':
			process_list = process_list_initial[:]
			process_result = None
			process_head = 'p'
			process_tail = 'r'

		if input_char in string.ascii_letters:
			if process_head == 'p':
				if process_tail == 'p':
					pass
				if process_tail == 'i':
					pass
				if process_tail == 'r':
					pass
			elif process_head == 'i':
				if process_tail == 'p':
					pass
				if process_tail == 'i':
					pass
				if process_tail == 'r':
					pass
			elif process_head == 'r':
				if process_tail == 'p':
					pass
				if process_tail == 'i':
					pass
				if process_tail == 'r':
					pass
		elif input_char.isdigit():
			if process_head == 'p':
				if process_tail == 'p':
					pass
				if process_tail == 'i':
					pass
				if process_tail == 'r':
					pass
			elif process_head == 'i':
				if process_tail == 'p':
					pass
				if process_tail == 'i':
					pass
				if process_tail == 'r':
					pass
			elif process_head == 'r':
				if process_tail == 'p':
					pass
				if process_tail == 'i':
					pass
				if process_tail == 'r':
					pass
		elif input_char.isspace():
			if process_head == 'p':
				if process_tail == 'p':
					pass
				if process_tail == 'i':
					pass
				if process_tail == 'r':
					pass
			elif process_head == 'i':
				if process_tail == 'p':
					pass
				if process_tail == 'i':
					pass
				if process_tail == 'r':
					pass
			elif process_head == 'r':
				if process_tail == 'p':
					pass
				if process_tail == 'i':
					pass
				if process_tail == 'r':
					pass
		else:
			raise GCodeObject.GCodeSyntaxError()