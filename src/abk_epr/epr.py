#!/usr/bin/env python
"""Main program for renaming images and translate images from raw to dng format."""

# Standard library imports
from enum import Enum
import os
from pathlib import Path
import shutil
import sys
import logging
import re
from datetime import datetime
import json


# Third party imports
from pydngconverter import DNGConverter
from colorama import Fore, Style
import exiftool


# Local application imports
from abk_epr.abk_common import PerformanceTimer, function_trace
from abk_epr.clo import CommandLineOptions


# -----------------------------------------------------------------------------
# Local Constants
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# local functions
# -----------------------------------------------------------------------------
class ListType(Enum):
    """ListType is type of image or video list."""

    RAW_IMAGE_DICT = "raw_image_dict"
    THUMB_IMAGE_DICT = "thumb_image_dict"
    COMPRESSED_IMAGE_DICT = "compressed_image_dict"
    COMPRESSED_VIDEO_DICT = "compressed_video_dict"


class ExifTag(Enum):
    """ExifTags contains all exif meta data tags."""

    SOURCE_FILE = "SourceFile"
    CREATE_DATE = "EXIF:CreateDate"
    MAKE = "EXIF:Make"
    MODEL = "EXIF:Model"


class ExifRename:
    """ExifRename contains module to convert RAW images to DNG & rename them using exif data."""

    FILES_TO_EXCLUDE_EXPRESSION = r"Adobe Bridge Cache|Thumbs.db|^\."
    THMB = {"ext": "jpg", "dir": "thmb"}
    SUPPORTED_RAW_IMAGE_EXT = {
        "Adobe": ["dng"],
        "Canon": ["crw", "cr2", "cr3"],
        "FujiFilm": ["raf"],
        "Leica": ["rwl"],
        "Minolta": ["mrw"],
        "Nikon": ["nef", "nrw"],
        "Olympus": ["orw"],
        "Panasonic": ["raw", "rw2"],
        "Pentax": ["pef"],
        "Samsung": ["srw"],
        "Sony": ["arw", "sr2"],
    }
    SUPPORTED_COMPRESSED_IMAGE_EXT_LIST = [
        "gif",
        "heic",
        "jpg",
        "jpeg",
        "jng",
        "mng",
        "png",
        "psd",
        "tiff",
        "tif",
    ]
    # crm (Canon Raw Movie) is not compressed,
    # but we are not going to compress/transform into other format.
    SUPPORTED_COMPRESSED_VIDEO_EXT_LIST = [
        "3g2",
        "3gp2",
        "crm",
        "m4a",
        "m4b",
        "m4p",
        "m4v",
        "mov",
        "mp4",
        "mqv",
        "qt",
    ]
    EXIF_UNKNOWN = "unknown"
    DATE_UNKNOWN = "yyyymmdd"
    DIR_NAME = "DirName"
    EXIF_TAGS = [ExifTag.CREATE_DATE.value, ExifTag.MAKE.value, ExifTag.MODEL.value]

    def __init__(self, logger: logging.Logger, op_dir: str):
        """ExifRename init."""
        self._logger = logger or logging.getLogger(__name__)
        self._op_dir = op_dir
        self._current_dir = None
        self._supported_raw_image_ext_list = list(
            set([ext for exts in self.SUPPORTED_RAW_IMAGE_EXT.values() for ext in exts])
        )
        self._logger.debug(f"{self._supported_raw_image_ext_list = }")
        self._project_name = None

    @property
    def project_name(self) -> str:
        """Returns project name."""
        if self._project_name is None:
            current_dir = os.getcwd()
            norm_path = os.path.basename(os.path.normpath(current_dir))
            dir_parts = norm_path.split("_")
            self._project_name = "_".join(dir_parts[1:])
            self._logger.info(f"{self._project_name = }")
        return self._project_name

    @function_trace
    def check_exiftool(self) -> None:
        """Check EXIF tool is installed."""
        with exiftool.ExifTool() as exif_tool:
            exif_tool.logger = self._logger
            exiftool_exe = exif_tool.executable
            self._logger.debug(f"{exiftool_exe=}")

    @function_trace
    async def move_rename_convert_images(self) -> None:
        """Move, rename and convert images."""
        self._validate_image_dir()
        self._change_to_image_dir()
        metadata_list = self._read_image_dir()
        await self._move_and_rename_files_concurrently(metadata_list)
        self._change_from_image_dir()

    @function_trace
    def return_to_previous_state(self) -> None:
        """Returns to the previous state."""
        self._change_from_image_dir()

    @function_trace
    def _change_to_image_dir(self) -> None:
        """Changes into image directory."""
        if self._op_dir != ".":
            self._current_dir = os.getcwd()
            os.chdir(self._op_dir)
            self._logger.info(f"inside directory: {self._op_dir}")

    @function_trace
    def _change_from_image_dir(self) -> None:
        """Returns from image directory."""
        if self._current_dir is not None:
            os.chdir(self._current_dir)
            self._logger.info(f"inside directory: {self._current_dir}")

    @function_trace
    async def _move_and_rename_files_concurrently(self, collection_dict) -> None:
        """Moves and renames files."""
        if collection_dict:
            for key, value in collection_dict.items():
                await self._move_and_rename_files(key, value)

    async def _rename_file_async(self, old_name: str, new_file: str) -> None:
        """Rename file asynchronously.

        Args:
            old_name (str): _description_
            new_file (str): _description_
        """
        try:
            os.rename(old_name, new_file)
            self._logger.debug(f"renamed file: {old_name} to {new_file}")
        except OSError as exp:
            self._logger.error(f"Error renaming: {old_name}: {str(exp)}")

    @function_trace
    async def _move_and_rename_files(self, key, value) -> None:
        """Moves and renames files."""
        self._logger.info(f"_move_and_rename_files: {key = }, {value = }")
        rename_files_list: list[tuple[str, str]] = []
        for directory, obj_list in value.items():
            file_ext = directory.split("_")[-1]
            self._logger.info(f"{directory = }, {file_ext = }, {obj_list = }")
            if not os.path.exists(directory):
                os.makedirs(directory)
            for obj in obj_list:
                # self._logger.info(f'ABK: {obj = }')
                new_file_name = f"./{directory}/{obj[ExifTag.CREATE_DATE.value]}_{obj[ExifTag.MAKE.value]}_{obj[ExifTag.MODEL.value]}_{self.project_name}.{file_ext}".lower()  # noqa: E501
                old_file_name = obj[ExifTag.SOURCE_FILE.value]
                # self._logger.info(f"ABK: {old_file_name = }, {new_file_name = }")
                rename_files_list.append((old_file_name, new_file_name))
        if len(rename_files_list) > 0:
            rename_tasks = [
                self._rename_file_async(old_name, new_name)
                for old_name, new_name in rename_files_list
            ]  # noqa: E501
            await asyncio.gather(*rename_tasks)

        if key == ListType.RAW_IMAGE_DICT.value:
            self._logger.info(f"{ListType.RAW_IMAGE_DICT.value = }")
            convert_list: list[tuple[str, str]] = []
            for old_dir, obj_list in value.items():  # noqa: B007
                base_dir, dir_ext = old_dir.rsplit("_", 1)
                if dir_ext == "dng":
                    continue
                new_dir = f"{base_dir}_dng"
                convert_list.append((old_dir, new_dir))
            if len(convert_list) > 0:
                self._logger.info(f"{convert_list = }")
                convert_tasks = [
                    self._convert_raw_files(old_dir, new_dir) for old_dir, new_dir in convert_list
                ]  # noqa: E501
                await asyncio.gather(*convert_tasks)
                self._delete_org_raw_files(convert_list)

    async def _convert_raw_files(self, src_dir: str, dst_dir: str):
        """Converts raw files."""
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        py_dng = DNGConverter(source=Path(src_dir), dest=Path(dst_dir))
        return await py_dng.convert()

    def _delete_org_raw_files(self, convert_list: list[tuple[str, str]]):
        """Deletes original raw files."""
        for raw_dir, dng_dir in convert_list:
            raw_files = [file_name.rsplit(".", 1)[0] for file_name in os.listdir(raw_dir)]
            dng_files = [file_name.rsplit(".", 1)[0] for file_name in os.listdir(dng_dir)]
            if all(file_name in dng_files for file_name in raw_files):
                self._logger.info(f"Deleting directory: {raw_dir}")
                shutil.rmtree(raw_dir)
            else:
                self._logger.info(f"Not deleting directory: {raw_dir}")
                raw_file_ext = raw_dir.split("_")[-1]
                matching_files = set(raw_files).intersection(dng_files)
                for file_name in matching_files:
                    full_file_name = os.path.join(raw_dir, f"{file_name}.{raw_file_ext}")
                    self._logger.info(f"Deleting file: {full_file_name}")
                    os.remove(full_file_name)

    @function_trace
    def _read_image_dir(self) -> dict:
        """Reads image directory."""
        list_collection = {}
        with PerformanceTimer(timer_name="ReadingImageDirectory", logger=self._logger):
            files_list = [f for f in os.listdir(".") if os.path.isfile(f)]
            filtered_list = sorted(
                [i for i in files_list if not re.match(rf"{self.FILES_TO_EXCLUDE_EXPRESSION}", i)]
            )
            self._logger.debug(f"filtered_list = {filtered_list}")
            with exiftool.ExifToolHelper() as etp:
                etp.logger = self._logger
                metadata_list = etp.get_tags(files=filtered_list, tags=self.EXIF_TAGS)
                self._logger.debug(f"{metadata_list = }")
            for metadata in metadata_list:
                list_type: ListType | None = None
                # detect thumbnail files
                file_name = metadata.get(ExifTag.SOURCE_FILE.value)
                file_base, file_extension = os.path.splitext(os.path.basename(file_name))
                file_extension = file_extension.replace(".", "").lower()

                if file_extension in self._supported_raw_image_ext_list:
                    list_type = ListType.RAW_IMAGE_DICT
                elif file_extension in self.SUPPORTED_COMPRESSED_IMAGE_EXT_LIST:
                    if file_extension == self.THMB["ext"]:
                        if any(
                            f"{file_base.lower()}{raw_ext}" in [j.lower() for j in filtered_list]
                            for raw_ext in self._supported_raw_image_ext_list
                        ):
                            file_extension = self.THMB["dir"]
                            self._logger.debug(f"{file_extension=} for file: {file_name}")
                            list_type = ListType.THUMB_IMAGE_DICT
                        else:
                            list_type = ListType.COMPRESSED_IMAGE_DICT
                    else:
                        list_type = ListType.COMPRESSED_IMAGE_DICT
                elif file_extension in self.SUPPORTED_COMPRESSED_VIDEO_EXT_LIST:
                    list_type = ListType.COMPRESSED_VIDEO_DICT

                if list_type:
                    metadata[ExifTag.CREATE_DATE.value] = (
                        metadata.get(ExifTag.CREATE_DATE.value, self.EXIF_UNKNOWN)
                        .replace(":", "")
                        .replace(" ", "_")
                    )
                    metadata[ExifTag.MAKE.value] = metadata.get(
                        ExifTag.MAKE.value, self.EXIF_UNKNOWN
                    ).replace(" ", "")
                    if (
                        metadata[ExifTag.MAKE.value] == self.EXIF_UNKNOWN
                        and list_type == ListType.RAW_IMAGE_DICT
                    ):
                        metadata[ExifTag.MAKE.value] = next(
                            (
                                key
                                for key, value in self.SUPPORTED_RAW_IMAGE_EXT.items()
                                if any(ext in file_extension for ext in value)
                            ),
                            self.EXIF_UNKNOWN,
                        )
                    metadata[ExifTag.MODEL.value] = metadata.get(
                        ExifTag.MODEL.value, self.EXIF_UNKNOWN
                    ).replace(" ", "")
                    if (
                        metadata[ExifTag.MAKE.value] in metadata[ExifTag.MODEL.value]
                        and metadata[ExifTag.MAKE.value] != self.EXIF_UNKNOWN
                    ):
                        metadata[ExifTag.MODEL.value] = (
                            metadata[ExifTag.MODEL.value]
                            .replace(metadata[ExifTag.MAKE.value], "")
                            .strip()
                        )
                    dir_parts = [
                        metadata[ExifTag.MAKE.value],
                        metadata[ExifTag.MODEL.value],
                        file_extension,
                    ]
                    dir_name = "_".join(dir_parts).lower()
                    self._logger.debug(f"{list_type.value = }")
                    list_collection.setdefault(list_type.value, {}).setdefault(
                        dir_name, []
                    ).append(metadata)
            # TODO: if there is no date and time: get the date from the fir name and set time to 'xxxxxx'  # noqa: E501
            # TODO: if there is repeat in make and model remove the repeated words from model

        if len(list_collection) == 0:
            raise Exception("no files to process for the current directory.")
        self._logger.debug(f"list_collection = {json.dumps(list_collection, indent=4)}")
        return list_collection

    @function_trace
    def _validate_image_dir(self):
        self._logger.debug(f"{self._op_dir = }")
        try:
            dir_name_to_validate = self._op_dir if self._op_dir != "." else os.getcwd()
            last_part_of_dir = os.path.basename(os.path.normpath(dir_name_to_validate))

            match = re.match(r"^(\d{8})_\w+$", last_part_of_dir)
            if not match:
                raise ValueError("Regex match failed")

            datetime.strptime(match.group(1), "%Y%m%d")

        except (AttributeError, ValueError) as e:
            raise Exception(
                "Not a valid date / directory format, please use: YYYYMMDD_name_of_the_project"
            ) from e


async def epr():
    """Main program to order images."""
    exit_code = 1
    exif_rename = None
    try:
        clo = CommandLineOptions()
        clo.handle_options()
        exif_rename = ExifRename(logger=clo.logger, op_dir=clo.options.dir)
        exif_rename.check_exiftool()
        await exif_rename.move_rename_convert_images()
        exit_code = 0
    except Exception as exception:
        if exif_rename:
            exif_rename.return_to_previous_state()
        print(f"{Fore.RED}ERROR: executing exif image renamer")
        print(f"EXCEPTION: {exception}{Style.RESET_ALL}")
        exit_code = 1
    finally:
        sys.exit(exit_code)


if __name__ == "__main__":
    import asyncio

    asyncio.run(epr())
