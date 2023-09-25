from flask import render_template, request, redirect, url_for, send_file, Response, send_from_directory, Blueprint, current_app, session
from webapp.models.post_model import Post
from webapp.models.stream_model import Stream
from webapp.models.file_model import File

import os
import datetime

post_routes = Blueprint('post', __name__)

files_folder = os.path.join(os.getcwd(), "static", "files")

@post_routes.route("/submit")
def submit():

    logged = session.get("logged")

    if logged is True:
        return render_template("create_post.html", logged=logged)
    else:
        return redirect(url_for("homepage"))

@post_routes.route("/post/<sf_id>", methods=["GET"])
def post(sf_id):

    logged = session.get("logged")
    session_user_id = session.get("user_id")

    p = Post.get_post_info_by_id(sf_id)

    ind_post = {}
    file_type = None
    file_id = None

    title = None
    summary = None
    user_id = None

    for k, v in p.items():
        if k == "type":
            file_type = v
        if k == "file_id":
            file_id = v
        if k == "title":
            title = v
        if k == "summary":
            summary = v
        if k == "user_id":
            user_id = v
            
    ind_post["title"] = title  
    ind_post["summary"] = summary   
    ind_post[file_type] = file_id 

    if user_id == session_user_id:
        owned = True
    else:
        owned = False

    return render_template("post.html", ind_post=ind_post, logged=logged, owned=owned, post_id=sf_id)

@post_routes.route("/softdelete_post/<post_id>", methods=["POST"])
def softdelete_post(post_id):

    Post.softdelete_post(post_id)

    return redirect(url_for("homepage"))

@post_routes.route("/create_post", methods=["POST"])
def create_post():

    if request.method == "POST":

        user_id = session.get("user_id")

        title = request.form.get("title")
        summary = request.form.get("summary")
        attachment = request.files["attachment"]

        file_extension = os.path.splitext(attachment.filename)[1].strip(".")

        type = ""
        if file_extension == "mp4":
            type = "vid"
        elif file_extension == "png":
            type = "img"

        ## FILE CREATION IN DB ##
        file = File(created_on=datetime.datetime.today())
        file_id = file.create_file()

        ## POST CREATION IN DB ##
        post = Post(title=title, type=type, created_on=datetime.datetime.today(), summary=summary, file_id=str(file_id), user_id=str(user_id), deleted=False)
        post_id = post.create_post()

        file_name = str(file_id) + "." + file_extension

        file_path = os.path.join(os.getcwd(), "static", "files", file_name)

        attachment.save(file_path)

    return redirect(url_for("homepage"))

def retrieve_files():
    
    posts_list = []
    posts = []

    for filename in os.listdir(files_folder):
        file_path = "/files/" + filename
        file_extension = os.path.splitext(filename)[1].lower()

        result_string = filename[:-4]
        post = Post.get_post_by_file_id(result_string)

        posts_list.append(post)

    for pl in posts_list:
        for p in pl:
            if 'file_id' in p:
                p['file_id'] = 'files/' + p['file_id']
            posts.append(p)

    return posts


