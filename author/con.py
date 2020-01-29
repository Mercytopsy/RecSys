import sqlalchemy 
import mysql.connector
import pandas as pd
import numpy as np
def execute():
    df=pd.read_excel('/home/babatope/Documents/dietp/diet/data.xlsx')
    database_username = 'Dietitian_app'
    database_password = 'diet_password'
    database_ip       = 'localhost'
    database_name     = 'Dietitians'
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
    df.to_sql(con=database_connection, name='Dietetic', if_exists='replace')
    print('done')