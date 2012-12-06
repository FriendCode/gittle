# Python imports
import os
import re
import fnmatch
import operator
from functools import wraps

# Constants
LIST_TYPES = (list, tuple, set)


def first(iterable):
    return iterable[0]


def last(iterable):
    return iterable[-1]


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
        args_list = list_from_args(args)
        return func(self, args_list, **kwargs)
    return f


# Cache calls
def memoize(func):
    """Cache a functions output for a given set of arguments"""
    cache = {}

    @wraps(func)
    def f(*args, **kwargs):
        sorted_kwargs = kwargs.items()
        sorted_kwargs.sort()
        cache_key = hash(args + tuple(sorted_kwargs))
        if cache_key in cache:
            return cache[cache_key]
        cache[cache_key] = func(*args, **kwargs)
        return cache[cache_key]
    return f


def transform(transform_func):
    """Apply a transformation to a functions return value"""
    def decorator(func):
        @wraps(func)
        def f(*args, **kwargs):
            return transform_func(
                func(*args, **kwargs)
            )
        return f
    return decorator


# Useful functions
negate = transform(operator.not_)


# Path filters
def path_filter_hidden(path, abspath):
    return path.startswith('.')

path_filter_visible = negate(path_filter_hidden)


def path_filter_directory(path, abspath):
    return os.path.isdir(abspath)

path_filter_file = negate(path_filter_directory)


@arglist
def path_filter_regex(regexes):
    compiled_regexes = map(re.compile, regexes)

    def _filter(path, abspath):
        return any([
            cre.match(abspath)
            for cre in compiled_regexes
        ])
    return _filter


@arglist
def combine_filters(filters):
    def combined_filter(path, abspath):
        filter_results = [
            _filter(path, abspath)
            for _filter in filters
        ]
        return all(filter_results)
    return combined_filter


def abspaths_only(paths_couple):
    return map(lambda x: x[1], paths_couple)


def clean_relative_paths(paths):
    return [
        p[2:]
        for p in paths
    ]


def dir_subpaths(root_path):
    """Get paths in a given directory"""
    paths = []
    for dirname, dirnames, filenames in os.walk(root_path):

        # Add directory paths
        paths.extend([
            # path, abspath
            (subdirname, os.path.join(dirname, subdirname))
            for subdirname in dirnames
        ])

        # Add file paths
        paths.extend([
            # path, abspath
            (filename, os.path.join(dirname, filename))
            for filename in filenames
        ])
    return paths


def subpaths(root_path, filters=None):
    if filters is None:
        filters = [
            path_filter_visible,
            path_filter_file,
        ]

    # One big filter which combines all other smaller filters
    big_filter = combine_filters(filters)
    filter_func = lambda x: big_filter(x[0], x[1])

    paths = dir_subpaths(root_path)

    # Do filtering
    filtered_paths = filter(filter_func, paths)
    abs_filtered_paths = abspaths_only(filtered_paths)
    return clean_relative_paths(abs_filtered_paths)


@arglist
def globers_to_regex(globers):
    return map(fnmatch.translate, globers)
