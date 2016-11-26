"""GCode Objects"""

import functools

def custom_coroutine_wrapper(func):
    """Initialzie automatically."""
    @functools.wraps(func)
    def init(*args, **kwargs):
        """Initialize wrapper"""
        cr_obj = func(*args, **kwargs)
        next(cr_obj)
        return cr_obj
    return init

class GCodeElementBase:
    "G-code element base"
    element = None
    def __init__(self, element=None):
        self.element = element
    def __str__(self):
        return self.element

class GCodeParserElementBase(GCodeElementBase):
    """G-code parser element base"""
    def __repr__(self):
        return '(GCodeParserElementBase: {})'.format(repr(self.element))

class GCodeParserChar(GCodeParserElementBase):
    """G-code parser char element"""
    def __repr__(self):
        return '(GCodeParserChar: {})'.format(repr(self.element))

class GCodeParserInt(GCodeParserElementBase):
    """G-code parser int element"""
    def __repr__(self):
        return '(GCodeParserInt: {})'.format(repr(self.element))

class GCodeParserSpace(GCodeParserElementBase):
    """G-code parser space element"""
    def __repr__(self):
        return '(GCodeParserSpace: {})'.format(repr(self.element))

class GCodeParserMinus(GCodeParserElementBase):
    """G-code parser minus element"""
    def __repr__(self):
        return '(GCodeParserMinus: {})'.format(repr(self.element))

class GCodeParserBracketBase(GCodeParserElementBase):
    """G-code parser bracket base"""
    def __repr__(self):
        return '(GCodeParserBracketBase: {})'.format(repr(self.element))

class GCodeParserBracketLeft(GCodeParserBracketBase):
    """G-code parser left bracket element"""
    def __repr__(self):
        return '(GCodeParserBracketLeft: {})'.format(repr(self.element))

class GCodeParserBracketRight(GCodeParserBracketBase):
    """G-code parser right bracket element"""
    def __repr__(self):
        return '(GCodeParserBracketRight: {})'.format(repr(self.element))

class GCodeParserSpecialCharacter(GCodeParserElementBase):
    """G-code parser special element"""
    def __repr__(self):
        return '(GCodeParserSpecialCharacter: {})'.format(repr(self.element))

class GCodePrefixBase(GCodeElementBase):
    """G-code prefix"""
    def __repr__(self):
        return '(GCodePrefix: {})'.format(repr(self.element))

class GCodePrefixChar(GCodePrefixBase):
    """G-code prefix with character"""
    def __repr__(self):
        return '(GCodePrefixChar: {})'.format(repr(self.element))

class GCodePrefixInt(GCodePrefixBase):
    """G-code prefix with integer"""
    def __repr__(self):
        return '(GCodePrefixInt: {})'.format(repr(self.element))

class GCodePostfixFloat(GCodeElementBase):
    "G-code float"
    def __repr__(self):
        return '(GCodeFloat: {})'.format(repr(self.element))

class GCode:
    "G-code object"
    prefix_char = GCodePrefixChar('')
    prefix_int = GCodePrefixInt(0)
    postfix_float = GCodePostfixFloat(0)
    def __init__(self, prefix_char, prefix_int, postfix_float):
        self.prefix_char = prefix_char
        self.prefix_int = prefix_int
        self.postfix_float = postfix_float
    def __str__(self):
        return '{}{}{}'.format(str(self.prefix_char), str(self.prefix_int), str(self.postfix_float))
    def __repr__(self):
        return '(GCode: {}, {}, {})'.format(repr(self.prefix_char), \
                repr(self.prefix_int), repr(self.postfix_float))

class GCodeElementHandler:
    "Handler of G-code elements"
    memeber_tuple = None
    def __init__(self, builtin_element_tuple):
        temporary_list = list()
        for indic in builtin_element_tuple:
            if isinstance(indic, str):
                temporary_list.append(GCodePrefixChar(indic))
            elif isinstance(indic, float):
                temporary_list.append(GCodePostfixFloat(indic))
            elif isinstance(indic, GCodePrefixChar) or isinstance(indic, GCodePostfixFloat):
                temporary_list.append(indic)
        self.memeber_tuple = tuple(temporary_list)
    def __repr__(self):
        return '(GCodeElementHandler: {})'.format(self.memeber_tuple)
    def validate_grammer(self):
        """Validate Grammer"""
        last_processed_type = type(GCodePostfixFloat())
        for indic in self.memeber_tuple:
            if isinstance(indic, last_processed_type):
                raise GCodeSyntaxError('Check whether prefix and float comes alternately.')
            else:
                last_processed_type = type(indic)

        # Check whether last_processed_type is GCodePrefix
        if last_processed_type == type(GCodePrefixChar()):
            raise GCodeSyntaxError('G-code ends with prefix.')

        return True
    def bind_to_gcode(self):
        """Bind to GCode"""
        self.validate_grammer()
        result_list = list()
        buf = None
        odd = True
        for indic in self.memeber_tuple:
            if odd:
                buf = indic
                odd = False
            else:
                result_list.append(GCode(buf, None, indic))
                odd = True
        return tuple(result_list)

class GCodeException(Exception):
    "Basic exception class for G-code handling"
    pass

class GCodeSyntaxError(GCodeException):
    "G-code Syntax Error"
    pass
