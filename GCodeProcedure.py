"""GCode Procedure"""

import string
from . import GCodeObject

class GCodeParser:
    """Parse the GCode into tuple with elements."""
    process_string = None

    def __init__(self, process_string):
        self.process_string = process_string

    def parse_syntax(self):
        """Parse the syntax, form text file to Python tuple."""
        result_list = []
        main_loop = True
        idx = 0
        last_processed_type = 'space' # 'str', 'float', 'space', 'minus', 'dot'
        while main_loop:
            if idx == len(self.process_string):
                character = ' '
                main_loop = False
            else:
                character = self.process_string[idx]

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
