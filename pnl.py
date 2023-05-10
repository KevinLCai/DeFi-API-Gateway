import mysql.connector
import logging
from flask import jsonify
import datetime
from collections import deque
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="env/.env")

PASSWORD = os.getenv('PASSWORD')

class PnL():
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database
            )
            self.valid = True
        except:
            logging.error("Invalid Database Credentials")
            self.valid = False

    def get_all_trades(self, from_timestamp=None):
        cursor = self.connection.cursor()
        if from_timestamp:
            query = "SELECT * FROM Orders WHERE Timestamp > %s"
            values = (datetime.datetime.fromtimestamp(from_timestamp).strftime('%Y-%m-%d %H:%M:%S'),)
            cursor.execute(query, values)
        else:
            query = "SELECT * FROM Orders"
            cursor.execute(query)
            
        result = cursor.fetchall()
        cursor.close()
        self.deals = pd.DataFrame(result)
    
    def calculate_pnl(self):
        self.get_all_trades(1672537140)
        self.deals['position'] = self.deals[5] * self.deals[6]
        btc_buy = self.deals.loc[(self.deals[2] == 1) & (self.deals[4] == 'buy')]
        btc_sell = self.deals.loc[(self.deals[2] == 1) & (self.deals[4] == 'sell')]
        eth_buy = self.deals.loc[(self.deals[2] == 2) & (self.deals[4] == 'buy')]
        eth_sell = self.deals.loc[(self.deals[2] == 2) & (self.deals[4] == 'sell')]
        
        btc_position = btc_buy['position'].sum() - btc_sell['position'].sum()
        eth_position = eth_buy['position'].sum() - eth_sell['position'].sum()
        usd_position = btc_position - eth_position
        return usd_position

def create_db_instance():
    db = PnL(
        user='root',
        password=PASSWORD,
        host='localhost',
        database='defi_trading'
    )
    return db

db = create_db_instance()
pnl = db.calculate_pnl()

print(pnl)
