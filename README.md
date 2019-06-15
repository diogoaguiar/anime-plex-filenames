# Anime Plex Filenames
Python script used to rename anime episodes from HorribleSubs to the Plex format and move them into the the Plex library, while applying the correct file structure.

## Setup
### Needs
- Pyhton 3.7+

### Configuration
1. Create a copy of the `config.json.example` and rename it to `config.json`. 
2. Edit the `config.json` and set the fields to match your system and usage:
    - **regex**: The regex used to parse the original filenames.
        - The script expects the named groups: `show`, `season`, `episode` and `ext`.
        - Also supports a list with various regex entries. The script will try to match the filenames with each of the entries, in the given order, until it finds a match.
        - The given example is set to match HorribleSubs filenames only. You will need to modify the regex (or append new entries) to work with other website releases.
    - **from_path**: Path to the directory where the files that need processing are located.
    - **to_path**: Path to the directory of the Plex library, where the shows folders are located.

## Usage
Run the python script `move-and-rename.py`, like so:
```shell
$ python move-and-rename.py
```
Make sure that `python` refers to the Python v3.7+ installation, otherwise adjust the command to use the correct alias (`python3`, `python3.7`, etc.).