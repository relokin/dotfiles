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

import re, sys, os, glob
import os.path

import pystache

EXCLUDE = [ 'install.py', 'README\..*', 'LICENSE', '.*~', '#.*#' ]
TEMPLATE_EXT = '.mustache'

class Patterns(object):
    """Functions used to substitute tags in template files"""
    @classmethod
    def name(cls):
        """Get and return full name"""
        return raw_input('Your Name: ')

    @classmethod
    def email(cls):
        """Get and return email address"""
        return raw_input('Your Email: ')

    @classmethod
    def gh_user(cls):
        """Get and return GitHub Username"""
        return raw_input('GitHub Username: ')

    @classmethod
    def gh_token(cls):
        """Get and return GitHub API Token"""
        return raw_input('GitHub API Token: ')

    @classmethod
    def home(cls):
        """Return absolute path to the home directory"""
        return os.path.expanduser('~')


def action(src_abs, dst_abs, _dst_abs):
    """Check if destination exists and ask for action if not identical"""
    if os.path.exists(_dst_abs) and not action.replace_all:
        if os.path.islink(_dst_abs):
            dst_link = os.readlink(_dst_abs)
            if os.path.abspath(dst_link) == src_abs:
                print 'identical %s' % dst_abs
                return True

        answer = None
        while answer not in [ 'a', 'y', 'q', 'n' ]:
            answer = raw_input('overwrite %s? [ynaq] ' % dst_abs)

        if answer == 'a':
            action.replace_all = True
            os.unlink(_dst_abs)
        elif answer == 'q':
            sys.exit(0)
        elif answer == 'n':
            print 'skipping %s' % dst_abs
            return True
        else:
            print 'deleting %s' % dst_abs
            os.unlink(_dst_abs)
    # Upon replace all we need to remove everytime
    elif os.path.exists(_dst_abs) and action.replace_all:
        os.unlink(_dst_abs)

    return False
action.replace_all = False

def main():
    """Check DESCRIPTION"""
    excluded = [ re.compile(f) for f in EXCLUDE ]
    for src in glob.iglob('*'):
        src_abs = os.path.dirname(os.path.abspath(__file__)) + '/' + src
        skip = False
        for exc in excluded:
            if exc.match(src):
                skip = True
                break

        if skip == True:
            continue

        if src.endswith(TEMPLATE_EXT):
            n = len(TEMPLATE_EXT)
            dst_abs = '~/.' + src[:(-n)]
        else:
            dst_abs = '~/.' + src
        _dst_abs = os.path.expanduser(dst_abs)
        skip = action(src_abs, dst_abs, _dst_abs)

        if skip == True:
            continue

        if src_abs.endswith(TEMPLATE_EXT):
            renderer = pystache.Renderer()
            patterns = Patterns()
            with open(_dst_abs, 'w') as f:
                print 'generating %s' % dst_abs
                f.write(renderer.render_path(src_abs, patterns))
        else:
            print 'linking %s' % dst_abs
            os.symlink(src_abs, _dst_abs)

if __name__ == '__main__':
    main()


