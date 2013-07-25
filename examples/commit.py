# -*- coding: utf8 -*-

import os
from gittle import Gittle
from tempfile import mkdtemp

path = mkdtemp()
fn = 'test.txt'
filename = os.path.join(path, fn)

name = 'Samy Pessé'
email = 'samypesse@gmail.com'
message = "C'est beau là bas"


def create_file():
    fd = open(filename, 'w+')
    fd.write('blabla\n BOOM BOOM\n à la montagne')
    fd.close()

repo = Gittle.init(path)
create_file()

repo.stage(fn)
repo.commit(name=name, email=email, message=message)


print('COMMIT_INFO =', repo.commit_info())

print('PATH =', path)
