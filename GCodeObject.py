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

# G-code element base class
class GCodeElementBase:
    "G-code element base"
    element = None
    def __init__(self, element=None):
        self.element = element
    def __str__(self):
        return self.element

# G-code parser elements
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

# G-code result elements
class GCodeResultElementBase(GCodeElementBase):
    """G-code result element base"""
    def __repr__(self):
        return '(GCodeResultElementBase: {})'.format(repr(self.element))

class GCodePrefix(GCodeResultElementBase):
    """G-code prefix element"""
    def __repr__(self):
        return '(GCodePrefix: {})'.format(repr(self.element))

class GCodeFloat(GCodeResultElementBase):
    """G-code float element"""
    def __repr__(self):
        return '(GCodeFloat: {})'.format(repr(self.element))

class GCode:
    "G-code object"
    element_prefix = GCodePrefix('')
    element_float = GCodeFloat(None)
    def __init__(self, element_prefix, element_float):
        self.element_prefix = element_prefix
        self.element_float = element_float
    def __str__(self):
        return '{}{}'.format(str(self.element_prefix), str(self.element_float))
    def __repr__(self):
        return '(GCode: {}, {})'.format(repr(self.element_prefix), repr(self.element_float))

class GCodeException(Exception):
    "Basic exception class for G-code handling"
    pass

class GCodeSyntaxError(GCodeException):
    "G-code Syntax Error"
    pass
