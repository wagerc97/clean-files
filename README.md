# Clean Files

## PURPOSE:
This script formats files to fit a common pdf standard.
    - whitespace and other problematic symbols in the file name are substituted. 
    - pdfs are compressed with ghost script
    - pptx files are converted to pdf (the script will re-iterate over any new pdfs created)

## USAGE:
Call the script with a folder name to clean all files in this folder on the first level. 
Any subdirectories are ignored. The user is prompted before script execution (defaults to YES). 

### EXAMPLE USAGE: 
$ ./clean-files.py folder123/
