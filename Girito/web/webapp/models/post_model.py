from db_config import db_conn
from models.file_model import File
from bson import ObjectId
import re

class Post:
    def __init__(self, title, type=None, created_on=None, summary=None, file_id=None, user_id=None, votes=None, deleted=None):
        self.title = title
        self.created_on = created_on
        self.summary = summary
        self.type = type
        self.file_id = file_id
        self.user_id = user_id
        self.votes = votes
        self.deleted = deleted

    def create_post(self):
        post_data = {
            "title": self.title,
            "type": self.type,
            "created_on": self.created_on,
            "summary": self.summary,
            "file_id": self.file_id,
            "user_id": self.user_id,
            "votes": self.votes,
            "deleted": self.deleted,
        }

        filtered_post_data = {key: value for key, value in post_data.items() if value is not None and value != ""}
        
        results = db_conn.db.posts.insert_one(filtered_post_data)
        
        return results.inserted_id
    
    def update_post(post_id, title, summary, file_id, type):
        
        post_id_obj = ObjectId(post_id)
        post = db_conn.db.posts.update_one({"_id": post_id_obj}, {"$set": {"title": title, "summary": summary, "file_id": file_id, "type": type}})
    
    def get_post_by_file_id(file_id):
        posts = db_conn.db.posts.find({"file_id": file_id, "deleted": {"$ne": True}})
        return list(posts)

    def get_files_by_partial_title(title):
        # Create a regular expression pattern for the keyword
        pattern = re.compile(title, re.IGNORECASE)
        query = {
            "title": {
                "$regex": pattern
             },
        "deleted": False  # Add this condition to filter out deleted posts
        }

        # Find posts with titles containing the keyword
        posts = db_conn.db.posts.find(query, {"title": 1, "summary": 1, "created_on": 1, "type": 1, "user_id": 1, "file_id": 1, "deleted": 1, "_id": 0})

        # Extract the file_ids from matching posts
        file_ids = [post["file_id"] for post in posts]

        # Find files associated with the matching file_ids
        matching_files = db_conn.db.posts.find({"file_id": {"$in": file_ids}})

        return list(matching_files)

    
    def get_post_info_by_id(post_id):
        
        post_id_obj = ObjectId(post_id)
        post = db_conn.db.posts.find_one({"_id": post_id_obj}, {"title": 1, "summary": 1, "created_on": 1, "type": 1, "user_id": 1,"file_id": 1, "deleted": 1,"_id": 0})
        
        deleted = post.get("deleted")

        if deleted == False:
            return post
        else:
            return None
        
    def get_post_info_by_title(title):
        pattern = re.compile(title, re.IGNORECASE)
        query = {
            "title": {
                "$regex": pattern
            }
        }
        posts = db_conn.db.posts.find(query, {"title": 1, "summary": 1, "created_on": 1, "type": 1, "user_id": 1, "file_id": 1, "deleted": 1, "_id": 0})

        return posts
    
    def softdelete_post(post_id):
        post_id_obj = ObjectId(post_id)
        results = db_conn.db.posts.update_one(
            {"_id": post_id_obj},
            {"$set": {"deleted": True}}
        )