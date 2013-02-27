# Python imports
import os
from StringIO import StringIO

# Dulwich imports
from dulwich import patch
from dulwich.objects import Blob

# Funky imports
from funky import first, true_only, rest


def commit_name_email(commit_author):
    try:
        name, email = commit_author.rsplit(' ', 1)
        # Extract the X from : "<X>"
        email = email[1:-1]
    except:
        name = commit_author
        email = ''
    return name, email


def commit_info(commit):
    author_name, author_email = commit_name_email(commit.author)
    committer_name, committer_email = commit_name_email(commit.committer)

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
        'author': commit.author,
        'author_name': author_name,
        'author_email': author_email,
        'committer': commit.committer,
        'committer_name': committer_name,
        'committer_email': committer_email,
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
    print("Changes = %s" % changes)
    return [
        ((oldpath, oldmode, oldsha), (newpath, newmode, newsha),)
        for (oldpath, newpath), (oldmode, newmode), (oldsha, newsha) in changes
    ]


def diff_changes(object_store, changes, diff_func=object_diff):
    """Return a dict of diffs for the changes
    """
    pairs = changes_to_pairs(changes)
    return {
        newpath: diff_func(object_store, old, new)
        for old, new in pairs
    }


def obj_blob(object_store, info):
    if not any(info):
        return info
    path, mode, sha = info
    return (path, mode, object_store[sha])


def path_blob(info):
    if not any(info):
        return info
    path, mode, sha = info
    return blob_from_path(path)


def changes_to_blobs(object_store, changes):
    pairs = changes_to_pairs(changes)
    return [
        (obj_blob(object_store, old), path_blob(new),)
        for old, new in pairs
    ]


def diff_changes_paths(object_store, changes):
    """Does a diff assuming that the old blobs are in git and others are unstaged blobs
       in the working directory
    """
    blobs = changes_to_blobs(object_store, changes)
    return {
        new[0]: blob_diff(object_store, old, new)
        for old, new in blobs
    }


def changes_tree_diff(object_store, old_tree, new_tree):
    return object_store.tree_changes(old_tree, new_tree)


def dict_tree_diff(object_store, old_tree, new_tree):
    """Returns a dictionary where the keys are the filenames and their respective
    values are their diffs
    """
    changes = changes_tree_diff(object_store, old_tree, new_tree)
    return diff_changes(object_store, changes)


def classic_tree_diff(object_store, old_tree, new_tree):
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


def blob_from_path(path):
    """Returns a tuple of (sha_id, mode, blob)
    """
    with open(path, 'rb') as working_file:
        blob = Blob()
        blob.data = working_file.read()
    return (path, os.stat(path).st_mode, blob)
