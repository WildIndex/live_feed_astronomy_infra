from pymongo import MongoClient

class DatabaseConnection:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://10.5.0.6:27017/")
            self.db = self.client["live_feed_astronomy"]
        except Exception as e:
            print("Error connecting to the database:", e)

db_conn = DatabaseConnection()