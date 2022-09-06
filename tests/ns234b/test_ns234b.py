# -*- coding: utf-8 -*-

"""Tests for ns234b package."""

import sys
sys.path.insert(0,'.')

import ns234b


def test_distance():
    p = (0,0,0)
    assert ns234b.distance(p,p) == 0
    q = (1,0,0)
    assert ns234b.distance(p,q) == 1
    q = (2,0,0)
    assert ns234b.distance(p,q) == 2


# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_distance

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')

# eof