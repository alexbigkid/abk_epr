#!/usr/bin/env python
"""Main program for renaming images and translate images from raw to dng format"""

# Standard library imports
import sys
# import asyncio

# Third party imports
from optparse import OptionParser
from pydngconverter import DNGConverter, flags
from colorama import Fore, Style
from os import listdir, system, getcwd, chdir
from os.path import isfile, isdir, join
# import exiftool

# Local application imports
from _version import __version__

class ExifRename:
    """ExifRename contains module to convert RAW images to DNG and rename them using exif meta data"""
    _options = None
    _args = None
    _current_dir = None


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
        (self._options, self._args) = parser.parse_args()

        if len(self._args) != 0:
            parser.error("wrong number of arguments")

        if self._options.verbose:
            print(f"options: {self._options}")
            print(f"args: {self._args}")
            print(f"options.dir: {self._options.dir}")
            print(f"__version__: {__version__}")


    def change_to_image_dir(self) -> None:
        if self._options.dir != ".":
            self._current_dir = getcwd()
            chdir(self._options.dir)


    def change_from_image_dir(self) -> None:
        if self._current_dir is not None:
            chdir(self._current_dir)


    def move_rename_convert_images(self) -> None:
        pass

    def _move_and_rename_files(self) -> None:
        pass


    def _convert_raw_files(self) -> None:
        pass

    def _read_image_dir(self):
        pass
        # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]



def main():
    exit_code = 0
    exif_rename = ExifRename()

    try:
        exif_rename.handle_options()
        exif_rename.change_to_image_dir()
        exif_rename.move_rename_convert_images()
    except Exception as exception:
        print(Fore.RED + f"ERROR: executing exif image renamer")
        print(f"EXCEPTION: {exception}{Style.RESET_ALL}")
        exit_code = 1
    finally:
        exif_rename.change_from_image_dir()
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
