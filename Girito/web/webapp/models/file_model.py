from webapp.db_config import db_conn
from bson import ObjectId

class File:
    def __init__(self, type=None, created_on=None):
        self.type = type
        self.created_on = created_on

    def create_file(self):
        file_data = {
            "type": self.type,
            "created_on": self.created_on,
        }

        filtered_file_data = {key: value for key, value in file_data.items() if value is not None and value != ""}
        
        results = db_conn.db.files.insert_one(filtered_file_data)
        
        return results.inserted_id
    
    def get_all_fileids():
        cursor = db_conn.db.files.find()
        return list(cursor)

    
