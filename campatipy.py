#!/usr/bin/python3

"""
PURPOSE:
This script formats files to fit a common PDF standard, making them machine-readable:
- Replaces problematic symbols in filenames.
- Compresses PDFs using Ghostscript.
- Converts PPTX files to PDF (handles newly created PDFs recursively).

USAGE:
Call the script with a folder path to clean all files in the specified folder.
Subdirectories are ignored. The user is prompted before execution.

EXAMPLE:
    ./clean-files.py /path/to/folder
"""

import os
import re
import shutil
import subprocess
import sys


def sanitize_filename(filename):
    """Sanitize filenames by replacing problematic characters."""
    substitutions = {
        r'\s': '_',   # Replace whitespace with underscore
        r'[ä]': 'ae', r'[ü]': 'ue', r'[ö]': 'oe', r'[ß]': 'ss',  # Replace German umlauts
        r'[:?/\\]': '-',  # Replace forbidden symbols
    }
    for pattern, replacement in substitutions.items():
        filename = re.sub(pattern, replacement, filename)
    return filename


def convert_pptx_to_pdf(file_path, output_folder):
    """Convert PPTX files to PDF using LibreOffice."""
    try:
        subprocess.run(
            ['soffice', '--headless', '--convert-to', 'pdf', '--outdir', output_folder, file_path],
            check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print(f"Converted PPTX to PDF: {os.path.basename(file_path)}")
        return os.path.splitext(file_path)[0] + '.pdf'
    except Exception as e:
        print(f"Error converting {file_path} to PDF: {e}")
        return None


def compress_pdf(file_path):
    """
    Compress PDF files using Ghostscript.

    EXPLANATION
        This command takes the input PDF (file_path), compresses it, adjusts its compatibility to PDF version 1.4,
        and saves the output in the specified temp_file. If the process succeeds, the temporary file replaces the
        original file, ensuring the compressed version is saved without directly overwriting the original until
        processing completes.
    """
    try:
        temp_file = file_path + '.tmp'
        subprocess.run(
            ['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dNOPAUSE', '-dQUIET', '-dBATCH', '-sOutputFile=' + temp_file, file_path],
            check=True
        )
        os.replace(temp_file, file_path)  # Replace original file with compressed file
        print(f"Compressed PDF: {os.path.basename(file_path)}")
    except Exception as e:
        print(f"Error compressing {file_path}: {e}")


def clean_folder(folder_path, target_files=None):
    """Clean filenames, convert PPTX to PDF, and compress PDFs."""
    target_files = target_files or os.listdir(folder_path)
    new_files = []

    for filename in target_files:
        full_path = os.path.join(folder_path, filename)

        if os.path.isdir(full_path):
            print(f"Skipping directory: {filename}")
            continue

        sanitized_name = sanitize_filename(filename)
        if sanitized_name != filename:
            sanitized_path = os.path.join(folder_path, sanitized_name)
            os.rename(full_path, sanitized_path)
            print(f"Renamed: {filename} -> {sanitized_name}")
            full_path = sanitized_path

        file_ext = os.path.splitext(sanitized_name)[1].lower()

        if file_ext == '.pptx':
            new_pdf = convert_pptx_to_pdf(full_path, folder_path)
            if new_pdf:
                new_files.append(os.path.basename(new_pdf))

        elif file_ext == '.pdf':
            compress_pdf(full_path)

    return new_files


def confirm_and_execute(folder_path):
    """Prompt the user for confirmation before executing the script."""
    folder_content = os.listdir(folder_path)
    n_files = len(folder_content)

    print(f"Cleaning {n_files} files in folder: {os.path.abspath(folder_path)}")
    print("Sample content:")
    for file in folder_content[:5]:
        print(f" - {file}")

    answer = input("Proceed with cleaning? [Y]/N: ").strip().lower() or 'y'
    if answer not in ('y', 'yes'):
        print("Operation canceled by the user.")
        sys.exit(0)

    new_files = clean_folder(folder_path)

    if new_files:
        print("\nProcessing newly created files...")
        clean_folder(folder_path, target_files=new_files)


def main():
    if len(sys.argv) != 2:
        print("Usage: ./clean-files.py /path/to/folder")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        sys.exit(1)

    # Ensure required tools are installed
    for tool in ['soffice', 'gs']:
        if not shutil.which(tool):
            print(f"Error: Required tool '{tool}' is not installed or not in PATH.")
            sys.exit(1)

    confirm_and_execute(folder_path)


if __name__ == '__main__':
    main()
