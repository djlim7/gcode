"""GCode Procedure"""

import string

try:
    from . import GCodeObject
except SystemError:
    import GCodeObject

class GCodeParser:
    """Parse the GCode into tuple with elements."""
    # 'char', 'int', 'space', '-', '.', '(', ')', '%', "'", '"'
    original_string = str()
    processed_list = tuple()

    def __init__(self, process_string):
        self.original_string = process_string

    def lexical_parse(self):
        """Lexical parse, form text file to Python tuple."""
        main_loop = True
        idx = 0
        result_list = []
        last_processed_type = GCodeObject.GCodeParserSpace
        # Replacement form newline('\n'') to '%'
        held_string = self.original_string.replace('\n', '%')
        while main_loop:
            # Check EOF and use space
            if idx == len(held_string):
                character = ' '
                main_loop = False
            else:
                character = held_string[idx]

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
        self.processed_list = tuple(result_list)
        return tuple(result_list)

    def trim_comment_and_specials(self):
        """Trim the comment and special characters."""
        list_before = list(self.processed_list)
        list_trimmed_specials = list()
        list_trimmed_twofold = list()

        # Eliminate special characters
        for piv in list_before:
            if isinstance(piv, GCodeObject.GCodeParserSpecialCharacter):
                continue
            else:
                list_trimmed_specials.append(piv)

        # Eliminate comments
        indent_level_head = 0
        indent_level_tail = 0
        for piv in list_trimmed_specials:
            if isinstance(piv, GCodeObject.GCodeParserBracketLeft):
                indent_level_head += 1
            elif isinstance(piv, GCodeObject.GCodeParserBracketRight):
                indent_level_head -= 1

            if indent_level_head == 0 and indent_level_tail == 0:
                list_trimmed_twofold.append(piv)

            # Check invalid indent level
            if indent_level_head < 0:
                raise GCodeObject.GCodeSyntaxError('Invalid comment wrapping')

            indent_level_tail = indent_level_head

        self.processed_list = list_trimmed_twofold
        return tuple(list_trimmed_twofold)
