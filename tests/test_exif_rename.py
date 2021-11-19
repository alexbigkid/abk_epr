"""Unit tests for main.py"""

# Standard library imports
import unittest
from unittest.mock import patch, call

# Third party imports
from optparse import OptionParser, Values

# Local application imports
from context import ExifRename

class TestExifRename(unittest.TestCase):
    TEST_IMAGE_DIR = './unittest_image_dir'
    TEST_CURRENT_DIR = './unittest_current_dir'
    _current_dir = None

    def setUp(self) -> None:
        self.maxDiff = None
        values = Values()
        values.dir = self.TEST_IMAGE_DIR
        values.verbose = False
        self.mut = ExifRename(options=values)
        return super().setUp()


    # -------------------------------------------------------------------------
    # Tests for get_ingredients
    # -------------------------------------------------------------------------
    def test_ExifRename_changes_into_image_directory_and_back(self):
        with patch('os.getcwd', return_value=self.TEST_CURRENT_DIR) as mock_getcwd:
            with patch('os.chdir') as mock_chdir:
                self.mut.move_rename_convert_images()
                self.assertEqual(mock_getcwd.mock_calls, [call()])
                self.assertEqual(mock_chdir.mock_calls, [call(self.TEST_IMAGE_DIR), call(self.TEST_CURRENT_DIR)])


if __name__ == '__main__':
    unittest.main()
