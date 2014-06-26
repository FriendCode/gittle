# Python imports
import os
from StringIO import StringIO
from functools import partial

# Dulwich imports
from dulwich import patch
from dulwich.objects import Blob
from dulwich.patch import is_binary

# Funky imports
from funky import first, true_only, rest, negate, transform


def is_readable(store):
    def fn(info):
        path, mode, sha = info
        return path is None or (type(store[sha]) is Blob and not is_binary(store[sha].data))
    return fn

def is_readable_change(store):
    def fn(change):
        return all(
            map(is_readable(store), change)
        )
    return fn

def is_unreadable_change(store):
    return negate(is_readable_change(store))

def dummy_diff(*args, **kwargs):
    return ''


def commit_name_email(commit_author):
    try:
        name, email = commit_author.rsplit(' ', 1)
        # Extract the X from : "<X>"
        email = email[1:-1]
    except:
        name = commit_author
        email = ''
    return name, email


def contributor_from_raw(raw_author):
    name, email = commit_name_email(raw_author)
    return {
        'name': name,
        'email': email,
        'raw': raw_author
    }


def commit_info(commit):
    author = contributor_from_raw(commit.author)
    committer = contributor_from_raw(commit.committer)

    message_lines = commit.message.splitlines()
    summary = first(message_lines, '')
    description = '\n'.join(
        true_only(
            rest(
                message_lines
            )
        )
    )

    return {
        'author': author,
        'committer': committer,
        'sha': commit.sha().hexdigest(),
        'time': commit.commit_time,
        'timezone': commit.commit_timezone,
        'message': commit.message,
        'summary': summary,
        'description': description,
    }


def object_diff(*args, **kwargs):
    """A more convenient wrapper around Dulwich's patching
    """
    fd = StringIO()
    patch.write_object_diff(fd, *args, **kwargs)
    return fd.getvalue()


def blob_diff(object_store, *args, **kwargs):
    fd = StringIO()
    patch.write_blob_diff(fd, *args, **kwargs)
    return fd.getvalue()


def changes_to_pairs(changes):
    return [
        ((oldpath, oldmode, oldsha), (newpath, newmode, newsha),)
        for (oldpath, newpath), (oldmode, newmode), (oldsha, newsha) in changes
    ]


def _diff_pairs(object_store, pairs, diff_func, diff_type='text'):
    for old, new in pairs:
        yield { 'diff': diff_func(object_store, old, new),
                'new': change_to_dict(new),
                'old': change_to_dict(old),
                'type': diff_type }


def diff_changes(object_store, changes, diff_func=object_diff, filter_binary=True):
    """Return a dict of diffs for the changes
    """
    pairs = changes_to_pairs(changes)
    readable_pairs = filter(is_readable_change(object_store), pairs)
    unreadable_pairs = filter(is_unreadable_change(object_store), pairs)

    for x in _diff_pairs(object_store, readable_pairs, diff_func):
        yield x
    for x in _diff_pairs(object_store, unreadable_pairs, dummy_diff, 'binary'):
        yield x


def obj_blob(object_store, info):
    if not any(info):
        return info
    path, mode, sha = info
    return (path, mode, object_store[sha])


def path_blob(basepath, info):
    if not any(info):
        return info
    path, mode, sha = info
    return blob_from_path(basepath, path)


def changes_to_blobs(object_store, basepath, pairs):
    return [
        (obj_blob(object_store, old), path_blob(basepath, new),)
        for old, new in pairs
    ]


def change_to_dict(info):
    path, mode, sha_or_blob = info

    if sha_or_blob and not is_sha(sha_or_blob):
        sha = sha_or_blob.id
    else:
        sha = sha_or_blob

    return {
        'path': path,
        'mode': mode,
        'sha': sha,
    }


def diff_changes_paths(object_store, basepath, changes, filter_binary=True):
    """Does a diff assuming that the old blobs are in git and others are unstaged blobs
       in the working directory
    """
    pairs = changes_to_pairs(changes)
    readable_pairs = filter(is_readable_change(object_store), pairs)
    unreadable_pairs = filter(is_unreadable_change(object_store), pairs)

    blobs = changes_to_blobs(object_store, basepath, readable_pairs)

    for x in _diff_pairs(object_store, blobs, blob_diff):
        yield x
    for x in _diff_pairs(object_store, unreadable_pairs, dummy_diff, 'binary'):
        yield x


def changes_tree_diff(object_store, old_tree, new_tree):
    return object_store.tree_changes(old_tree, new_tree)


def dict_tree_diff(object_store, old_tree, new_tree, filter_binary=True):
    """Returns a dictionary where the keys are the filenames and their respective
    values are their diffs
    """
    changes = changes_tree_diff(object_store, old_tree, new_tree)
    return diff_changes(object_store, changes, filter_binary=filter_binary)


def classic_tree_diff(object_store, old_tree, new_tree, filter_binary=None):
    """Does a classic diff and returns the output in a buffer
    """
    output = StringIO()

    # Write to output (our string)
    patch.write_tree_diff(
        output,
        object_store,
        old_tree,
        new_tree
    )

    return output.getvalue()


def prune_tree(tree, paths):
    """Return a tree with only entries matching the list of paths supplied
    """
    raise NotImplemented()


def is_sha(sha):
    return isinstance(sha, basestring) and len(sha) == 40


def blob_from_path(basepath, path):
    """Returns a tuple of (sha_id, mode, blob)
    """
    fullpath = os.path.join(basepath, path)
    with open(fullpath, 'rb') as working_file:
        blob = Blob()
        blob.data = working_file.read()
    return (path, os.stat(fullpath).st_mode, blob)


def subkey(base, refkey):
    if not refkey.startswith(base):
        return None
    base_len = len(base) + 1
    return refkey[base_len:]


def subrefs(refs_dict, base):
    """Return the contents of this container as a dictionary.
    """
    base = base or ''
    keys = refs_dict.keys()
    subkeys = map(
        partial(subkey, base),
        keys
    )
    key_pairs = zip(keys, subkeys)

    return {
        newkey: refs_dict[oldkey]
        for oldkey, newkey in key_pairs
        if newkey
    }


def clean_refs(refs):
    return {
        ref: sha
        for ref, sha in refs.items()
        if not ref.endswith('^{}')
    }
