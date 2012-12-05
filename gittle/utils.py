# Python imports
from functools import wraps

# Constants
LIST_TYPES = (list, tuple, set)


def list_from_args(args):
    """
    Flatten list of args
    So as to accept either an array
    Or as many arguments
    For example:
    func(['x', 'y'])
    func('x', 'y')
    """
    # Empty args
    if not args:
        return []

    # Get argument type
    arg_type = type(args[0])
    is_list = arg_type in LIST_TYPES

    # Check that the arguments are uniforn (of same type)
    same_type = all([
        isinstance(arg, arg_type)
        for arg in args
    ])

    if not same_type:
        raise Exception('Expected uniform arguments of same type !')

    # ['x', 'y'], ...
    if is_list:
        flattened_args = sum(args, [])
        return flattened_args

    # 'x', 'y'
    return list(args)


# Decorator for list_from_args
def arglist(func):
    @wraps(func)
    def f(*args, **kwargs):
        args_list = list_from_args(args)
        return func(args_list, **kwargs)
    return f


# Decorator for methods
def arglist_method(func):
    @wraps(func)
    def f(self, *args, **kwargs):
        print('ARGS', args)
        args_list = list_from_args(args)
        print('ARGS LIST', args_list)
        return func(self, args_list, **kwargs)
    return f
