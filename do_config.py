#!/usr/bin/env python

"""Generates the extractor_info.json file from the configuration file
"""
import os
import copy
import json
import re
import sys
import shutil
import subprocess
import configuration

# The extractor information template to use
BASE_CONFIG = \
    {
        "@context": "http://clowder.ncsa.illinois.edu/contexts/extractors.jsonld",
        "name": None,
        "version": None,
        "description": None,
        "author": None,
        "contributors": [],
        "contexts": [],
        "repository": {
            "repType": "git",
            "repUrl": None
        },
        "process": {
            "dataset": [
                "file.added"
            ]
        },
        "external_services": [],
        "dependencies": [],
        "bibtex": []
    }

# The template file name for Dockerfile
DOCKERFILE_TEMPLATE_FILE_NAME = "Dockerfile.template"

def determine_git_submodule_folder():
    """Used to determine if the script file is in a git submodule folder
    Return:
        Returns the relative path to the submodule folder, or None if not a submodule
    """
    is_submodule = False
    submodule_folder = "./"

    # First check for a command line hint
    argc = len(sys.argv)
    for idx in range(1, argc):
        if '=' in sys.argv[idx]:
            parts = sys.argv[idx].split('=')
            parts_len = len(parts)
            if parts_len > 0:
                if parts[0] == 'submodule':
                    if parts_len > 1:
                        is_submodule = True
                        submodule_folder = parts[1]
                        break
                    else:
                        print('Missing submodule parameter folder: "submodule=<folder>"')
                        exit(1)

    # Get our folder name and try to determine if we're a submodule
    if not is_submodule:
        start_folder = os.getcwd()
        folder = os.path.dirname(__file__)
        folder_name = os.path.basename(folder)
        while folder and not folder == '/':
            os.chdir(folder)
            if os.path.isfile(os.path.join(folder, ".gitmodules")) or \
               os.path.isfile(os.path.join(folder, ".git")):
                psm = subprocess.Popen(['git', 'submodule', 'status', folder],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
                result = psm.communicate()[0]
                if result:
                    if 'fatal' in result and 'outside repository' in result:
                        break
                    elif folder_name in result:
                        # Check for a complete name
                        if " " + folder_name + " " in result:
                            is_submodule = True
                            break

            # Try the next folder up
            submodule_folder += os.path.basename(folder) + '/'
            folder = os.path.dirname(folder)

        # Restore to our starting folder
        os.chdir(start_folder)

    if not is_submodule:
        submodule_folder = None
    return submodule_folder

def generate_info():
    """Generates the extractor_info.json file to the current folder
    """
    global BASE_CONFIG

    missing = []
    if not configuration.EXTRACTOR_NAME:
        missing.append("Extractor name")
    if not configuration.VERSION:
        missing.append("Extractor version")
    if not configuration.DESCRIPTION:
        missing.append("Extractor description")
    if not configuration.AUTHOR_NAME:
        missing.append("Author name")
    if not configuration.AUTHOR_EMAIL:
        missing.append("Author email")
    if not configuration.REPOSITORY:
        missing.append("Repository")
    if missing:
        raise RuntimeError("One or more configuration fields aren't defined in configuration.py: " \
                           + ", ".join(missing))

    # We make a deep copy so we can manipulate the dict without messing up the master
    config = copy.deepcopy(BASE_CONFIG)
    config['name'] = configuration.EXTRACTOR_NAME
    config['version'] = configuration.VERSION
    config['description'] = configuration.DESCRIPTION
    config['author'] = "%s <%s>" % (configuration.AUTHOR_NAME, configuration.AUTHOR_EMAIL)
    if 'repository' in config:
        config['repository']['repUrl'] = configuration.REPOSITORY

    with open("extractor_info.json", "w") as out_file:
        json.dump(config, out_file, indent=4)
        out_file.write("\n")

def generate_dockerfile(submodule_folder):
    """Genertes a Dockerfile file using the configured information
    Args:
        submodule_folder(str): None if not a git submodule, or relative path of
                submodule folder
    """
    global DOCKERFILE_TEMPLATE_FILE_NAME

    missing = []
    if not configuration.EXTRACTOR_NAME:
        missing.append("Extractor name")
    if not configuration.AUTHOR_NAME:
        missing.append("Author name")
    if not configuration.AUTHOR_EMAIL:
        missing.append("Author email")
    if missing:
        raise RuntimeError("One or more configuration fields aren't defined in configuration.py: " \
                           + ", ".join(missing))

    new_name = configuration.EXTRACTOR_NAME.strip().replace(' ', '_').replace('\t', '_').\
                                            replace('\n', '_').replace('\r', '_')
    extractor_name = new_name.lower()

    template = [line.rstrip('\n') for line in open(DOCKERFILE_TEMPLATE_FILE_NAME, "r")]
    with open('Dockerfile', 'w') as out_file:
        for line in template:
            if line.startswith('MAINTAINER'):
                out_file.write("MAINTAINER {0} <{1}>\n".format(configuration.AUTHOR_NAME, \
                               configuration.AUTHOR_EMAIL))
            elif line.startswith('ENV') and 'submodule_home' in line and submodule_folder:
                out_file.write('ENV submodule_home "' + submodule_folder + '"')
            elif line.lstrip().startswith('RABBITMQ_QUEUE'):
                white_space = re.match(r"\s*", line).group()
                out_file.write("{0}RABBITMQ_QUEUE=\"terra.dronepipeline.{1}\" \\\n". \
                         format(white_space, extractor_name))
            else:
                out_file.write("{0}\n".format(line))

def copy_files_to_parent(file_list):
    """Moves key files to the parent folder
    Args:
        file_list(list): A list of file names to copy
    Return:
        Returns True if files copied or skipped without a problem. False
        is returned if the copy had to be aborted and rolled back
    """
    our_folder = os.path.dirname(__file__)
    parent_folder = os.path.dirname(our_folder)
    copied_files = []

    # Loop through and copy files
    no_problems = True
    for one_file in file_list:
        try:
            dest_file = os.path.join(parent_folder, one_file)
            if not os.path.isfile(dest_file):
                print('Copying: "' + one_file + '" to parent folder: "' + parent_folder + '"')
                shutil.copyfile(os.path.join(our_folder, one_file), dest_file)
                copied_files.append(dest_file)
            else:
                print('Not overwriting destination file: "' + dest_file + '"')
                print('  Remove the file if you want it updated')
        except Exception as ex:
            print('Exception while copying files: ' + str(ex))
            print('File to parent folder: "' + os.path.join(our_folder, one_file) + '"')
            no_problems = False
            break

    # Clean up if we had serious problems
    if not no_problems:
        copied_len = len(copied_files)
        if copied_len > 0:
            print('Exceptions detected. Cleaning up copied files')
            for one_file in copied_files:
                print('  Deleting: "' + one_file + '"')
                os.remove(one_file)

    # Return the result
    return no_problems

# Make the call to generate the file
if __name__ == "__main__":
    SUBMODULE_FOLDER = determine_git_submodule_folder()
    if SUBMODULE_FOLDER:
        print('Configuring extractor as a git submodule with relative folder of "' +
              SUBMODULE_FOLDER + '"')
    else:
        print('Configuring extractor')
    generate_info()
    generate_dockerfile(SUBMODULE_FOLDER)
    if SUBMODULE_FOLDER:
        copy_files_to_parent(['extractor_info.json', 'extractor.py'])
