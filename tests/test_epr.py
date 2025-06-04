"""Unit tests for epr.py."""

# Standard library imports
import unittest
from unittest.mock import mock_open, patch, call

# Third party imports
from optparse import Values
from parameterized import parameterized

# Local application imports
from context import CommandLineOptions, ExifRename
# import exiftool


class TestExifRename(unittest.IsolatedAsyncioTestCase):
    """TestExifRename class."""

    TEST_IMAGE_DIR = "./20220101_unittest_image_dir"
    TEST_CURRENT_DIR = "./20220101_unittest_current_dir"
    _current_dir = None
    yaml_file = """version: 1
disable_existing_loggers: True
formatters:
    abkFormatterShort:
        format: '[%(asctime)s]:[%(funcName)s]:[%(levelname)s]: %(message)s'
        datefmt: '%Y%m%d %H:%M:%S'
handlers:
    consoleHandler:
        class: logging.StreamHandler
        level: DEBUG
        formatter: abkFormatterShort
        stream: ext://sys.stdout
loggers:
    consoleLogger:
        level: DEBUG
        handlers: [consoleHandler]
        qualname: consoleLogger
        propagate: no
"""
    mut = None

    def setUp(self) -> None:
        """Setup TestExifRename."""
        self.maxDiff = None
        values = Values()
        values.dir = self.TEST_IMAGE_DIR
        values.verbose = False
        values.log_into_file = False
        self.clo = CommandLineOptions()
        self.clo.options = values
        return super().setUp()

    # -------------------------------------------------------------------------
    # Tests for CommandLineOptions
    # -------------------------------------------------------------------------
    def test_CommandLineOptions__setup_logger_throws_given_yaml_config_file_does_not_exist(
        self,
    ) -> None:
        """Test test_CommandLineOptions__setup_logger_throws_given_yaml_config_file_does_not_exist."""  # noqa: E501
        with self.assertRaises(IOError) as context:
            self.clo.options.config_log_file = "NotValidFile.yaml"
            self.clo._setup_logging()
        self.assertEqual(
            str(context.exception), "[Errno 2] No such file or directory: 'NotValidFile.yaml'"
        )

    def test_CommandLineOptions__setup_logger_throws_given_invalid_yaml_file(self) -> None:
        """Test test_CommandLineOptions__setup_logger_throws_given_invalid_yaml_file."""
        with patch("builtins.open", mock_open(read_data='{"notValid": 2}')) as mock_file:
            with self.assertRaises(ValueError) as context:
                self.clo.options.config_log_file = "valid.yaml"
                self.clo._setup_logging()
            self.assertEqual(str(context.exception), "valid.yaml is not a valid yaml format")
            mock_file.assert_called_with("valid.yaml", "r", encoding="utf-8")

    # -------------------------------------------------------------------------
    # Tests for ExifRename
    # -------------------------------------------------------------------------
    @parameterized.expand(
        [
            "./NODATE_unittest_image_dir",
            "/blah-blah/INVALID_DIR_FORMAT_20220101_unittest_image_dir/",
            "../data/20220101NO_UNDERSCORE_DIR",
            "020221301_TOO_MANY_DIGITS",
            "0221301_NOT_ENOUGH_DIGITS",
            "00000101_INVALID_YEAR",
            "20221301_INVALID_MONTH",
            "20220132_INVALID_DAY",
            "20220229_INVALID_DAY_NOT_LEAP_YEAR",
        ]
    )
    async def test_ExifRename__move_rename_convert_images_throws_given_image_dir_has_invalid_format(  # noqa: E501
        self, image_dir: str
    ) -> None:
        """Test test_ExifRename__move_rename_convert_images_throws_given_image_dir_has_invalid_format."""  # noqa: E501
        with patch("builtins.open", mock_open(read_data=self.yaml_file)) as mock_file:
            self.clo.options.config_log_file = "valid.yaml"
            self.clo.options.dir = image_dir
            self.clo._setup_logging()
            mock_file.assert_called_with("valid.yaml", "r", encoding="utf-8")
            self.mut = ExifRename(logger=self.clo.logger, options=self.clo.options)
            with patch("os.getcwd") as mock_getcwd:
                with patch("os.chdir") as mock_chdir:
                    with patch("os.listdir") as mock_listdir:
                        with self.assertRaises(Exception) as context:
                            await self.mut.move_rename_convert_images()
                        self.assertEqual(
                            "Not a valid date / directory format, please use: YYYYMMDD_name_of_the_project",  # noqa: E501
                            str(context.exception),
                        )
                    self.assertEqual(mock_listdir.mock_calls, [])
                self.assertEqual(mock_chdir.mock_calls, [])
            self.assertEqual(mock_getcwd.mock_calls, [call()])

    async def test_ExifRename__move_rename_convert_images_throws_given_image_dir_does_not_exist(
        self,
    ) -> None:
        """Test test_ExifRename__move_rename_convert_images_throws_given_image_dir_does_not_exist."""  # noqa: E501
        with patch("builtins.open", mock_open(read_data=self.yaml_file)) as mock_file:
            self.clo.options.config_log_file = "valid.yaml"
            self.clo._setup_logging()
            mock_file.assert_called_with("valid.yaml", "r", encoding="utf-8")
            self.mut = ExifRename(logger=self.clo.logger, options=self.clo.options)
            with patch("os.getcwd", return_value=self.TEST_CURRENT_DIR) as mock_getcwd:
                with patch(
                    "os.chdir",
                    side_effect=Exception(f"No such file or directory: '{self.TEST_IMAGE_DIR}'"),
                ) as mock_chdir:
                    with self.assertRaises(Exception) as context:
                        await self.mut.move_rename_convert_images()
                    self.assertEqual(
                        f"No such file or directory: '{self.TEST_IMAGE_DIR}'",
                        str(context.exception),
                    )
                self.assertEqual(mock_chdir.mock_calls, [call(self.TEST_IMAGE_DIR)])
            self.assertEqual(mock_getcwd.mock_calls, [call(), call()])

    @patch("exiftool.ExifTool")
    async def test_ExifRename__check_exiftool__get_tests_run_without_exiftool_installed(
        self, mock_exif
    ) -> None:
        """Test test_ExifRename__check_exiftool__get_tests_run_without_exiftool_installed."""
        with patch("builtins.open", mock_open(read_data=self.yaml_file)) as mock_file:
            self.clo.options.config_log_file = "valid.yaml"
            self.clo._setup_logging()
            mock_file.assert_called_with("valid.yaml", "r", encoding="utf-8")
            self.mut = ExifRename(logger=self.clo.logger, options=self.clo.options)
            mock_exif.return_value.executable = "/path/to/exiftool"

            try:
                self.mut.check_exiftool()
            except Exception as exc:
                self.fail(f"An unexpected exception occurred: {exc}")

    @unittest.skip("still not ready")
    @patch("exiftool.ExifToolHelper")
    @patch("os.listdir")
    @patch("os.chdir")
    @patch("os.getcwd")
    async def test_ExifRename__move_rename_convert_images_does_not_change_dir_given_it_is_current_dir(  # noqa: E501
        self, mock_getcwd, mock_chdir, mock_listdir, mock_eth
    ) -> None:
        """Test test_ExifRename__move_rename_convert_images_does_not_change_dir_given_it_is_current_dir."""  # noqa: E501
        with patch("builtins.open", mock_open(read_data=self.yaml_file)) as mock_file:
            self.clo.options.config_log_file = "valid.yaml"
            self.clo.options.dir = "."
            self.clo._setup_logging()
            mock_file.assert_called_with("valid.yaml", "r", encoding="utf-8")
            self.mut = ExifRename(logger=self.clo.logger, options=self.clo.options)
            mock_getcwd.return_value = self.TEST_CURRENT_DIR
            mock_listdir.return_value = ["a.json", "b.json", "c.json", "d.txt"]
            mock_eth.return_value.get_tags.return_value = []

            # with patch('exiftool.ExifTool') as mock_exif:
            # mock_exif.return_value.executable = '/path/to/exiftool'
            with self.assertRaises(Exception) as context:
                await self.mut.move_rename_convert_images()

            self.assertEqual(
                "no files to process for the current directory.", str(context.exception)
            )
            print(f"{mock_eth.mock_calls = }")
            self.assertEqual(
                mock_eth.mock_calls,
                [call(files=[], tags=["EXIF:CreateDate", "EXIF:Make", "EXIF:Model"])],
            )
            self.assertEqual(mock_listdir.mock_calls, [call(".")])
            self.assertEqual(mock_chdir.mock_calls, [])
            self.assertEqual(mock_getcwd.mock_calls, [call()])

    @unittest.skip("still not ready")
    @patch("exiftool.ExifToolHelper.get_tags")
    @patch("os.listdir")
    @patch("os.chdir")
    @patch("os.getcwd")
    async def test_ExifRename__move_rename_convert_images_calls_get_change_list_dir(
        self, mock_getcwd, mock_chdir, mock_listdir, mock_eth_gt
    ) -> None:
        """Test test_ExifRename__move_rename_convert_images_calls_get_change_list_dir."""
        with patch("builtins.open", mock_open(read_data=self.yaml_file)) as mock_file:
            self.clo.options.config_log_file = "valid.yaml"
            self.clo.options.dir = "."
            self.clo._setup_logging()
            mock_file.assert_called_with("valid.yaml", "r", encoding="utf-8")
            self.mut = ExifRename(logger=self.clo.logger, options=self.clo.options)
            mock_getcwd.return_value = self.TEST_CURRENT_DIR
            files_to_return = ["a.json", "b.json"]
            mock_listdir.return_value = files_to_return
            mock_eth_gt.return_value = [
                {
                    "SourceFile": "20110709_174538_5dm2_vancouver_035.cr2",
                    "EXIF:CreateDate": "2011:07:09 17:45:38",
                    "EXIF:Make": "Canon",
                    "EXIF:Model": "Canon EOS 5D Mark II",
                },
                {
                    "SourceFile": "20110709_174604_5dm2_vancouver_036.cr2",
                    "EXIF:CreateDate": "2011:07:09 17:46:04",
                    "EXIF:Make": "Canon",
                    "EXIF:Model": "Canon EOS 5D Mark II",
                },
                {
                    "SourceFile": "20110709_175718_5dm2_vancouver_038.cr2",
                    "EXIF:CreateDate": "2011:07:09 17:57:18",
                    "EXIF:Make": "Canon",
                    "EXIF:Model": "Canon EOS 5D Mark II",
                },
                {
                    "SourceFile": "20110709_175905_5dm2_vancouver_040.cr2",
                    "EXIF:CreateDate": "2011:07:09 17:59:05",
                    "EXIF:Make": "Canon",
                    "EXIF:Model": "Canon EOS 5D Mark II",
                },
            ]

            with patch("os.path.isfile", return_value=True) as mock_isfile:
                await self.mut.move_rename_convert_images()

            self.assertEqual(
                mock_isfile.mock_calls, [call(files_to_return[0]), call(files_to_return[1])]
            )
            self.assertEqual(
                mock_eth_gt.mock_calls,
                [
                    call(
                        files=files_to_return, tags=["EXIF:CreateDate", "EXIF:Make", "EXIF:Model"]
                    )
                ],
            )
            self.assertEqual(mock_listdir.mock_calls, [call(".")])
            self.assertEqual(mock_chdir.mock_calls, [])
            self.assertEqual(mock_getcwd.mock_calls, [call()])


if __name__ == "__main__":
    unittest.main()
