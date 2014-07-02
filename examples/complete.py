# Samy Pessé <samypesse@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it only under the terms of the GNU GPLv2 and/or the Apache
# License, Version 2.0.  See the COPYING file for further details.

from gittle import Gittle

path = '/tmp/gittle_bare'

# Clone repository
repo = Gittle.clone('git://github.com/FriendCode/gittle.git', path)

# Information
print "Branches :"
print repo.branches
print "Commits :"
print repo.commit_count

# Commiting
fn = 'test.txt'
filename = os.path.join(path, fn)

# Create a new file
fd = open(filename, 'w+')
fd.write('My file commited using Gittle')
fd.close()

# Stage file
repo.stage(fn)

# Do commit
repo.commit(name='Samy Pessé', email='samypesse@gmail.com', message="This is a commit")

# Commit info
print "Commit : ", repo.commit_info()

# Auth for pushing
repo.auth(pkey=open("private_key"))

# Push
repo.push()
