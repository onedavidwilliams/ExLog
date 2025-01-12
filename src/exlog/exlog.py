import os
from termcolor import colored
from datetime import datetime
import asyncio
import re

class ExLog:
    class color:
        black = "black"
        red = "red"
        green = "green"
        yellow = "yellow"
        blue = "blue"
        magenta = "magenta"
        cyan = "cyan"
        white = "white"
        grey = "grey"

    class bg_color:
        black = "on_black"
        red = "on_red"
        green = "on_green"
        yellow = "on_yellow"
        blue = "on_blue"
        magenta = "on_magenta"
        cyan = "on_cyan"
        white = "on_white"
        grey = "on_grey"

    def __init__(self, log_level=1, log_dir=None, log_file_prefix="log", rotation="daily", max_file_size=None, custom_colors=None):
        """
        Initialize the ExLog logger with configurable log level, file logging options, and rotation strategies.

        Args:
            log_level (int): Verbosity level for logging messages.
            log_dir (str, optional): Directory where log files will be saved. If provided, file logging is enabled.
            log_file_prefix (str): Prefix for log filenames.
            rotation (str): Log file rotation strategy ("daily", "hourly", or "none").
            max_file_size (int, optional): Maximum log file size (in bytes) before creating a new part file.
            
            custom_colors (dict, optional): Custom color configuration for different log levels.
                Example:
                    {
                        "debug": {"color": ExLog.color.red},
                        "info": {"color": ExLog.color.yellow, "background_color": ExLog.bg_color.red},
                        "error": {"color": "yellow"},
                        ... etc
                    }
        """
        self.log_level = log_level
        self.log_to_file = log_dir is not None
        self.rotation = rotation
        self.max_file_size = max_file_size
        self.log_dir = log_dir
        self.log_file_prefix = log_file_prefix
        self.file_part = 0
        self.current_log_file = None
        self.last_log_time = None

        # Merge custom colors with default colors
        self.default_colors = {
            "debug": {"color": ExLog.color.cyan},
            "info": {"color": ExLog.color.green},
            "warning": {"color": ExLog.color.yellow, "background_color": ExLog.bg_color.grey},
            "error": {"color": ExLog.color.red, "background_color": ExLog.bg_color.white},
            "critical": {"color": ExLog.color.white, "background_color": ExLog.bg_color.red}
        }

        if custom_colors:
            self.default_colors.update(custom_colors)

        if self.log_to_file:
            os.makedirs(log_dir, exist_ok=True)
            self.current_log_file = self._get_current_log_file()

    def _get_current_log_file(self):
        """Determine the log file name based on the rotation strategy and size."""
        now = datetime.now()

        if self.rotation == "daily":
            date_str = now.strftime("%Y-%m-%d")
        elif self.rotation == "hourly":
            date_str = now.strftime("%Y-%m-%d_%H")
        else:  # "none"
            date_str = "static"

        base_filename = f"{self.log_file_prefix}_{date_str}.log"
        base_file_path = os.path.join(self.log_dir, base_filename)

        # Scan existing files to find the highest part number upon restart
        if self.file_part == 0:  # Only check if we haven't already detected it
            highest_part = 0
            pattern = re.compile(rf"{re.escape(self.log_file_prefix)}_{date_str}_(\d+)\.log")
            for filename in os.listdir(self.log_dir):
                match = pattern.match(filename)
                if match:
                    part_number = int(match.group(1))
                    highest_part = max(highest_part, part_number)

            self.file_part = highest_part

        # Time-based rotation check
        if self.last_log_time is None or \
           (self.rotation == "daily" and self.last_log_time.date() != now.date()) or \
           (self.rotation == "hourly" and self.last_log_time.hour != now.hour):
            self.file_part = 0  # Reset part counter for new time period
            self.last_log_time = now
            self.current_log_file = base_file_path

        # Size-based rotation check
        if self.max_file_size and os.path.exists(self.current_log_file) and os.path.getsize(self.current_log_file) >= self.max_file_size:
            self.file_part += 1
            part_filename = f"{self.log_file_prefix}_{date_str}_{self.file_part:03}.log"
            self.current_log_file = os.path.join(self.log_dir, part_filename)

        return self.current_log_file

    def _write_to_log_file(self, message):
        """Write a message to the log file."""
        if not self.log_to_file:
            return

        log_file = self._get_current_log_file()

        with open(log_file, "a") as f:
            f.write(message + "\n")

    def _format_message(self, message, level_name, show_timestamp, time_format, custom_tag):
        """Format the message with optional timestamp."""
        timestamp = ""
        if show_timestamp:
            time_format_str = "%I:%M:%S %p" if time_format == "12hr" else "%H:%M:%S"
            timestamp = datetime.now().strftime(time_format_str)
            timestamp = f"[{timestamp}] "
        if level_name == "CUSTOM" and not custom_tag:
                return f"{timestamp}{message}"
        return f"{timestamp}[{level_name.upper()}] {message}"

    def dprint(self, message, level=None, color=None, background_color=None, show_timestamp=True, time_format="24hr", custom_tag=None):
        """
        Print a message with optional color, timestamp, and a custom tag.
        """
        level = level if level is not None else self.log_level
        numeric_level, level_name = self._resolve_level(level)
        if numeric_level == 0:
            return
        if numeric_level >= self.log_level:
            # Use the custom tag if provided
            level_name = custom_tag if custom_tag else level_name.upper()

            # Use default colors if not provided
            if level_name.lower() in self.default_colors:
                if not color:
                    color = self.default_colors[level_name.lower()].get("color")
                if not background_color:
                    background_color = self.default_colors[level_name.lower()].get("background_color")

            formatted_message = self._format_message(message, level_name, show_timestamp, time_format, custom_tag)

            if color or background_color:
                print(colored(formatted_message, color=color, on_color=background_color))
            else:
                print(formatted_message)

            # Log to file if enabled
            self._write_to_log_file(formatted_message)

    async def adprint(self, message, level=0, color=None, background_color=None, show_timestamp=True, time_format="24hr", custom_tag=None):
        """
        Asynchronously print a message with optional color, timestamp, and a custom tag.
        """
        
        level = level if level is not None else self.log_level
        numeric_level, level_name = self._resolve_level(level)

        if numeric_level == 0:
            return

        if numeric_level >= self.log_level and numeric_level > 0:
            # Use the custom tag if provided
            level_name = custom_tag if custom_tag else level_name.upper()

            # Use default colors if not provided
            if level_name.lower() in self.default_colors:
                if not color:
                    color = self.default_colors[level_name.lower()].get("color")
                if not background_color:
                    background_color = self.default_colors[level_name.lower()].get("background_color")

            formatted_message = self._format_message(message, level_name, show_timestamp, time_format, custom_tag)

            if color or background_color:
                print(colored(formatted_message, color=color, on_color=background_color))
            else:
                print(formatted_message)

            # Log to file if enabled
            self._write_to_log_file(formatted_message)

        await asyncio.sleep(0)  # Yield control to event loop

    level_map = {
        "notset": 0,
        "info": 1,
        "debug": 2,
        "warning": 3,
        "error": 4,
        "critical": 5
    }

    def _resolve_level(self, level):
        """
        Convert descriptive level to numeric value and return both numeric and descriptive names.
        
        Args:
            level (str or int): The logging level (e.g., "debug", 2).
        
        Returns:
            tuple: (numeric_level, level_name)
        """
        if isinstance(level, str):
            level_lower = level.lower()
            numeric_level = self.level_map.get(level_lower, 2)  # Default to debug level
            return numeric_level, level_lower
        else:
            # Convert numeric level to string name (fallback to "custom" if not found)
            level_name = next((name for name, num in self.level_map.items() if num == level), "custom")
            return level, level_name