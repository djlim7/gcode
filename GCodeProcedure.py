"""GCode Procedure"""

import string

try:
    from . import GCodeObject
except SystemError:
    import GCodeObject

class GCodeParser:
    """Parse the GCode into tuple with elements."""
    process_string = None

    def __init__(self, process_string):
        self.process_string = process_string

    def parse_syntax(self):
        """Parse the syntax, form text file to Python tuple."""
        main_loop = True
        idx = 0
        result_list = []
        last_processed_type = 'space'
        # 'str', 'int', 'space', 'minus', 'dot', '%'
        while main_loop:
            # Check EOF
            if idx == len(self.process_string):
                character = ' '
                main_loop = False
            else:
                character = self.process_string[idx]

            # 'str'
            if character in string.ascii_letters:
                result_list.append(character.upper())
                last_processed_type = 'str'
            # 'int'
            elif character.isdigit():
                if last_processed_type == 'str':
                    result_list.append(float(character))
                elif last_processed_type == 'int':
                    result_list[-1] = float(result_list[-1]) * 10 + float(character)
                elif last_processed_type == 'space':
                    result_list.append(float(character))
                last_processed_type = 'int'
            # 'space'
            elif character.isspace():
                last_processed_type = 'space'
            else:
                raise GCodeObject.GCodeSyntaxError \
                    ('The file contains unsupported character.')

            idx += 1

        return tuple(result_list)
