from db_config import db_conn
from bson import ObjectId

class User:
    def __init__(self, name=None, surname=None, email=None, pwd=None, username=None, blocked=False, silenced=False, deleted=False, approved=False, role=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.pwd = pwd
        self.username = username
        self.blocked = blocked
        self.silenced = silenced
        self.deleted = deleted
        self.approved = approved
        self.role = role

    def create_user(self):
        user_data = {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "pwd": self.pwd,
            "username": self.username,
            "blocked": self.blocked,
            "silenced": self.silenced,
            "deleted": self.deleted,
            "approved": self.approved,
            "role": self.role,
        }
        
        filtered_user_data = {key: value for key, value in user_data.items() if value is not None and value != ""}

        db_conn.db.users.insert_one(filtered_user_data)

    def get_all():
        return list(db_conn.db.users.find())
    
    def check_valid_user(email_username):

        user = db_conn.db.users.find_one({'$or': [{'email': email_username}, {'username': email_username}]})
        
        if user is not None:
            user_id = user.get("_id")
            hashed_pwd = user.get("pwd")

            return str(user_id), hashed_pwd
        else:
            return None
        
    def get_user_role_by_id(user_id):
        
        user_id_obj = ObjectId(user_id)
        user = db_conn.db.users.find_one({'_id': user_id_obj}, {'role': 1})

        if user is not None:
            return user.get("role")
        else:
            return None
