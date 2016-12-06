"""GCode Procedure"""

import decimal
import math
import string

try:
    from . import GCodeObject
except SystemError:
    import GCodeObject

class GCodeParser:
    """Parse the GCode into tuple with elements.

Overview:
This class handle str and convert it into GCodeObject.GCode.

Example:
'X-12.0056'
    * lexical_parse()
(GCodeObject.GCodeParserChar('X'), GCodeObject.GCodeParserMinus('-'), \
GCodeObject.GCodeParserInt(12), GCodeObject.GCodeParserDot('.'), \
GCodeObject.GCodeParserDigitAfterDot(2), GCodeObject.GCodeParserInt(56))
    * trim_comment_and_specials()
    * bind_float()
(GCodeObject.GCodeParserChar('X'), GCodeObject.GCodeParserFloat(12.0056))
    * bind_to_gcode()
(GCodeObject.GCode(GCodeObject.GCodeChar('x'), GCodeObject.GCodeInt(12.0056)))

Supported characters:
'char', 'int', 'space', '-', '.', '(', ')', '%', "'", '"'"""
    string_original = str()
    list_lexical_parse = list()
    list_trim_comment_and_specials = list()
    list_bind_float = list()
    list_bind_to_gcode = list()

    def __init__(self, string_process):
        self.string_original = string_process

    def run(self):
        """Run all the GCodeParser's methods"""
        self.lexical_parse()
        self.trim_comment_and_specials()
        self.bind_float()
        self.bind_to_gcode()
        return tuple(self.list_bind_to_gcode)

    def lexical_parse(self):
        # pylint: disable=too-many-branches
        """Lexical parse, form text file to Python tuple.

Notice:
lexical_parse doesn't collect zero(0)s located after dot(.).
The zero(0)s are binded at bind_float()."""
        main_loop = True
        idx = int()
        result_list = list()
        last_processed_type = GCodeObject.GCodeParserSpace
        # Replacement form newline('\n') to '%'
        held_string = self.string_original.replace('\n', '%')
        while main_loop:
            # Check EOF and replace character with space
            if idx == len(held_string):
                character = ' '
                main_loop = False
            else:
                character = held_string[idx]

            # 'char'
            if character in string.ascii_letters:
                result_list.append(GCodeObject.GCodeParserChar(character.upper()))
                last_processed_type = GCodeObject.GCodeParserChar
            # 'zero' after dot(.) or ordinary int
            elif character.isdigit():
                if last_processed_type == GCodeObject.GCodeParserDot:
                    if character == '0':
                        result_list.append(GCodeObject.GCodeParserDigitAfterDot(1))
                        last_processed_type = GCodeObject.GCodeParserDigitAfterDot
                    else:
                        result_list.append(GCodeObject.GCodeParserInt(int(character)))
                        last_processed_type = GCodeObject.GCodeParserInt
                elif last_processed_type == GCodeObject.GCodeParserDigitAfterDot:
                    if character == '0':
                        result_list[-1].element += 1
                        last_processed_type = GCodeObject.GCodeParserDigitAfterDot
                    else:
                        result_list.append(GCodeObject.GCodeParserInt(int(character)))
                        last_processed_type = GCodeObject.GCodeParserInt
                elif last_processed_type == GCodeObject.GCodeParserInt:
                    result_list[-1] = GCodeObject.GCodeParserInt \
                                            (int(result_list[-1]) * 10 + int(character))
                    last_processed_type = GCodeObject.GCodeParserInt
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
                    ('The file contains unsupported character: {}, {}'.format(idx, character))

            idx += 1
        self.list_lexical_parse = result_list
        return tuple(result_list)

    def trim_comment_and_specials(self):
        """Trim the comment and special characters."""
        list_before = list(self.list_lexical_parse)
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

        if indent_level_head:
            raise GCodeObject.GCodeSyntaxError('Invalid comment wrapping indent level')

        self.list_trim_comment_and_specials = list_trimmed_twofold
        return tuple(list_trimmed_twofold)

    def bind_float(self):
        # pylint: disable=too-many-branches
        """Bind the floats"""
        list_before = self.list_trim_comment_and_specials
        list_result = list()
        list_location_dot = list()
        list_location_minus_valid = list()

        # Check dots' locations
        for index in range(0, len(list_before)):
            if isinstance(list_before[index], GCodeObject.GCodeParserDot):
                list_location_dot.append(index)

        # Check whether dot(.) is sealed with integars,
        # and whether minus(-) is valid.
        for index in list_location_dot:
            try:
                if isinstance(list_before[index - 1], GCodeObject.GCodeParserInt) and \
                    (isinstance(list_before[index + 1], GCodeObject.GCodeParserInt) or \
                        isinstance(list_before[index + 1], GCodeObject.GCodeParserDigitAfterDot)):
                    if isinstance(list_before[index - 2], GCodeObject.GCodeParserMinus):
                        list_location_minus_valid.append(index - 2)
                else:
                    raise GCodeObject.GCodeSyntaxError('Dot(.) is not sealed with integers')
            except IndexError:
                if index == 1:
                    continue
                elif index + 1 == len(list_before):
                    raise GCodeObject.GCodeSyntaxError('Dot(.) is located in EOF')

        # Bind
        for index in range(0, len(list_before)):
            index_log10 = 0
            spot_actual_number = 0
            calculated = decimal.Decimal(1)

            if not index - 1 in list_location_dot and \
                not index in list_location_dot and \
                not index + 1 in list_location_dot and \
                (False if isinstance(list_before[index], GCodeObject.GCodeParserInt) and \
                index - 2 in list_location_dot else True) and \
                not index in list_location_minus_valid:
                list_result.append(list_before[index])
            elif index in list_location_dot:
                spot_actual_number = (index + 2) if isinstance(list_before[index + 1], \
                                GCodeObject.GCodeParserDigitAfterDot) else (index + 1)
                try:
                    if spot_actual_number == index + 2:
                        index_log10 -= list_before[index + 1].element
                    while index_log10 < math.log10(list_before[spot_actual_number].element):
                        calculated = calculated * decimal.Decimal('0.1')
                        index_log10 += 1
                # log10(0) is undefined, so it raises ValueError.
                # So check and process the zero.
                except ValueError:
                    if list_before[spot_actual_number].element == 0:
                        calculated = decimal.Decimal(0)

                calculated = calculated * decimal.Decimal(list_before[spot_actual_number].element)
                calculated = list_before[index - 1].element + calculated

                if index - 2 in list_location_minus_valid:
                    calculated = -calculated
                list_result.append(GCodeObject.GCodeParserFloat(float(calculated)))

        # Find the unused GCodeObject objects
        for index in list_result:
            if isinstance(index, GCodeObject.GCodeParserMinus) or \
                isinstance(index, GCodeObject.GCodeParserDot):
                raise GCodeObject.GCodeSyntaxError('Check minus(-) or Dot(.)')

        self.list_bind_float = list_result
        return tuple(list_result)

    def bind_to_gcode(self):
        # pylint: disable=redefined-variable-type
        """Bind the list into G-code object"""
        list_before = self.list_bind_float
        odd = False
        tem_prefix = None
        tem_number = None
        list_result = list()

        for index in list_before:
            odd = not odd
            if odd and isinstance(index, GCodeObject.GCodeParserChar):
                tem_prefix = index
            elif not odd and isinstance(index, GCodeObject.GCodeParserNumberBase):
                if isinstance(index, GCodeObject.GCodeParserInt):
                    tem_number = GCodeObject.GCodeInt(index.element)
                else:
                    tem_number = GCodeObject.GCodeFloat(index.element)
                list_result.append(GCodeObject.GCode( \
                                    GCodeObject.GCodePrefix(tem_prefix.element), tem_number))
            else:
                raise GCodeObject.GCodeSyntaxError('Check the sequence of prefixes and numbers')

        self.list_bind_to_gcode = list_result
        return tuple(list_result)
