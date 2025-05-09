#--------------------------------#
# Python database utilities file #
#--------------------------------#

import os
import warnings
import pandas as pd
from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error
from pandas import DataFrame

def __read_config(config_file = 'ShuttleService.ini', section = 'mysql'):
    """
    Private function to read the configuration file config_file 
    with the given section. If successful, return the configuration 
    as a dictionary, else raise an exception.
    """
    parser = ConfigParser()
    
    # Does the configuration file exist?
    if os.path.isfile(config_file):
        parser.read(config_file)
    else:
        raise Exception(f"Configuration file '{config_file}' "
                        "doesn't exist.")
    
    config = {}
    
    if parser.has_section(section):
        # Parse the configuration file.
        items = parser.items(section)
        
        # Construct the parameter dictionary.
        for item in items:
            config[item[0]] = item[1]
            
    else:
        raise Exception(f'Section [{section}] missing ' + \
                        f'in config file {config_file}')
    
    return config

def db_connection(config_file = 'ShuttleService.ini', section = 'mysql'):
    """
    Public function to make a database connection using the 
    configuration file config_file with the given section. 
    If successful, return the connection, else raise an exception.
    """
    try:
        db_config = __read_config(config_file, section)
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            return conn

    except Error as e:
        raise Exception(f'Connection failed: {e}')

def df_query(conn, sql):
    """
    Public function to use the database connection conn 
    to execute the SQL code. Return the resulting rows
    as a dataframe. If the query failed, raise an exception.
    """
    warnings.simplefilter(action='ignore', category=UserWarning)
    
    try:
        df = pd.read_sql_query(sql, conn)
        return df        
    except Error as e:
        raise Exception(f'Query failed: {e}')

# Copyright (c) 2025 by Ronald Mak