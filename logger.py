"""A small, lightweight Logger written in Python. Mainly created
because I dislike the already existing Logger module in the Python
Standard Library, also because I can sent colored-text directly
through this. 
"""

import re
import time
import colorama
from pathlib import Path
from datetime import datetime as dt

colorama.init(autoreset=True)

root_dir = Path(__file__).absolute().parents[0]
log_dir = root_dir / Path("logs")

# Color constants
reset = colorama.Fore.RESET
debug = colorama.Fore.WHITE
success = colorama.Fore.GREEN
info = colorama.Fore.LIGHTBLACK_EX
warning = colorama.Fore.LIGHTYELLOW_EX
critical = colorama.Fore.LIGHTRED_EX

conversion_table = {
    debug: "DEBUG",
    info: "INFO",
    success: "SUCCESS",
    warning: "WARNING",
    critical: "CRITICAL"
}


class Logger():
    """A Python implementation of a "Logger."

    :param _log_string: the string, along with it's "format specifiers", that
    is appended to the end of each log message
    :type _log_string: str

    :param logger_directory: the directory to output the logfile to
    :type logger_directory: Pathlike, str

    :param _logger_name: the name of the logger, defaults to ROOT
    :type _logger_name: str, optional

    :param _log_mode: how the logger logs text
        c  - log to console
        f  - log to file
        cf - log to console, and file.
    :type _log_mode: str
    :param logfile_name: the name of the logfile.
    :type logfile_name: str, defaults to the current date when an empty string,
    or a fully-whitespace name is given

    :param _logger_enabled: whether or not the logger is allowed to log messages
    :type _logger_enabled: bool, optional, defaults to True

    :param _color_enabled: whether or not color is enabled in the console
    :type _color_enabled: bool, optional, defaults to True

    :param _file_colors: whether or not to send color data to files. usually
    used for printing the log message's colors to be more readable.
    :type _file_colors: bool, optional, defaults to False 

    :param make_logger_dir: whether or not to make the logger_directory if it
    doesn't exist.
    :type make_logger_dir: bool, optional, defaults to False
    """

    def __init__(self, log_string: str, logger_directory: str,
                 logger_name="ROOT", log_mode="c", logfile_name="",
                 logger_enabled=True, color_enabled=True, file_colors=False,
                 make_logger_dir=False):

        # Create the file to log messages to.
        self._log_string = log_string
        self._logger_name = logger_name
        self._logger_enabled = logger_enabled
        self._log_mode = log_mode
        self._file_colors = file_colors
        self._color_enabled = color_enabled

        # If the logfile's name starts with, or is entirely whitespace,
        # give it a name of the current date.
        if not re.match("^\s*", logfile_name) or logfile_name == "":
            logfile_name = f"{dt.fromtimestamp(time.time()).strftime('%Y-%m-%d')}.log"

        # Validate the log mode.
        if not all(op in "cf" for op in log_mode):
            raise ValueError("_log_mode must only contain characters 'cf'!")
        
        # Logfile & Directory creation
        if not Path(logger_directory).exists():
            Path(logger_directory).mkdir(parents=make_logger_dir)

        _file_path = Path(logger_directory).absolute() / Path(logfile_name)
        self._logfile_path = _file_path
        self._log_file = open(_file_path, "a+")

    def _format_message(self, level: str, message: str) -> str:
        """Creates a formatted message using _log_string.
    
        :param message: the message to format.
        :type message: str
        :param level: the level of the message
        :type level: str
        :return: the formatted message
        :rtype: str

        Availible specifiers:
            %D - The current date.
            %T - The current time.
            %N - The logger's _logger_name.
            %L - The message's level.
            %% - An escaped percent sign.
        """

        specifiers = {
            "%D": lambda: dt.fromtimestamp(time.time()).strftime("%Y-%m-%d"),
            "%T": lambda: dt.fromtimestamp(time.time()).strftime("%H:%M:%S"),
            "%N": lambda: self._logger_name,
            "%L": lambda: level,
            "%%": lambda: "%"
        }

        formatted = "".join(message)

        for specifier, repl in specifiers.items():
            formatted = formatted.replace(specifier, repl())

        return formatted

    def _output_mode(self, message_type: str, output_message: str):
        """Goes through the format _log_mode and outputs it to the output specifier.

        :param message_type: the color from colorama to use
        :type message_type: str
        :param output_message: the message to send to the console or logfile.
        :type output_message: str
        
        Output specifiers:
           c  - Output to the console
           f  - Output to the log file.
           cf - Output to the console AND log file.
        """

        for specifier in self._log_mode:
            # Console specifier
            if specifier == "c":
                if self._color_enabled:
                    print(message_type + output_message)
                else:
                    print(output_message)

            # Logfile specifier. If _log_file is None, there is no file to log
            # the output to.
            if specifier == "f" and self._log_file is not None:
                # Wont send color information to the logfile.
                if not self._file_colors:
                    self._log_file.write(output_message + "\n")
                    self._log_file.flush()

                # Will send color information to the logfile.
                else:
                    self._log_file.write(message_type + output_message + reset + "\n")
                    self._log_file.flush()

    def debug(self, debug_message: str):
        """Sends text to the console, or file with white text.

        :param debug_message: the debug message
        :type debug_message: str
        """

        if not self._logger_enabled:
            return 

        formatted_debug: str = self._format_message("DEBUG", self._log_string) \
                             + " " + self._format_message("DEBUG", debug_message)

        self._output_mode(debug, formatted_debug)

    def info(self, info_message: str):
        """Sends text to the console, or file with grey text.

        :param info: the info message
        :type info: str
        """

        if not self._logger_enabled:
            return

        formatted_info: str = self._format_message("INFO", self._log_string) \
                            + " " + self._format_message("INFO", info_message)

        self._output_mode(info, formatted_info)

    def success(self, success_message: str):
        """Sends text to the console, or file with green text.

        :param success_message: the success message
        :type success_message: str
        """

        if not self._logger_enabled:
            return 

        formatted_success: str = self._format_message("SUCCESS", self._log_string) \
                                 + " " + self._format_message("SUCCESS", success_message)

        self._output_mode(success, formatted_success)

    def warn(self, warning_message: str):
        """Sends text to the console, or file with yellow text.

        :param warning_message: the warning message
        :type warning_message: str
        """

        if not self._logger_enabled:
            return 

        formatted_warning: str = self._format_message("WARNING", self._log_string) \
                               + " " + self._format_message("WARNING", warning_message)

        self._output_mode(warning, formatted_warning)

    def critical(self, critical_message: str):
        """Sends text to the console, or file with red text.

        :param critical_message: the critical_message
        :type critical_message: str
        """

        if not self._logger_enabled:
            return 

        formatted_critical: str = self._format_message("CRITICAL", self._log_string) \
                                + " " + self._format_message("CRITICAL", critical_message)

        self._output_mode(critical, formatted_critical)

