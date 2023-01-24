
from functools import wraps
import logging
import datetime as dt


##############   HOW TO CONTROL LOGGING    ########################################################
# to enable debug logging for the console and logfile set env var MYPYLOGGER_LOGLEVEL=DEBUG
# else the default logging level will be WARNING
# when deployed into production the env var will not be set, therefore debug logging 
# will automatically be disabled

# import os
# MYPYLOGGER_LOGLEVEL = os.environ.get('MYPYLOGGER_LOGLEVEL', 'WARNING').upper()
MYPYLOGGER_LOGLEVEL = "WARNING"

# $env:MYPYLOGGER_LOGLEVEL="DEBUG"                 # POWERSHELL creates environment variable
# Get-ChildItem -Path Env:\MYPYLOGGER_LOGLEVEL     # POWERSHELL get/display environment variable
# $env:MYPYLOGGER_LOGLEVEL="WARNING"               # POWERSHELL re-assigns environment varialble
# $Env:MYPYLOGGER_LOGLEVEL = $null                 # POWERSHELL clear and delete an environment variable

# export MYPYLOGGER_LOGLEVEL=DEBUG                 # BASH create and set environment variable
# echo $MYPYLOGGER_LOGLEVEL                        # BASH get/display environment variable
# unset MYPYLOGGER_LOGLEVEL                        # BASH delete environment variable.
###################################################################################################


# setup a logfile with the name being month-day-year.log
today = dt.datetime.today()
filename = f"{today.month:02d}-{today.day:02d}-{today.year}.log"

logging.basicConfig(level=MYPYLOGGER_LOGLEVEL)

# ##########  Problems with basicConfig NOT allowing your messages ################################
# ##########  you can loop thru handlers and remove root handlers. ################################
# for handler in logging.root.handlers:
#     logging. root.removeHandler(handler)
# ##########  occassionaly this is needed  ########################################################


#   create your own logger
logger = logging.getLogger("MYPYLOGGER")


# setup a log file for your logger messages
file_handler = logging.FileHandler(filename)
file_handler.setLevel(MYPYLOGGER_LOGLEVEL)
# setup our formatter for the log file
formatter = logging.Formatter("%(asctime)s: %(name)s %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

###################################################################################################
# setup console handler to send log messages to the console, sys.stderr is default
# majority of time i don't use this code, since two messages will be printed on the console screen
# the console_handler uses the simple formatter with less information 
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# logger.addHandler(console_handler)
###################################################################################################

# set file handler to send log messages to "filename.log" file
logger.addHandler(file_handler)


# create a decorator function just to log the function has been called
# wraps will update the decorator function with the decorated functions attributs
def log_functionCalled(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        logger.debug(f"debug message mypylogger DECORATED Function: {func.__name__} called  ##########")
        result = func(*args, **kwargs)
        return result
    return wrapper_func


logger.debug("debug message mypylogger ########## BEGIN ##########")
# logger.info("info message mypylogger ########## BEGIN ##########")
# logger.warning("warning message mypylogger ########## BEGIN ##########")
# logger.critical("critical message mypylogger ########## BEGIN ##########")

