import psycopg2 
import mypyLogger
import confighelper

import os
MYPYCONFIG_INI = os.environ.get('MYPYCONFIG_INI', 'PRODUCTION').upper()
# either DEVELOPMENT OR PRODUCTION will be pre-pended to form section title name
postgressDBSettings = MYPYCONFIG_INI + "_POSTGRES_DBSettings"
# postgressDBSettings = "PRODUCTION_POSTGRES_DBSettings"

# read in conifgurations.ini file
config = confighelper.read_config()

CONFIG_HOST_ADDRESS = config[postgressDBSettings]["ini_db_host_address"]
CONFIG_DB = config[postgressDBSettings]["ini_database"]
CONFIG_USER = config[postgressDBSettings]["ini_user"]
CONFIG_PASSWORD = config[postgressDBSettings]["ini_password"]


class Database(object):
    DB_HOST_ADDRESS = CONFIG_HOST_ADDRESS
    DB = CONFIG_DB
    USER = CONFIG_USER
    PASSWORD = CONFIG_PASSWORD

    CONNECTION = None
    CURSOR = None

    @staticmethod
    def initialize():
        Database.CONNECTION = psycopg2.connect(host=Database.DB_HOST_ADDRESS, database=Database.DB, user=Database.USER, password=Database.PASSWORD)
        Database.CURSOR = Database.CONNECTION.cursor()
    
    @staticmethod
    def execute(psql):
        Database.CURSOR.execute(psql)

    @staticmethod
    def commit():
        Database.CONNECTION.commit()

    @staticmethod
    def fetchall():
        return Database.CURSOR.fetchall()

    @staticmethod
    def cleanup():
        Database.CURSOR.close()
        Database.CONNECTION.close()

    @staticmethod
    def __del__():
        Database.CURSOR.close()
        Database.CONNECTION.close()

    @staticmethod
    def insert_into_db(*args, **kwargs):
        # args, list of dictionaries
        # traverse thru a [list] of {dictionaries,,} and INSERT into a database
        # remove "'" and remove "/" replace with "_", special characters for postgres INSERT command (quick way to move on with my coding)
        for mydict in args:
            columns = ', '.join(str(x).replace('/', '_').replace("'", '')  for x in mydict.keys())
            values  = ', '.join("'" + str(x).replace('/', '_').replace("'", '') + "'" for x in mydict.values())
            test_sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (kwargs["tablename"], columns, values) 
            mypyLogger.logger.debug(test_sql)
            Database.CURSOR.execute(test_sql)



    # @mypylogger.log_functionCalled
    @staticmethod
    def select_webchat_history(**kwargs):
        # execute the query and return the results in a dictionary
        tempDict = []
        if (kwargs["query"]):
            Database.execute(kwargs["query"])
            rows = Database.fetchall()
            for r in rows:
                data_dict = {"username" : r[0], "message" : r[1], "time_stamp" : r[2], "loadhistory" : r[3]}
                tempDict.append( data_dict )
                mypyLogger.logger.debug(data_dict)

            mypyLogger.logger.debug("Data fetched from the database")
            mypyLogger.logger.debug(tempDict)
        return tempDict




