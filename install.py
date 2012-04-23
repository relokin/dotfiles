#!/usr/bin/env python

"""Copies the files and symlinks the directories from the current
directory to the home directory. Checks if destination files exist and
asks for permission to overwrite when they are not identical
"""

__author__    = 'Nikos Nikoleris'
__copyright__ = 'Copyright 2012, Nikos Nikoleris'
__credits__   = ['Nikos Nikoleris']

__licence__    = 'GPL'
__version__    = '0.1'
__maintainer__ = 'Nikos Nikoleris'
__email__      = 'nikos.nikoleris@it.uu.se'
__status__     = 'Prototype'

import re, sys
import glob
import shutil
import filecmp
import os.path

EXCLUDE = [ 'install.py', 'README\..*', 'LICENSE', '.*~', '#.*#' ]

def action(src, dst):
    """Check if destination exists and ask for action if not identical"""
    _dst = os.path.expanduser(dst)
    if os.path.exists(dst) and not action.replace_all:
        if filecmp.cmp(src, _dst):
            print 'identical %s' % dst
            return True
        if os.path.islink(_dst):
            _dst_link = os.readlink(_dst)
            if os.path.abspath(_dst_link) == src:
                print 'identical %s' % dst
                return True

        answer = None
        while answer not in [ 'a', 'y', 'q', 'n' ]:
            answer = raw_input('overwrite %s? [ynaq] ' % dst)

        if answer == 'a':
            action.replace_all = True
            os.unlink(_dst)
        elif answer == 'q':
            sys.exit(0)
        elif answer == 'n':
            print 'skipping %s' % dst
            return True
        else:
            print 'deleting %s' % dst
            os.unlink(_dst)
    # Upon replace all we need to remove everytime
    elif os.path.exists(dst) and action.replace_all:
        os.unlink(_dst)

    return False
action.replace_all = False

def main():
    """Check DESCRIPTION"""
    excluded = [ re.compile(f) for f in EXCLUDE ]
    for _src in glob.iglob('*'):
        src = os.path.dirname(os.path.abspath(__file__)) + '/' + _src
        skip = False
        for pat in excluded:
            if pat.match(src):
                skip = True
                break

        if skip == True:
            continue

        dst = '~/.' + _src
        _dst = os.path.expanduser(dst)

        skip = action(src, dst)
        
        if skip == True:
            continue

        if os.path.isfile(src):
            # Copy w /file attributes
            shutil.copy2(src, _dst)
            print 'copying %s' % dst
        elif os.path.isdir(src):
            os.symlink(src, _dst)
            print 'linking %s' % dst

if __name__ == '__main__':
    main()


