"""A small, lightweight Logger written in Python. Mainly created
because I dislike the already existing Logger module in the Python
Standard Library, also because I can sent colored-text directly
through this.
"""

import re
import time
import colorama
import constants
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime as dt

colorama.init(autoreset=True)


@dataclass
class SpaceLogger():
    log_string: str
    logger_name: str = "ROOT"
    log_mode: str = "c"
    logfile_name: str = "log.txt"
    logger_enabled: bool = True
    color_enabled: bool = True,
    file_colors: bool = False,
    logger_directory: Path = Path(".")

    def __init__(self):
        # log_mode can only have "console" or "file" flags.
        for char in self.log_mode:
            if char not in "cf":
                raise ValueError("log_mode must only have flags 'c' or 'f'")

        # Filename and directory name validity checks
        if self._is_valid_name(self.logfile_name) is False:
            raise ValueError("Filename cannot start with or exclusively be, whitespace.")

        if self._is_valid_name(self.logger_directory.stem) is False:
            ValueError("Directory name cannot start with or exclusively be, whitespace.")

        _file_path = self.logger_directory.absolute() / Path(self.logfile_name)
        self._logfile_path = _file_path
        self._log_file = open(_file_path, "a+")

    def _format_message(self, level: str, message: str) -> str:
        """Creates a formatted message using log_string.

        :param message: the message to format.
        :type message: str
        :param level: the level of the message
        :type level: str
        :return: the formatted message
        :rtype: str
        """

        specifiers = {
            "%D": lambda: self._get_date(),
            "%T": lambda: self._get_time(),
            "%C": lambda: self.creation_time,
            "%N": lambda: self.logger_name,
            "%P": lambda: __file__,
            "%L": lambda: level,
            "%%": lambda: "%"
        }

        formatted = "".join(message)

        for specifier, repl in specifiers.items():
            formatted = formatted.replace(specifier, repl())

        return formatted

    def _output_mode(self, message_type: str, output_message: str):
        """Goes through the format log_mode and outputs it to the output specifier.

        :param message_type: the color from colorama to use
        :type message_type: str
        :param output_message: the message to send to the console or logfile.
        :type output_message: str
        """

        for specifier in self.log_mode:
            # Console specifier
            if specifier == "c":
                if self.color_enabled:
                    print(message_type + output_message)
                else:
                    print(output_message)

            # Logfile specifier. If _log_file is None, there is no file to log
            # the output to.
            if specifier == "f" and self._log_file is not None:
                # Wont send color INFOrmation to the logfile.
                if not self.file_colors:
                    self._log_file.write(output_message + "\n")
                    self._log_file.flush()

                # Will send color INFOrmation to the logfile.
                else:
                    self._log_file.write(message_type + output_message + RESET + "\n")
                    self._log_file.flush()

    @staticmethod
    def _get_date():
        """Gets the current date.
        """

        return str(dt.fromtimestamp(time.time()).strftime('%Y-%m-%d'))

    @staticmethod
    def _get_time():
        """Gets the current time
        """

        return str(dt.fromtimestamp(time.time()).strftime("%H:%M:%S"))

    @staticmethod
    def _is_valid_name(file_name: str) -> bool:
        """Returns whether or not the filename is allowed. If the logfile's
        name starts with, or is entirely whitespace, then it is considered an
        'illegal' filename.

        :param file_name: the name to check for validity.
        :type file_name: str
        """
    
        if re.match(INVALID_NAME, file_name) or file_name == "":
            return False
        else:
            return True

    def log(self, log_message: str, level: str = "DEBUG"):
        """Sends text to the console, or file with the specified
        message level.

        :param log_message: the log message
        :type log_message: str
        :param level: the level of the log message
        :type level: str
        :raises: ValueError
        """

        if not self.logger_enabled:
            return

        if level not in conversion_table.values():
            raise ValueError(f"{level} is not a valid logging level.")

        formatted_log: str = (self._format_message(level, self.log_string)
                              + " " + self._format_message(level, log_message))

        # Find the correct color for this log type.
        for color, assigned_mode in conversion_table.items():
            if assigned_mode == level:
                self._output_mode(color, formatted_log)
                break
