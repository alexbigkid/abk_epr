"""Context - import helper for unit tests"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from abk_epr import CommandLineOptions, ExifRename
