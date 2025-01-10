# ExLog

![Python](https://img.shields.io/badge/python-%3E%3D3.7-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)

**A lightweight, colorful, customizable Python logging utility with support for terminal output, file rotation, custom tags, and asynchronous logging; built for the Ex Projects, and YOURs too!**

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage Examples](#usage-examples)
4. [Feature Demonstrations](#feature-demonstrations)
5. [Custom Tags and Timestamps](#custom-tags-and-timestamps)
6. [Configuration](#configuration)
7. [Available Colors](#available-colors)
8. [Contributing](#contributing-explained)
9. [License](#license)
 
---

## Overview
`ExLog` is a flexible logging utility that supports both console and file-based logging with:
- Customizable log levels (`debug`, `info`, `warning`, `error`, `critical`).
- Colored output for better readability.
- File rotation by **time** (`daily`, `hourly`) and **size**.
- Asynchronous logging with minimal overhead.

---

## Installation
Install `ExLog` via pip:
```bash
pip install exlog
```

Ensure that `termcolor` is included for colored console output. Alternatively, include it in your `requirements.txt`.

To clone the repository:
```bash
git clone https://github.com/onedavidwilliams/ExLog.git
cd ExLog
```

---

## Minimum Python Version
`ExLog` requires **Python 3.7 or higher** to support `asyncio.run()`.

---

### How It Works:
- When you instantiate `ExLog`, you can set the minimum `log_level`. Only messages with a **numeric value greater than or equal** to the set level will be printed.
- You can specify the `log_level` using a **string** (e.g., `"debug"`, `"info"`, etc.) or **number** (`1`, `2`, etc.).

---

## Usage Examples:
### 1. **Log Level: `info` (1)**
```python
logger = ExLog(log_level="info")  # Same as log_level=1
logger.dprint("Info message", level="info")  # Printed
logger.dprint("Debug message", level=2)  # Not printed - Same as "debug"
```

### 2. **Log Level: `debug` (2)**
```python
logger = ExLog(log_level="debug")  # Same as log_level=2
logger.dprint("Debug message", level="debug")  # Printed
logger.dprint("Info message", level="info")  # Not Printed
```

### 3. **Log Level: `warning` (3)**
```python
logger = ExLog(log_level="warning")  # Same as log_level=3
logger.dprint("Warning message", level="warning")  # Printed
logger.dprint("Info message", level="info")  # Not Printed
logger.dprint("Debug message", level="debug")  # Not printed
```

### 4. **Basic Console Logging**
```python
from exlog import ExLog

logger = ExLog()  # Default log level: info, console-only
logger.dprint("Hello, World!", level="info")
```
**Output:**
```
[03:15:20 PM] [INFO] Hello, World!
```

---

### 5. **Logging to File with Daily Rotation**
```python
logger = ExLog(log_dir="my_logs", rotation="daily")
logger.dprint("Logging to file and terminal.", level="debug")
```
- Logs are saved in the `my_logs/` directory.
- New files are created daily.

---

### 6. **Async Logging**
```python
import asyncio
from exlog import ExLog

async def main():
    logger = ExLog(log_dir="my_logs", rotation="hourly")
    await logger.adprint("Async log message", level="info")

asyncio.run(main())
```
- Async-friendly logging for concurrent applications.

---

## Feature Demonstrations

### 1. **Size-Based Log File Rotation**
```python
logger = ExLog(log_dir="my_logs", max_file_size=1024 * 5)  # 5 KB max size
for i in range(100):
    logger.dprint(f"Message {i}", level="info")
```
- Automatically creates new log files when the size exceeds 5 KB.

---

### 2. **Custom Color Formatting**
```python
logger = ExLog(custom_colors={
    "info": {"color": ExLog.color.magenta},
    "warning": {"color": ExLog.color.blue, "background_color": ExLog.bg_color.yellow}
})
logger.dprint("Custom color for info.", level="info")
logger.dprint("Custom color for warning.", level="warning")
```

---

### 3. **Critical Log with Program Exit**
```python
def critical_exit_example(error=None):
    logger = ExLog()
    error = error if error else "No error specified"
    logger.dprint(f"Critical failure! Exiting program...\nError: {error}", level="critical")
    exit(1)

critical_exit_example("Test")
```
- Prints a critical log message and the error if one is passed and exits the program.

---

### 4. **Different Log Levels in Loop**
```python
log_levels = ["debug", "info", "warning", "error", "critical"]
logger = ExLog(log_dir="my_logs")

for i, level in enumerate(log_levels):
    logger.dprint(f"This is a {level.upper()} message", level=level)
```
- Cycles through all log levels to demonstrate their output.

---

## Custom Tags and Timestamps

`ExLog` provides flexibility with custom tags and timestamp options. You can add context to logs using custom tags and choose whether to display timestamps.

### 1. **Custom Tag Example**
```python
logger.dprint("System initialized", custom_tag="SYSTEM EVENT", color=ExLog.color.cyan)
```
**Output:**
```
[03:30:00 PM] [SYSTEM EVENT] System initialized
```

### 2. **Log Without Timestamp**
```python
logger.dprint("This log has no timestamp", show_timestamp=False)
```
**Output:**
```
[SYSTEM EVENT] This log has no timestamp
```

### 3. **Custom Log Level Without Predefined Tag**
If you do not specify a tag and use `level="custom"`, the message appears without any default tags.
```python
logger.dprint("This is a raw message", level="custom", show_timestamp=True)
```
**Output:**
```
[03:45:15 PM] This is a raw message
```

These options allow for more concise or context-rich logging depending on the situation.

---

## Configuration

### Initialization Parameters
| **Parameter**   | **Type** | **Default** | **Description** |
|-----------------|----------|-------------|-----------------|
| `log_level`     | `int`    | `1`         | Minimum log level to display (1 for "info", 2 for "debug", etc.). |
| `log_dir`       | `str`    | `None`      | Directory for log files. If `None`, logs only print to the console. |
| `log_file_prefix` | `str`  | "log"      | Prefix for log filenames. |
| `rotation`      | `str`    | "daily"    | Log rotation type: "daily", "hourly", or "none". |
| `max_file_size` | `int`    | `None`      | Maximum log file size (in bytes) before rotating to a new file. |
| `custom_colors` | `dict`   | `None`      | Dictionary for custom foreground and background colors. |

---

## Available Colors
You can set colors using `ExLog.color` (foreground) and `ExLog.bg_color` (background):

| **Foreground Colors (`ExLog.color`)** | **Background Colors (`ExLog.bg_color`)** |
|---------------------------------------|------------------------------------------|
| `black`                               | `on_black`                               |
| `red`                                 | `on_red`                                 |
| `green`                               | `on_green`                               |
| `yellow`                              | `on_yellow`                              |
| `blue`                                | `on_blue`                                |
| `magenta`                             | `on_magenta`                             |
| `cyan`                                | `on_cyan`                                |
| `white`                               | `on_white`                               |
| `grey`                                | `on_grey`                                |

---

## Contributing Explained
We are always looking for help and if you have never contributed to git and are wondering here is how:

To contribute to the `ExLog` project, follow these steps:

### **Step 1: Fork the Repository**
This creates a copy of the `ExLog` repository under your GitHub account. You will work on your forked copy rather than directly on the original project.

### **Step 2: Create a Feature Branch**
To keep your work organized and avoid conflicts, create a separate branch for your feature or fix:
```bash
git checkout -b my-feature-branch
```
This creates and switches to a new branch.

### **Step 3: Commit Your Changes**
After making your edits, save them locally by running:
```bash
git commit -m "Added new feature"
```
Make sure the commit message describes your changes clearly.

### **Step 4: Push Your Changes**
Send your changes from your local machine to your forked repository:
```bash
git push origin my-feature-branch
```
This pushes your branch to your GitHub repository.

### **Step 5: Open a Pull Request (PR)**
- Navigate to your forked repository on GitHub.
- GitHub will often show a "Compare & Pull Request" button at the top after a push.
- Click the button, provide a clear description of your changes, and submit your pull request.

The project maintainers will review your PR, and if everything looks good, they will merge your changes into the official project.

---

### Example PR Description - (This is going to a be a future upgrade)
> "This PR adds support for asynchronous file logging in addition to synchronous logging. Also included are updated tests to demonstrate async behavior."

By following these steps, you contribute effectively to the project and help maintain a smooth development process. Let me know if you'd like more details or examples!



---

