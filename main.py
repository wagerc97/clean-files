#!/usr/bin/python3

import os
import re
import subprocess
import sys


def rename_files(folder_path=None):
    """
    Call the function to rename, convert, and compress files in the current folder.

    USAGE:
     Can be called like this:
      ./main.py sysevo

    :param folder_path: optional argument
    :return:
    """
    if folder_path is None:
        folder_path = os.getcwd()  # Set current folder as default

    n_files = len(os.listdir(folder_path))
    print(f"Clean all {n_files} files and filenames in", folder_path)

    # User prompt before full execution
    answer = str(input("Continue here? (y|n) ")).lower()
    if answer not in ("y", "yes"):
        sys.exit(f"Aborted by user! Answer was '{answer}'.")

    script_directory = os.path.dirname(os.path.abspath(__file__))

    # iterate over all files
    for filename in os.listdir(folder_path):
        # Skip directories
        if os.path.isdir(os.path.join(folder_path, filename)):
            continue

        print("\nNew file:", filename)
        file_path = os.path.join(folder_path, filename) # define the full file path
        file_ext = os.path.splitext(filename)[1]    # get the file extension / suffix

        # Rename file if it's not a PDF
        new_filename = re.sub(r'\s', '_', filename)  # Replace whitespace with _
        #new_filename = re.sub(r'\.(?=[^.]*\.)', '_', new_filename)  # Replace dots (except last before suffix) with _
        new_filename = re.sub(r'[ä]', 'ae', new_filename)  # Replace ä with ae
        new_filename = re.sub(r'[ü]', 'ue', new_filename)  # Replace ü with ue
        new_filename = re.sub(r'[ö]', 'oe', new_filename)  # Replace ö with oe
        new_filename = re.sub(r'[ß]', 'ss', new_filename)  # Replace ß with ss

        # Rename the file
        if new_filename != filename:
            new_file_path = os.path.join(folder_path, new_filename)
            os.rename(file_path, new_file_path)
            print(f'Renamed: {filename} -> {new_filename}')

            # Update the file path for further operations
            file_path = new_file_path

        # Convert PPTX files to PDF using LibreOffice
        #if file_ext == '.pptx':
        #    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', file_path])
        #    print(f'Converted ".pptx" file: {filename} -> PDF')

        # Convert PPTX files to PDF using LibreOffice
        if file_ext == '.pptx':
            pdf_filename = os.path.splitext(filename)[0] + '.pdf'
            pdf_file_path = os.path.join(folder_path, pdf_filename)
            subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', folder_path, file_path])
            print(f'Converted: {filename} -> {pdf_filename}')

            # Update the file path for further operations
            file_path = pdf_file_path
            filename = pdf_filename

        # Compress PDF files using Ghostscript
        if file_ext == '.pdf':
            subprocess.run(['gs', '-o', file_path, '-sDEVICE=pdfwrite', file_path])
            print(f'Compressed ".pdf" file with gs: {filename}')



if __name__ == '__main__':

    # Check if the folder path argument is provided
    if len(sys.argv) > 1:
        # Pass the folder path as an argument when calling the function
        folder_path = sys.argv[1]
    else:
        folder_path = None

    # Call the function to rename, convert, and compress files in the current folder
    rename_files(folder_path)
