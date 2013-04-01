# Python imports
import os
import re
import fnmatch

from funky import first, arglist


# Path filters
def path_filter_visible(path, abspath):
    return True


def path_filter_file(path, abspath):
    return os.path.isfile(abspath)


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
