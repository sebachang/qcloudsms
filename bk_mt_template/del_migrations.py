#!/usr/bin/python

import os


def search_migrations(root=os.curdir):

    migrations_list = [path for path, dirs, files in os.walk(os.path.abspath(root)) if 'migrations' in path]

    for i in migrations_list:
        for x in os.listdir(i):
            if not x.startswith('__'):
                yield os.path.join(i, x)

if __name__ == '__main__':
    for x in search_migrations(os.path.dirname(os.path.abspath(__file__)) + '\mt_apps'):
        print(x)
        os.remove(x)
    for i in search_migrations(os.path.dirname(os.path.abspath(__file__)) + '\\blueapps'):
        print(i)
        os.remove(i)