#!/usr/bin/python3

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PURPOSE:
This script formats files to fit a common pdf standard.
    - whitespace and other problematic symbols in the file name are substituted. 
    - pdfs are compressed with ghost script
    - pptx files are converted to pdf (the script will re-iterate over any new pdfs created)

USAGE:
Call the script with a folder name to clean all files in this folder on the first level. 
Any subdirectories are ignored. The user is prompted before script execution (defaults to YES). 

EXAMPLE USAGE: 
$ ./clean-files.py folder123/

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import re
import subprocess
import sys
#import time


def clean(folder_path, new_file_list=None):
    """ The file cleaning happens here. """
    # Switch for which list of files to use
    if new_file_list is None:
        # if no list is provided -> it's the first call to clean() -> new empty list of new_files will be filled
        print("\n--- Start cleaning ---")
        all_files = os.listdir(folder_path)
    else:
        # if list is provided use only these files
        print("\n--- Clean new files ---")
        all_files = new_file_list

    new_files = []  # list of new files (i.e. created from .pptx)

    # iterate over all files
    for filename in all_files:
        # Skip directories
        if os.path.isdir(os.path.join(folder_path, filename)):
            continue

        print("\nNew file:", filename)
        file_path = os.path.join(folder_path, filename)  # define the full file path
        file_ext = os.path.splitext(filename)[1]  # get the file extension / suffix

        # Rename file if it's not a PDF
        new_filename = re.sub(r'\s', '_', filename)  # Replace whitespace with _
        # new_filename = re.sub(r'\.(?=[^.]*\.)', '_', new_filename)  # Replace dots (except last before suffix) with _
        new_filename = re.sub(r'[ä]', 'ae', new_filename)  # Replace ä with ae
        new_filename = re.sub(r'[ü]', 'ue', new_filename)  # Replace ü with ue
        new_filename = re.sub(r'[ö]', 'oe', new_filename)  # Replace ö with oe
        new_filename = re.sub(r'[ß]', 'ss', new_filename)  # Replace ß with ss
        # Some windows conform file renaming
        new_filename = new_filename.replace(":", "-")
        new_filename = new_filename.replace("?", "-")
        new_filename = new_filename.replace("/", "-")
        new_filename = new_filename.replace("\\", "-")

        # Rename the file
        if new_filename != filename:
            new_file_path = os.path.join(folder_path, new_filename)
            os.rename(file_path, new_file_path)
            print(f'Renamed: {filename} -> {new_filename}')

            # Update the file path for further operations
            file_path = new_file_path

        # Convert PPTX files to PDF using LibreOffice
        if file_ext == '.pptx':
            pdf_filename = os.path.splitext(filename)[0] + '.pdf'
            pdf_file_path = os.path.join(folder_path, pdf_filename)
            subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', folder_path, file_path])
            print(f'Converted: {filename} -> {pdf_filename}')

            # Update the file path for further operations
            file_path = pdf_file_path
            filename = pdf_filename
            new_files.append(filename)

        # Compress PDF files using Ghostscript
        if file_ext == '.pdf':
            subprocess.run(['gs', '-o', file_path, '-sDEVICE=pdfwrite', file_path])
            print(f'Compressed ".pdf" file with gs: {filename}')

    return new_files



def userPrompt(folder_path):
    """ Prompt the user if the script should continue """
    n_files = len(os.listdir(folder_path))
    print(f"Folder '{os.path.abspath(folder_path)}' recognised.")
    print("Showing head of content:")
    [print(" -",file) for file in os.listdir(folder_path)[:5]]

    # User prompt before full execution
    answer = str(input(f"Clean {n_files} files and filenames here? [Y]/N ") or 'y').lower()
    if answer not in ("y", "yes"):
        sys.exit(f"Aborted by user! Answer was '{answer}'.")



def rename_files(folder_path=None):
    """
    Call the function to rename, convert, and compress files in the current folder.

    :param folder_path: optional argument
    :return:
    """
    if folder_path is None:
        folder_path = os.getcwd()  # Set current folder as default

    # Prompt the user if the script should continue
    userPrompt(folder_path)

    script_directory = os.path.dirname(os.path.abspath(__file__))
    new_files = clean(folder_path=folder_path)

    # if new_files where created i.e. from pptx -> pdf
    # then call clearn again
    if new_files:
        clean(folder_path=folder_path, new_file_list=new_files)




if __name__ == '__main__':

    # Check if the folder path argument is provided
    if len(sys.argv) > 1:
        # Pass the folder path as an argument when calling the function
        folder_path = sys.argv[1]
    else:
        folder_path = None

    # Call the function to rename, convert, and compress files in the current folder
    rename_files(folder_path)
