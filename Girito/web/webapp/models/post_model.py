from webapp.db_config import db_conn
from bson import ObjectId

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
    
    def get_post_by_file_id(file_id):
        
        post = db_conn.db.posts.find({"file_id": file_id})

        return list(post)
    
    def get_post_info_by_id(post_id):
        
        post_id_obj = ObjectId(post_id)
        post = db_conn.db.posts.find_one({"_id": post_id_obj}, {"title": 1, "summary": 1, "created_on": 1, "type": 1, "user_id": 1,"file_id": 1, "_id": 0})
        
        post_title = post.get("title")
        post_sum = post.get("summary")
        post_date = post.get("created_on")
        post_type = post.get("type")
        file_id = post.get("file_id")
        user_id = post.get("user_id")

        return post
    
    def softdelete_post(post_id):
        post_id_obj = ObjectId(post_id)
        results = db_conn.db.posts.update_one(
            {"_id": post_id_obj},
            {"$set": {"deleted": True}}
        )