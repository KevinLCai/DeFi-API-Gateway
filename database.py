import mysql.connector
import logging
from flask import jsonify

class Database:
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

    def is_not_valid(self):
        if not self.valid:
            logging.error("INVALID CREDENTIALS")
            return {'status': 'error', 'message': 'Invalid DB Credentials'}
        else:
            return False

    def insert_token(self, token_id, token_name, token_type):
        cursor = self.connection.cursor()
        query = "INSERT INTO Tokens (TokenID, TokenName, TokenType) VALUES (%s, %s, %s)"
        values = (token_id, token_name, token_type)
        try:
            cursor.execute(query, values)
            self.connection.commit()
        except mysql.connector.IntegrityError as e:
            logging.error(f"Duplicate entry violation: {e}")
            self.connection.rollback()
        cursor.close()

    def insert_market_data(self, token_id, timestamp, price, volume, bid_price, ask_price):
        cursor = self.connection.cursor()
        query = "INSERT INTO MarketData (TokenID, Timestamp, Price, Volume, BidPrice, AskPrice) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (token_id, timestamp, price, volume, bid_price, ask_price)
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def insert_historical_data(self, token_id, timestamp, price, volume, news):
        cursor = self.connection.cursor()
        query = "INSERT INTO HistoricalData (TokenID, Timestamp, Price, Volume, News) VALUES (%s, %s, %s, %s, %s)"
        values = (token_id, timestamp, price, volume, news)
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def insert_trade(self, token_id, timestamp, trade_price, trade_size, fees):
        cursor = self.connection.cursor()
        query = "INSERT INTO Trades (TokenID, Timestamp, TradePrice, TradeSize, Fees) VALUES (%s, %s, %s, %s, %s)"
        values = (token_id, timestamp, trade_price, trade_size, fees)
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def insert_order(self, token_id, timestamp, order_type, order_price, order_size):
        cursor = self.connection.cursor()
        query = "INSERT INTO Orders (TokenID, Timestamp, OrderType, OrderPrice, OrderSize) VALUES (%s, %s, %s, %s, %s)"
        values = (token_id, timestamp, order_type, order_price, order_size)
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def insert_position(self, token_id, current_market_value, unrealized_gains, unrealized_losses):
        cursor = self.connection.cursor()
        query = "INSERT INTO Positions (TokenID, CurrentMarketValue, UnrealizedGains, UnrealizedLosses) VALUES (%s, %s, %s, %s)"
        values = (token_id, current_market_value, unrealized_gains, unrealized_losses)
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def insert_account(self, account_balance, available_buying_power, margin_requirements):
        cursor = self.connection.cursor()
        query = "INSERT INTO Accounts (AccountBalance, AvailableBuyingPower, MarginRequirements) VALUES (%s, %s, %s)"
        values = (account_balance, available_buying_power, margin_requirements)
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def get_token_by_id(self, token_id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM Tokens WHERE TokenID = %s"
        values = (token_id,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_market_data_by_token_id(self, token_id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM MarketData WHERE TokenID = %s"
        values = (token_id,)
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_historical_data_by_token_id(self, token_id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM HistoricalData WHERE TokenID = %s"
        values = (token_id,)
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_trades_by_token_id(self, token_id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM Trades WHERE TokenID = %s"
        values = (token_id,)
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_orders_by_token_id(self, token_id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM Orders WHERE TokenID = %s"
        values = (token_id,)
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_positions_by_token_id(self, token_id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM Positions WHERE TokenID = %s"
        values = (token_id,)
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_account_by_id(self, account_id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM Accounts WHERE AccountID = %s"
        values = (account_id,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        return result
    


    def insert_deal(self, strategy, order_id, token_id, timestamp, order_type, order_price, order_size):
        cursor = self.connection.cursor()
        query = "INSERT INTO Orders (Strategy, OrderID, TokenID, Timestamp, OrderType, OrderPrice, OrderSize) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (strategy, order_id, token_id, timestamp, order_type, order_price, order_size)
        print("VALUES==============")
        print(values)
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()




    def close(self):
        self.connection.close()
