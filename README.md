# PyCrasher

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

**PyCrasher** is a Python utility for forcibly terminating processes on a Windows machine by their Process ID (PID) or process name. Inspired by low-level Windows programming, PyCrasher leverages the `ctypes` library to interact with the Windows API.

⚠️ **Warning:** This tool is for educational purposes only. Use it responsibly and ethically. Improper use can lead to data loss or system instability. Always ensure you have the necessary permissions to terminate processes.

## Features

- **Crash by PID:** Terminate a process using its PID.
- **Crash by Name:** Terminate all processes matching a given name.

## Installation

### Method 1

You can download an optimized and pre compiled release [here](https://github.com/JancoNel-dev/PyCrasher/releases/tag/V1)

### Method 2

1. Clone the repository:
    ```bash
    git clone https://github.com/JancoNel-dev/pycrasher.git
    cd pycrasher
    ```
2. Ensure you have Python 3.x installed on your system.
3. Run the main file
    ```bash
    start.bat
    ```

## Usage

Run the script with administrator privileges to ensure it has the necessary permissions to terminate processes.

### Command Line

- Crash a process by its PID:
    ```bash
    python main.py <PID>
    ```

- Crash processes by name:
    ```bash
    python main.py <ProcessName>
    ```

### Examples

- Terminate a process with PID `1234`:
    ```bash
    python main.py 1234
    ```

- Terminate all instances of `notepad.exe`:
    ```bash
    python main.py notepad.exe
    ```

## Code Structure

- `main.py`: The main script containing the logic for terminating processes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for educational purposes only. The author is not responsible for any damage caused by the use of this tool. Use it responsibly and only on systems you have permission to operate on.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For issues or questions, please open an issue on the [GitHub repository](https://github.com/yourusername/pycrasher).

---

*Happy crashing!*

