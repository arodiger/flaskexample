
import configparser

##############   CONFIGURATIONS.INI WITH ENVIRONMENT VARIABLE    #####################################
# to enable DEVELOPMENT MODE set env var MYPYCONFIG_INI=DEVELOPMENT
# when deployed into production the env var will NOT be set, therefore PRODUCTION MODE ENABLED 

# import os
# MYPYCONFIG_INI = os.environ.get('MYPYCONFIG_INI', 'PRODUCTION').upper()

# $env:MYPYCONFIG_INI="DEVELOPMENT"           # powershell creates environment variable
# Get-ChildItem -Path Env:\MYPYCONFIG_INI     # powershell get/display environment variable
# $env:MYPYCONFIG_INI="PRODUCTION"            # powershell re-assigns environment varialble
# $Env:MYPYCONFIG_INI = $null                 # powershell clear and delete an environment variable

# export MYPYCONFIG_INI=DEVELOPMENT           # bash create and set environment variable
# echo $MYPYCONFIG_INI                        # bash get/display environment variable
# unset MYPYCONFIG_INI                        # bash delete environment variable.
###################################################################################################


# Method to read config file settings
def read_config():
    config = configparser.ConfigParser()
    config.read('configurations.ini')
    return config

# function to read a specific section from a specific file, defaults values 
def get_section_config(filename="configurations.ini", section="PRODUCTION_POSTGRES_DBSettings"):
    section_dict = {}
    parser = configparser.ConfigParser()
    parser.read(filename)

    # get section, default production postgres
    if (parser.has_section(section)):
        params = parser.items(section)
        for param in params:
            section_dict[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")
    return section_dict


   