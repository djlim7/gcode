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
    def __repr__(self):
        return '({}: {})'.format(self.__class__.__name__, repr(self.element))

# G-code parser elements
class GCodeParserElementBase(GCodeElementBase):
    """G-code parser element base"""
    pass

class GCodeParserChar(GCodeParserElementBase):
    """G-code parser char element"""
    pass

class GCodeParserInt(GCodeParserElementBase):
    """G-code parser int element"""
    def __int__(self):
        return self.element

class GCodeParserSpace(GCodeParserElementBase):
    """G-code parser space element"""
    pass

class GCodeParserMinus(GCodeParserElementBase):
    """G-code parser minus element"""
    pass

class GCodeParserDot(GCodeParserElementBase):
    """G-code parser dot element"""
    pass

class GCodeParserBracketBase(GCodeParserElementBase):
    """G-code parser bracket base"""
    pass

class GCodeParserBracketLeft(GCodeParserBracketBase):
    """G-code parser left bracket element"""
    pass

class GCodeParserBracketRight(GCodeParserBracketBase):
    """G-code parser right bracket element"""
    pass

class GCodeParserSpecialCharacter(GCodeParserElementBase):
    """G-code parser special element"""
    pass

# G-code result elements
class GCodeResultElementBase(GCodeElementBase):
    """G-code result element base"""
    pass

class GCodePrefix(GCodeResultElementBase):
    """G-code prefix element"""
    pass

class GCodeInt(GCodeResultElementBase):
    """G-code inteagr element"""
    def __int__(self):
        return self.element

class GCodeFloat(GCodeResultElementBase):
    """G-code float element"""
    def __float__(self):
        return self.element

class GCode:
    "G-code object"
    element_prefix = None
    element_num = None
    def __init__(self, element_prefix, element_num):
        self.element_prefix = element_prefix
        self.element_num = element_num
    def __str__(self):
        return '{}{}'.format(str(self.element_prefix), str(self.element_num))
    def __repr__(self):
        return '({}: {}, {})'.format \
            (self.__class__.__name__, repr(self.element_prefix), repr(self.element_num))

class GCodeException(Exception):
    "Basic exception class for G-code handling"
    pass

class GCodeSyntaxError(GCodeException):
    "G-code Syntax Error"
    pass
