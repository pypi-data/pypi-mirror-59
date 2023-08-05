#!/usr/bin/env python2

import unittest
import sys

import FixPath

# list the tests explicitly, so that they can be order from most basic
# functionality to more complex.
suites = ['Basic.Test', 'SessionStoreTest']

# To run specific test cases, pass one or more names of package/module names
# on the command line which contain the test cases to be run.

# If no arguments are given, all of the test cases are run.
if len(sys.argv) == 1:
    testnames = suites
else:
    testnames = sys.argv[1:]
tests = unittest.defaultTestLoader.loadTestsFromNames(testnames)

unittest.TextTestRunner(verbosity=2).run(tests)
