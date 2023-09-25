from pymongo import MongoClient

class DatabaseConnection:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client["live_feed_astronomy"]
        except Exception as e:
            print("Error connecting to the database:", e)

db_conn = DatabaseConnection()