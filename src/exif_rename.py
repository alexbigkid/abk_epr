#!/usr/bin/env python
"""Main program for renaming images and translate images from raw to dng format"""

# Standard library imports
import os
import sys
import logging
# import logging.handlers
import logging.config
import yaml
# import asyncio

# Third party imports
from optparse import OptionParser, Values
# from pydngconverter import DNGConverter, flags
from colorama import Fore, Style
from yaml.loader import Loader
# import exiftool

# Local application imports
from _version import __version__


CONSOLE_LOGGER = 'consoleLogger'
FILE_LOGGER = 'fileLogger'

class CommandLineOptions:
    """CommandLineOptions module handles all parameters passed in to the python script"""
    _args = None
    options = None
    logger = None

    def __init__(self, args:list=None, options:Values=None):
        self._args = args
        self.options = options
        self.logger = None


    def handle_options(self) -> None:
        """Handles user specified options and arguments"""
        usage_string = "usage: %prog [options]"
        version_string = "%prog version: " + Fore.GREEN + f"{__version__}{Style.RESET_ALL}"
        parser = OptionParser(usage=usage_string, version=version_string)
        parser.add_option(
            "-d",
            "--directory",
            action="store",
            dest="dir",
            default=".",
            help="directory, where images will be converted and renamed"
        )
        parser.add_option(
            "-v",
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="verbose execution"
        )
        parser.add_option(
            "-l",
            "--log_into_file",
            action="store_true",
            dest="log_into_file",
            default=False,
            help="log into file exif_rename.log, if True, otherwise log into console"
        )
        parser.add_option(
            "-c",
            "--config_log_file",
            action="store",
            dest="config_log_file",
            default="./src/logging.yaml",
            help="config file for logging print outs"
        )
        (self.options, self._args) = parser.parse_args()

        if len(self._args) != 0:
            parser.error("wrong number of arguments")
        self._setup_logging()
        self.logger.info(f"options: {self.options}")
        self.logger.info(f"args: {self._args}")
        self.logger.info(f"options.dir: {self.options.dir}")
        self.logger.info(f"options.verbose: {self.options.verbose}")
        self.logger.info(f"options.log_into_file: {self.options.log_into_file}")
        self.logger.info(f"__version__: {__version__}")


    def _setup_logging(self) -> None:
        try:
            with open(self.options.config_log_file, 'r') as stream:
                try:
                    config_yaml = yaml.load(stream, Loader=yaml.FullLoader)
                    logging.config.dictConfig(config_yaml)
                    logger_type = FILE_LOGGER if self.options.log_into_file else CONSOLE_LOGGER
                    self.logger = logging.getLogger(logger_type)
                    self.logger.disabled = self.options.verbose == False
                except ValueError:
                    raise ValueError(f'{self.options.config_log_file} is not a valid yaml format')
                except Exception as ex:
                    raise Exception(f'not ValueError: {ex.exeption}')
        except IOError:
            raise IOError(f'{self.options.config_log_file} does not exist.')
        self.logger.debug(f"logger_type: {logger_type}")



class ExifRename:
    """ExifRename contains module to convert RAW images to DNG and rename them using exif meta data"""
    FILES_TO_EXCLUDE  = {'Adobe Bridge Cache', 'Thumbs.db'}


    def __init__(self, logger:logging.Logger=None, options:Values=None):
        self._logger = logger
        self._options = options
        self._current_dir = None

    def __del__(self):
        pass
        # if self._options.verbose:
        #     self._logger.


    def move_rename_convert_images(self) -> None:
        self._logger.debug(f"-> move_rename_convert_images")
        self._change_to_image_dir()
        self._read_image_dir()
        self._change_from_image_dir()
        self._logger.debug(f"<- move_rename_convert_images")


    def return_to_previous_state(self):
        self._logger.debug(f"-> return_to_previous_state")
        self._change_from_image_dir()
        self._logger.debug(f"<- return_to_previous_state")


    def _change_to_image_dir(self) -> None:
        self._logger.debug(f"-> _change_to_image_dir")
        if self._options.dir != ".":
            self._current_dir = os.getcwd()
            os.chdir(self._options.dir)
            self._logger.info(f"inside directory: {self._options.dir}")
        self._logger.debug(f"<- _change_to_image_dir")


    def _change_from_image_dir(self) -> None:
        self._logger.debug(f"-> _change_from_image_dir")
        if self._current_dir is not None:
            os.chdir(self._current_dir)
            self._logger.info(f"inside directory: {self._current_dir}")
        self._logger.debug(f"<- _change_from_image_dir")


    def _move_and_rename_files(self) -> None:
        self._logger.debug(f"-> _move_and_rename_files")
        pass
        self._logger.debug(f"<- _move_and_rename_files")


    def _convert_raw_files(self) -> None:
        self._logger.debug(f"-> _convert_raw_files")
        pass
        self._logger.debug(f"<- _convert_raw_files")


    def _read_image_dir(self) -> None:
        self._logger.debug(f"<- _read_image_dir")
        onlyfiles = [f for f in os.listdir('.') if os.path.isfile(f)]
        self._logger.debug(f"only_files = {onlyfiles}")
        self._logger.debug(f"<- _read_image_dir")


    def _validate_image_dir(self):
        self._logger.debug(f"-> _validate_image_dir")
        pass
        self._logger.debug(f"<- _validate_image_dir")
        # $cur_dir =~ /^\d{4}(\d{2})(\d{2})_\w+$/;
        # $month = $1;
        # $day   = $2;

        # die "wrong month $month\n" if(defined($month) && $month > 12);
        # die "wrong day $day\n" if(defined($day) && $day > 31);




def main():
    exit_code = 0

    try:
        command_line_options = CommandLineOptions()
        command_line_options.handle_options()
        exif_rename = ExifRename(logger=command_line_options.logger, options=command_line_options.options)
        exif_rename.move_rename_convert_images()
    except Exception as exception:
        exif_rename.return_to_previous_state()
        print(Fore.RED + f"ERROR: executing exif image renamer")
        print(f"EXCEPTION: {exception}{Style.RESET_ALL}")
        exit_code = 1
    finally:
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
