import mysql.connector
from mysql.connector import Error
import pandas as pd
from dashboard import key_vault

sql_host = key_vault.sql_host
sql_user = key_vault.sql_user
sql_pass = key_vault.sql_pass
sql_db = key_vault.sql