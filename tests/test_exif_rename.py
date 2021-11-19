"""Unit tests for main.py"""

# Standard library imports
from os import getcwd
import unittest
from unittest.mock import patch, call

# Third party imports
from optparse import OptionParser, Values

# Local application imports
from context import ExifRename

class TestExifRename(unittest.TestCase):
    TEST_DIR = './data/sony_raw'
    _current_dir = None

    def setUp(self) -> None:
        self.maxDiff = None
        self._current_dir = getcwd()
        values = Values()
        values.dir = self.TEST_DIR
        values.verbose = False
        self.mut = ExifRename(options=values)
        return super().setUp()


    # -------------------------------------------------------------------------
    # Tests for get_ingredients
    # -------------------------------------------------------------------------
    def test_ExifRename_changes_into_image_directory_and_back(self):
        with patch('os.chdir') as mock_chdir:
            self.mut.move_rename_convert_images()
            self.assertEqual(mock_chdir.mock_calls, [
                call(self.TEST_DIR),
                call(self._current_dir)
            ])


if __name__ == '__main__':
    unittest.main()
