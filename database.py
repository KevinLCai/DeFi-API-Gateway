import mysql.connector
import logging

class Database:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.connection = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )

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

    def close(self):
        self.connection.close()
