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

    # Flatten iterables
    # ['x', 'y'], ...
    if arg_type == list:
        flattened_args = sum(args, [])
        return flattened_args
    elif arg_type == tuple:
        flattened_args = sum(args, ())
        return flattened_args

    # Flatten set
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


class Memoizer(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def cache_key(self, args, kwargs):
        sorted_kwargs = kwargs.items()
        sorted_kwargs.sort()
        cache_key = hash(args + tuple(sorted_kwargs))
        return cache_key

    def has_cache(self, cache_key):
        return cache_key in self.cache

    def get_cache(self, cache_key):
        return self.cache[cache_key]

    def set_cache(self, cache_key, value):
        self.cache[cache_key] = value

    def clear(self):
        self.cache = {}

    def __call__(self, *args, **kwargs):
        cache_key = self.cache_key(args, kwargs)
        if not self.has_cache(cache_key):
            value = self.func(*args, **kwargs)
            self.set_cache(cache_key, value)
        return self.get_cache(cache_key)


# Cache calls
def memoize(func):
    """Cache a functions output for a given set of arguments"""
    return wraps(func)(Memoizer(func))


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
        p[2:] if p.startswith('./') else p
        for p in paths
    ]


def dir_subpaths(root_path):
    """Get paths in a given directory"""
    paths = []
    for dirname, dirnames, filenames in os.walk(root_path):

        # Add directory paths
        abs_dirnames = [
            os.path.join(dirname, subdirname)
            for subdirname in dirnames
        ]
        rel_dirnames = [
            os.path.relpath(abs_dirname, root_path)
            for abs_dirname in abs_dirnames
        ]
        paths.extend(zip(
            rel_dirnames,
            abs_dirnames,
        ))

        abs_filenames = [
            os.path.join(dirname, filename)
            for filename in filenames
        ]
        rel_filenames = [
            os.path.relpath(abs_filename, root_path)
            for abs_filename in abs_filenames
        ]
        paths.extend(zip(
            rel_filenames,
            abs_filenames,
        ))

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
    relative_filtered_paths = map(first, filtered_paths)
    return clean_relative_paths(relative_filtered_paths)


@arglist
def globers_to_regex(globers):
    return map(fnmatch.translate, globers)


def true_only(iterable):
    return filter(bool, iterable)


def first_true(iterable):
    true_values = true_only(iterable)
    if true_values:
        return true_values[0]
    return None
