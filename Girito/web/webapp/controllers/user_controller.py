from flask import render_template, request, redirect, url_for, Blueprint, current_app, session
import bcrypt
from models.user_model import User

user_routes = Blueprint('user', __name__)

@user_routes.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@user_routes.route("/register", methods=["GET", "POST"])
def register():
    return render_template("sign_up.html")

@user_routes.route("/sign_in", methods=["POST"])
def sign_in():

    app = current_app._get_current_object()
    app.secret_key = app.config['SECRET_KEY']

    email_username = request.form.get("email_username")
    pwd = request.form.get("pwd")

    user_data = User.check_valid_user(email_username)

    if user_data is not None:

        user_id, hashed_pwd = user_data

        if user_id is not None:

            if bcrypt.checkpw(pwd.encode("utf-8"), hashed_pwd):

                role = User.get_user_role_by_id(user_id)

                session['user_id'] = str(user_id)
                session['role'] = str(role)
                session['logged'] = True
                
                return redirect(url_for("homepage"))
            else:
                ## INCORRECT USER INPUT DATA ##
                return redirect(url_for("user.login"))
    else:
        ## INCORRECT USER INPUT DATA ##
        return redirect(url_for("user.login"))

@user_routes.route("/sign_up", methods=["POST"])
def sign_up():

    terms_checkbox = request.form.get("terms_checkbox")
    if terms_checkbox == "on":
        terms_checkbox = True
    else:
        terms_checkbox = False

    name = request.form.get("reg_name")
    surname = request.form.get("reg_surname")
    username = request.form.get("reg_username")
    email = request.form.get("reg_email")

    pwd = request.form.get("reg_pwd")
    hashed_pwd = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())

    if terms_checkbox is True:

        user = User(name=name, surname=surname, email=email, pwd=hashed_pwd, username=username, blocked=False, silenced=False, deleted=False, approved=False, role="Registered")
        user.create_user()

        return redirect(url_for("homepage"))
    else:
        return redirect(url_for("user.register"))

@user_routes.route("/logout")
def logout():

    session['logged'] = False
    session.pop('user_id', None) 
    return redirect(url_for("homepage"))
