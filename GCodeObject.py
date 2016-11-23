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
    "G-code element"
    element = None
    def __init__(self, element=None):
        self.element = element
    def __str__(self):
        return self.element

class GCodePrefix(GCodeElementBase):
    "G-code prefix"
    def __repr__(self):
        return '(GCodePrefix: {})'.format(repr(self.element))

class GCodeFloat(GCodeElementBase):
    "G-code float"
    def __repr__(self):
        return '(GCodeFloat: {})'.format(repr(self.element))

class GCodeElementHandler:
    "Handler of G-code elements"
    memeber_tuple = None
    def __init__(self, builtin_element_tuple):
        temporary_list = list()
        for indic in builtin_element_tuple:
            if isinstance(indic, str):
                temporary_list.append(GCodePrefix(indic))
            elif isinstance(indic, float):
                temporary_list.append(GCodeFloat(indic))
            elif isinstance(indic, GCodePrefix) or isinstance(indic, GCodeFloat):
                temporary_list.append(indic)
        self.memeber_tuple = tuple(temporary_list)
    def __repr__(self):
        return '(GCodeElementHandler: {})'.format(self.memeber_tuple)
    def validate_grammer(self):
        """Validate Grammer"""
        last_processed_type = type(GCodeFloat())
        for indic in self.memeber_tuple:
            if isinstance(indic, last_processed_type):
                raise GCodeSyntaxError('Check whether prefix and float comes alternately.')
            else:
                last_processed_type = type(indic)

        # Check whether last_processed_type is GCodePrefix
        if last_processed_type == type(GCodePrefix()):
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
                result_list.append(GCode(buf, indic))
                odd = True
        return tuple(result_list)

class GCode:
    "G-code object"
    prefix = GCodePrefix('')
    number = GCodeFloat(0)
    def __init__(self, prefix, number):
        self.prefix = prefix
        self.number = number
    def __str__(self):
        return '{}{}'.format(str(self.prefix), str(self.number))
    def __repr__(self):
        return '(GCode: {}, {})'.format(repr(self.prefix), repr(self.number))

class GCodeException(Exception):
    "Basic exception class for G-code handling"
    pass

class GCodeSyntaxError(GCodeException):
    "G-code Syntax Error"
    pass
