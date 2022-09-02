# -*- coding: utf-8 -*-

"""Tests for ns234b package."""

import sys
sys.path.insert(0,'.')

import ns234b


def test_hello_noargs():
    """Test for ns234b.hello()."""
    s = ns234b.hello()
    assert s == "Hello world"


def test_hello_me():
    """Test for ns234b.hello('me')."""
    s = ns234b.hello('me')
    assert s == "Hello me"


# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_hello_noargs

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')

# eof