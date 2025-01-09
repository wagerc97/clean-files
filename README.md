# Clean Files

## PURPOSE:
This script formats files to fit a common pdf standard making them machine readable. 
- whitespace and other problematic symbols in the file name are substituted. 
- pdfs are compressed with ghost script
- pptx files are converted to pdf (the script will re-iterate over any new pdfs created)

## USAGE:
Call the script with a folder name to clean all files in this folder on the first level. 
Any subdirectories are ignored. The user is prompted before script execution. 

### EXAMPLE USAGE: 

```bash
./clean-files.py ./path/to/folder/
```