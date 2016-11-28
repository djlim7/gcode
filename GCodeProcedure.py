"""GCode Procedure"""

import string

try:
    from . import GCodeObject
except SystemError:
    import GCodeObject

class GCodeParser:
    """Parse the GCode into tuple with elements."""
    # 'char', 'int', 'space', '-', '.', '(', ')', '%', "'", '"'
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
        last_processed_type = GCodeObject.GCodeParserSpace
        # Replacement form newline('\n'') to '%''
        process_string = self.process_string.replace('\n', '%')
        while main_loop:
            # Check EOF and use space
            if idx == len(process_string):
                character = ' '
                main_loop = False
            else:
                character = process_string[idx]

            # 'char'
            if character in string.ascii_letters:
                result_list.append(GCodeObject.GCodeParserChar(character.upper()))
                last_processed_type = GCodeObject.GCodeParserChar
            # 'int'
            elif character.isdigit():
                if last_processed_type == GCodeObject.GCodeParserInt:
                    result_list[-1] = GCodeObject.GCodeParserInt \
                        (int(result_list[-1]) * 10 + int(character))
                else:
                    result_list.append(GCodeObject.GCodeParserInt(int(character)))
                last_processed_type = GCodeObject.GCodeParserInt
            # 'space'
            elif character.isspace():
                last_processed_type = GCodeObject.GCodeParserSpace
            # '-'
            elif character == '-':
                result_list.append(GCodeObject.GCodeParserMinus(character))
                last_processed_type = GCodeObject.GCodeParserMinus
            # '.'
            elif character == '.':
                result_list.append(GCodeObject.GCodeParserDot(character))
                last_processed_type = GCodeObject.GCodeParserDot
            # '('
            elif character == '(':
                result_list.append(GCodeObject.GCodeParserBracketLeft(character))
                last_processed_type = GCodeObject.GCodeParserBracketLeft
            # ')'
            elif character == ')':
                result_list.append(GCodeObject.GCodeParserBracketRight(character))
                last_processed_type = GCodeObject.GCodeParserBracketRight
            # '%', "'", '"'
            elif character == '%' or  "'" or '"':
                result_list.append(GCodeObject.GCodeParserSpecialCharacter(character))
                last_processed_type = GCodeObject.GCodeParserSpecialCharacter
            else:
                raise GCodeObject.GCodeSyntaxError \
                    ('The file contains unsupported character: {}'.format(character))

            idx += 1

        return tuple(result_list)
