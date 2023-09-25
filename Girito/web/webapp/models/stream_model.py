from flask import jsonify
from webapp.db_config import db_conn
from bson import ObjectId

stream_dict = {}

class Stream:
    def __init__(self, title, live=None ,created_on=None, summary=None, exp_method=None, iso_sens=None, location=None, country=None, deleted=False, user_id=None, file_id=None):
        self.title = title
        self.live = live
        self.created_on = created_on
        self.summary = summary
        self.exp_method = exp_method
        self.iso_sens = iso_sens
        self.location = location
        self.country = country
        self.deleted = deleted
        self.user_id = user_id
        self.file_id = file_id

    def create_stream(self):
        stream_data = {
            "title": self.title,
            "live": self.live,
            "created_on": self.created_on,
            "summary": self.summary,
            "exp_method": self.exp_method,
            "iso_sens": self.iso_sens,
            "location": self.location,
            "country": self.country,
            "deleted": self.deleted,
            "user_id": self.user_id,
            "file_id": self.file_id,
        }

        filtered_stream_data = {key: value for key, value in stream_data.items() if value is not None and value != ""}
        
        results = db_conn.db.streams.insert_one(filtered_stream_data)
        
        return results.inserted_id
    
    def get_stream_title_by_id(stream_id):
        stream_id_obj = ObjectId(stream_id)
        stream = db_conn.db.streams.find_one({"_id": stream_id_obj}, {"title": 1, "created_on": 1, "_id": 0})
        
        if stream is not None:
            stream_title = stream.get("title")
            stream_date = stream.get("created_on")

            stream_details = []
            stream_details.append(stream_title)
            stream_details.append(stream_date)
            
            stream_dict.update({stream_id: stream_details})

            return stream_dict
        else:
            return None
    
    def set_stream_live_status(stream_id, live):
        stream_id_obj = ObjectId(stream_id)
        results = db_conn.db.streams.update_one(
            {"_id": stream_id_obj},
            {"$set": {"live": live}}
        )

    def get_live_streams():    
        live_streams = db_conn.db.streams.find({'live': True})  
        return list(live_streams)
    
    def is_stream_live(stream_id):
        stream_id_obj = ObjectId(stream_id)
        query = {
            '_id': stream_id_obj,
            'live': True
        }
        live_stream = db_conn.db.streams.find_one(query)

        is_live = None

        if live_stream == None:
            is_live = False
        else:
            live_stream == True

        return is_live

