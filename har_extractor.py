# -*- coding: utf-8 -*-
"""
HAR Content Extractor

A command-line tool to extract and save all files, API responses, and web assets
from a HAR (.har) archive.
"""

import json
import base64
import os
import re
import argparse
from urllib.parse import urlparse
import binascii  # Required for specific exception handling

def main(har_filepath: str, output_dir: str) -> None:
    """
    Parses a HAR file to extract and save all HTTP response bodies.

    Args:
        har_filepath (str): The path to the input .har file.
        output_dir (str): The directory where extracted files will be saved.
    """
    # Ensure the output directory exists, creating it if necessary.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Attempt to read and parse the HAR file.
    try:
        with open(har_filepath, 'r', encoding='utf-8') as f:
            har_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{har_filepath}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: '{har_filepath}' is not a valid JSON file.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    # Iterate through each HTTP request-response pair in the HAR log.
    for idx, entry in enumerate(har_data['log']['entries']):
        # --- Step 1: Decode the response content ---

        # Skip entries that have no response content, e.g., 304 Not Modified.
        if 'content' not in entry['response'] or 'text' not in entry['response']['content']:
            continue

        url = entry['request']['url']
        content = entry['response']['content']
        encoding = content.get('encoding')
        
        data: bytes
        if encoding == 'base64':
            # Handle Base64 encoded content, typically for binary files like images.
            try:
                data = base64.b64decode(content['text'])
            except (ValueError, binascii.Error) as e:
                print(f"Warning: Could not decode Base64 content from {url}. Skipping. Error: {e}")
                continue
        else:
            # Assume plain text and encode to UTF-8 bytes.
            data = content['text'].encode('utf-8')
        
        # --- Step 2: Construct a safe and descriptive filename from the URL ---

        parsed_url = urlparse(url)
        
        # Start with the last part of the URL path (e.g., 'script.js' from '/js/script.js').
        filename = os.path.basename(parsed_url.path)
        
        # If the path is empty (e.g., 'https://example.com/'), use the netloc.
        if not filename:
            filename = parsed_url.netloc

        # Append the query string to the filename to preserve uniqueness for API calls.
        if parsed_url.query:
            # Sanitize the query string to be filesystem-friendly.
            safe_query = re.sub(r'[\\/*?:"<>|]', '_', parsed_url.query)
            filename = f"{filename}?{safe_query}"
        
        # A final, aggressive sanitization to remove any remaining illegal characters.
        # This is a critical step for ensuring compatibility with all major OS.
        filename = re.sub(r'[\\/*?:"<>|]', '', filename)

        # If, after all processing, the filename is empty, create a default name.
        if not filename:
            filename = f"default_filename_{idx}"

        # --- Step 3: Write the decoded content to a file ---

        save_path = os.path.join(output_dir, filename)
        
        try:
            with open(save_path, 'wb') as f:
                f.write(data)
            print(f"Saved: {save_path}")
        except OSError as e:
            # Handle filesystem errors, e.g., filename too long or permission denied.
            print(f"Error: Could not write file {save_path}. OS Error: {e}")
        except Exception as e:
            print(f"An unknown error occurred while saving {save_path}: {e}")


if __name__ == "__main__":
    # This block sets up the command-line interface for the script.
    parser = argparse.ArgumentParser(
        description="Extracts and saves all HTTP response bodies from a HAR file.",
        epilog="Example: python har_extractor.py my_archive.har -o extracted_files"
    )
    
    parser.add_argument(
        "har_file",
        help="The path to the input .har file."
    )
    
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="The directory to save the extracted files (default: 'output')."
    )

    # Parse the arguments provided by the user.
    args = parser.parse_args()

    # Call the main function with the parsed arguments.
    main(args.har_file, args.output)
