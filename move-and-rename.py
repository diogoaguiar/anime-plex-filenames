import re
import os
import shutil
import json

# Defaults
from_path = os.path.expanduser("~/Downloads/")
to_path = os.path.expanduser("~/Videos/Plex/")
regex = r"^\[(?P<dist>\w+)\]\s?(?P<show>[A-za-z0-9\s\-\(\)\!\']+?)\s?S?(?P<season>\d+)?\s?\-\s?(?P<episode>\d+\.?\d+?)v?(?P<version>\d+)?\s?\[(?P<quality>\d+p)\]\.?(?P<ext>[a-z0-9\-]+)?$"

# Load configs
try:
    config_path = os.path.dirname(os.path.abspath(__file__)) + "/config.json"
    with open(config_path) as json_config:
        config = json.load(json_config)
        if "from_path" in config.keys():
            from_path = os.path.expanduser(config["from_path"])
            print("Loaded 'from_path' from the config file.")
        else:
            print("Using the default 'from_path'.")

        if "to_path" in config.keys():
            to_path = os.path.expanduser(config["to_path"])
            print("Loaded 'to_path' from the config file.")
        else:
            print("Using the default 'to_path'.")

        if "regex" in config.keys():
            regex = list(config["regex"])
            print("Loaded 'regex' from the config file.")
        else:
            print("Using the default 'regex'.")

        print("Config file 'config.json' loaded successfully.")

except Exception as e:
    print("Couldn't load one or more parameters from 'config.json'. Will assume program defaults.")
    print(e)

# Validate configs
if not os.path.exists(from_path):
    print("from_path '%s' does not exist." % from_path)
    quit()

if not os.path.exists(to_path):
    print("to_path '%s' does not exist." % to_path)
    quit()

try:
    if type(regex) is not list:
        regex = [regex]

    for i, reg in enumerate(regex):
        regex[i] = re.compile(reg)

except:
    print("regex is not a valid python regular expression.")
    quit()


# Methods
def is_float(s):
    try:
        int(s)
        return False
    except:
        try:
            float(s)
            return True
        except:
            return False

# Main
from_dir = os.fsencode(from_path)
files_from_dir = os.listdir(from_dir)

print("There are %d files in '%s'." % (len(files_from_dir), from_path))

for file in files_from_dir:
    filename = os.fsdecode(file)
    print("\nFile: '%s'" % filename)

    m = None
    for i, reg in enumerate(regex):
        m = reg.match(filename)
        if m:
            print("Filename matches the regex #%d" % i+1)
            break

    if not m:
        print("Filename doesn't match any regex.")
        continue

    season = m.group("season") if m.group("season") is not None else '1'
    if is_float(m.group("episode")):
        season = '0'
    e = {
        "show": m.group("show"),
        "episode": m.group("episode").zfill(2),
        "season": season.zfill(2),
        "ext": m.group("ext")
    }
    print(e)

    plex_path = to_path + ("%s/Season %s/" % (e["show"], e["season"]))
    plex_file = "%s - S%sE%s.%s" % (e["show"], e["season"], e["episode"], e["ext"])
    plex_full_filename = plex_path+plex_file
    # print(plex_full_filename)

    try:
        if not os.path.exists(plex_path):
            print("Creating directories to the path '%s'." % plex_path)
            os.makedirs(plex_path)

        print("Moving file '%s' -> '%s'" % (from_path + filename, plex_full_filename))
        shutil.move(from_path + filename, plex_full_filename)
        print("File moved successfully.")
    except Exception as e:
        print("Error moving the file.")
        print(e)

print("Done.")
