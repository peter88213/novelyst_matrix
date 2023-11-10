"""Build a matrix novelyst plugin.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the novxlib package.

The novxlib project (see https://github.com/peter88213/novxlib)
must be located on the same directory level as the novelyst_matrix project. 

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
sys.path.insert(0, f'{os.getcwd()}/../../novxlib-Alpha/src')
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE = f'{SRC}novelyst_matrix.py'
TARGET_FILE = f'{BUILD}novelyst_matrix.py'


def main():
    inliner.run(SOURCE_FILE, TARGET_FILE, 'nvmatrixlib', '../../novelyst_matrix/src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'novxlib-Alpha', '../../novxlib-Alpha/src/', copynovxlib=False)
    print('Done.')


if __name__ == '__main__':
    main()
