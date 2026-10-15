"""Self-check: runs the PyTest suite in tests/. Usage: python autograder.py"""
import os
import sys

import pytest

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # works from any cwd
sys.path.insert(0, os.getcwd())  # so tests can import lab_kernels
sys.exit(pytest.main(["tests", "-p", "no:warnings", "-s"]))
