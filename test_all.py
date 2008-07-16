#!/usr/bin/env python

# Author: Ilan Schnell, Enthought, Inc. <ischnell@enthought.com>
#
# Description:
#     This unittest tests the entire package.
#     It can be run directly:
#
#         $ python test_all.py
#
#     or from setup.py
#
#         $ python setup.py test

import os.path
import re
import subprocess
import unittest


class Tests(unittest.TestCase):
    
    def test_directories(self):
        """
            Runs nosetests (as a subprocess) in each subdirectory
            which ends with 'tests' (case ignored).
            Directories containing certain words, e.g. 'attic' may
            be skipped.
        """
        skip_dirs = ['attic', 'deprecated', 'research']

        pat_test = re.compile(r'tests$', re.I)

        # contruct regular expression for directories to be skipped
        # note that .svn is always excluded.
        pat_skip = re.compile('(' +
                              '|'.join([r'\b%s\b' % s for s in skip_dirs]+
                                        [r'\.svn']) +
                              ')', re.I)
        cwd = os.getcwd()
        
        # map directory to exit status of nosetests
        nose_dirs = {}
        
        for root, dum1, dum2 in os.walk(cwd):
            if pat_skip.search(root):
                continue

            if pat_test.search(root):
                print 'Running nosetests in:', root
                nose_dirs[root] = subprocess.call(['nosetests'], cwd=root)

        print
        print (30*'=' + ' Ran %i nosetests: ' + 30*'=') % len(nose_dirs)
        
        for d in sorted(nose_dirs):
            print 'Failed' if nose_dirs[d] else 'OK    ', \
                  '.' + d[len(cwd):]


if __name__ == '__main__':
    unittest.main()
