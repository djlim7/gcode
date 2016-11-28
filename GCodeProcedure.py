"""GCode Procedure"""

import string

try:
    from . import GCodeObject
except SystemError:
    import GCodeObject

class GCodeParser:
    """Parse the GCode into tuple with elements."""
    # 'char', 'int', 'space', '-', '.', '%', '(', ')', "'", '"'
    process_string = None

    def __str__(self):
        print(self.process_string)

    def __init__(self, process_string):
        self.process_string = process_string
    def lexical_parse(self):
        """Lexical parse, form text file to Python tuple."""
        main_loop = True
        idx = 0
        result_list = []
        last_processed_type = 'space'
        # Replacement form newline('\n'') to '%''
        process_string = self.process_string.replace('\n', '%')
        while main_loop:
            # Check EOF
            if idx == len(process_string):
                character = ' '
                main_loop = False
            else:
                character = process_string[idx]

            # 'char'
            if character in string.ascii_letters:
                result_list.append(character.upper())
                last_processed_type = 'char'
            # 'int'
            elif character.isdigit():
                if last_processed_type == 'int':
                    result_list[-1] = int(result_list[-1]) * 10 + int(character)
                else:
                    result_list.append(int(character))
                last_processed_type = 'int'
            # 'space'
            elif character.isspace():
                last_processed_type = 'space'
            # '-'
            elif character == '-':
                result_list.append(character)
                last_processed_type = '-'
            # '.', '%', '(', ')', "'", '"'
            elif character == '.' or '%' or '(' or ')' or "'" or '"':
                result_list.append(character)
                last_processed_type = character
            else:
                raise GCodeObject.GCodeSyntaxError \
                    ('The file contains unsupported character: {}'.format(character))

            idx += 1

        return tuple(result_list)
