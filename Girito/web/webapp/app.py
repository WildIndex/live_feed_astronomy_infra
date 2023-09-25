from flask import Flask, render_template, session
from config import Config
from webapp.extensions import socketio
from webapp.controllers.stream_controller import stream_routes
from webapp.controllers.post_controller import post_routes
from webapp.controllers.post_controller import retrieve_files 
from webapp.controllers.user_controller import user_routes

app = Flask(__name__, static_url_path='/static')

app.config.from_object(Config)

socketio.init_app(app)

app.register_blueprint(stream_routes, socketio=socketio)
app.register_blueprint(post_routes)
app.register_blueprint(user_routes)

@app.route('/homepage')
def homepage():
    
    logged = session.get('logged', False)
    stored_files = retrieve_files()
    return render_template('homepage.html', stored_files=stored_files, logged = logged)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, ssl_context="adhoc", debug=True)