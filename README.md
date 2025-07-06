# HAR Content Extractor

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool to extract and save all files, API responses, and web assets from a HAR (`.har`) archive.

---

## What problem does this solve?

This script addresses the common need to extract all resources from a web session for offline analysis, debugging, or bulk downloading. Manually saving each file from a browser's developer tools is tedious and impractical, especially for modern web applications with numerous API calls and dynamically loaded assets. 

This tool automates the entire process: simply save your network activity as a HAR file, and this script will unpack everything into a local directory for you.

## Features

*   **Automatic HAR Parsing**: Natively processes standard `.har` files without any configuration.
*   **Base64 Decoding**: Automatically detects and decodes Base64 encoded content, typically used for images and fonts.
*   **Filename Sanitization**: Cleans filenames by removing characters that are illegal in common operating systems (`\ / : * ? " < > |`), ensuring cross-platform compatibility.
*   **Handles Ambiguous URLs**: Generates logical default filenames for requests that don't point to a specific file (e.g., API endpoints like `/api/user/123`).
*   **Zero Dependencies**: Uses only Python's standard library. No `pip install` required.
*   **Simple CLI**: A straightforward command-line interface for easy operation.

## How to Use

### 1. Obtain a HAR File

First, you need to capture the network activity from your browser and save it as a `.har` file.

1.  On the target website, open your browser's **Developer Tools** (usually by pressing `F12`).
2.  Navigate to the **Network** tab.
3.  Ensure the "Preserve log" option is checked if you need to capture activity across multiple pages.
4.  Perform the actions on the website that you want to record (e.g., refresh the page, click buttons, submit forms).
5.  Once you see the network requests appear in the log, right-click anywhere on the list of requests.
6.  Select **"Save all as HAR with content"**.
7.  Save the file to your computer (e.g., `my_archive.har`).

### 2. Run the Script

Place the `har_extractor.py` script in the same directory as your `.har` file, or ensure it's in your system's PATH. Open your terminal or command prompt and run the script.

**Basic Usage**

This command will read `my_archive.har` and save all extracted files into a new folder named `output` in the current directory.

```bash
python har_extractor.py my_archive.har
```

**Specifying an Output Directory**

Use the `-o` or `--output` flag to save files to a custom directory.

```bash
python har_extractor.py my_archive.har --output ./downloaded_assets
```

**Get Help**

To see all available options, use the `--help` flag.

```bash
python har_extractor.py --help
```

### Example

**Before:**
Your directory contains the script and the captured HAR file.

```
/my-project
├── har_extractor.py
└── example.har
```

**After running `python har_extractor.py example.har`:**
The script creates an `output` directory and populates it with the extracted content.

```
/my-project
├── har_extractor.py
├── example.har
└── output/          <-- Automatically created
    ├── index.html
    ├── style.css
    ├── logo.png
    └── user?id=123&type=customer
```

## License

This project is licensed under the MIT License.
