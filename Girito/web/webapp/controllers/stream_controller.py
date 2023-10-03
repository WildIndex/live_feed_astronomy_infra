from flask import render_template, request, redirect, url_for, send_file, Response, current_app, session, Blueprint
from flask_session import Session
from models.stream_model import Stream
from models.post_model import Post
from models.file_model import File
from extensions import socketio
from flask_socketio import emit, join_room, leave_room

import secrets
import datetime
import cv2
import os

stream_routes = Blueprint('stream', __name__)

streams = {}

cap = None
is_streaming = False

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Emit functions to handle WebRTC signaling
@socketio.on('broadcaster')
def handle_broadcaster():
    print('Received broadcaster signal')
    socketio.emit('broadcaster')

@socketio.on('watcher')
def handle_watcher():
    print('Received watcher signal')
    socketio.emit('watcher')

@socketio.on('offer')
def handle_offer(id, message):
    print('Received offer')
    socketio.emit('offer', id, message)

@socketio.on('answer')
def handle_answer(id, message):
    print('Received answer')
    socketio.emit('answer', id, message)

@socketio.on('candidate')
def handle_candidate(id, message):
    print('Received candidate')
    socketio.emit('candidate', id, message)

@stream_routes.route('/broadcast')
def broadcast():
    return render_template('broadcast.html')

@stream_routes.route('/watch')
def watch():
    return render_template('index.html')

@stream_routes.route("/stream")
def stream():

    logged = session.get("logged")

    if logged is True:
        return render_template("create_stream.html", logged=logged)
    else:
        return redirect(url_for("homepage"))

@stream_routes.route("/streaming/<stream_id>", methods=["GET"])
def streaming(stream_id):

    title = request.args.get("title")
    summary = request.args.get("summary")

    checking = Stream.is_stream_live(stream_id)
    
    if checking == False:
        return redirect(url_for("homepage"))
    else:
        s = Stream.get_stream_title_by_id(stream_id)
        is_live = request.form.get("live")

        if s != None:
                
            cap = streams[str(stream_id)]["capture"]

            #start_recording(str(stream_id))

            return render_template("streaming.html", stream_id=stream_id, title=title, summary=summary)
        elif is_live == True and stream_id == s:
            return render_template("streaming.html", stream_id=stream_id, title=title, summary=summary)
        elif is_live == False and stream_id == s:
            return redirect(url_for("homepage"))
        else:
            return "INVALID ID!"

@stream_routes.route("/create_stream", methods=["POST"])
def create_stream():

    if request.method == "POST":

        recording = False
        live = True

        file = File(type="vid", created_on=datetime.datetime.today())
        saved_file = file.create_file()

        title = request.form.get("title")
        summary = request.form.get("summary")
        stream = Stream(live=live, title=title, created_on=datetime.datetime.today(), summary=summary, exp_method=None, iso_sens=None, location=None, country=None, deleted=False, user_id=None, file_id=saved_file)
        stream_id = stream.create_stream()
        
        cap = cv2.VideoCapture(cv2.CAP_DSHOW)
        streams[str(stream_id)] = {"stream_file": str(saved_file),
                                   "capture": cap, "live":live,
                                   "recording":recording}

    return redirect(url_for("stream.streaming", stream_id=str(stream_id), title=title, summary=summary))


@stream_routes.route('/save_video', methods=['POST'])
def save_video():
    data = request.get_data()
    with open('recorded-video.mpeg', 'wb') as f:
        f.write(data)
        print("CAP!")
    return 'Video saved successfully!'

@socketio.on('stop_stream')
def stop_stream():

    print("STOPPED!")

    socketio.emit('stream_stopped')

'''

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, ssl_context="adhoc")



app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
streams = {}

streams_count = -1

def generate_random_id(length=12):
    return secrets.token_hex(length)

@app.route("/streaming/<stream_id>", methods=["GET"])
def streaming(stream_id):

    checking = Stream.is_stream_live(stream_id)
    
    if checking == False:
        return redirect(url_for("homepage"))
    else:
        s = Stream.get_stream_title_by_id(stream_id)
        is_live = request.form.get("live")
        
        user_id = streams[str(stream_id)]["user_id"]
        session['user_id'] = user_id

        if s != None:
            if stream_id in streams and streams[stream_id]["user_id"] == session["user_id"]:
                
                cap = streams[str(stream_id)]["capture"]

                start_recording(str(stream_id))

                return render_template("streaming.html", stream_id=stream_id)
        elif is_live == True and stream_id == s:
            return render_template("streaming.html", stream_id=stream_id)
        elif is_live == False and stream_id == s:
            return redirect(url_for("homepage"))
        else:
            return "INVALID ID!"

@app.route("/create_stream", methods=["POST"])
def create_stream():
    global streams_count

    if request.method == "POST":

        ## FOR TESTING ##
        user_id = generate_random_id()
        session["user_id"] = user_id

        recording = False
        live = True

        file = File(type="vid", created_on=datetime.datetime.today())
        saved_file = file.create_file()

        title = request.form.get("title")
        summary = "## Example Summary ##"
        stream = Stream(live=live, title=title, created_on=datetime.datetime.today(), summary=summary, exp_method=None, iso_sens=None, location=None, country=None, deleted=False, user_id=user_id, file_id=saved_file)
        stream_id = stream.create_stream()
        
        cap = cv2.VideoCapture(cv2.CAP_DSHOW)
        streams[str(stream_id)] = {"user_id": session["user_id"],
                                   "stream_file": str(saved_file),
                                   "capture": cap, "live":live,
                                   "recording":recording}

    return redirect(url_for("streaming", stream_id=str(stream_id)))

@app.route("/update_live_status", methods=["PATCH"])
def update_live_status(stream_id):
    live = streams[str(stream_id)]["live"]
    stream = Stream.set_stream_live_status(stream_id, live)

@app.route("/start_recording", methods=["POST"])
def start_recording(stream_id):

    fourcc = None

    cap = streams[str(stream_id)]["capture"]
    video_id = streams[str(stream_id)]["stream_file"]
    recording = streams[str(stream_id)]["recording"]

    cam_width = int(cap.get(3)) 
    cam_height = int(cap.get(4))

    if not recording:

        fourcc = cv2.VideoWriter_fourcc(*"H264")
        output_dir = os.path.join(app.root_path, 'static', 'files')
        output_path = os.path.join(output_dir, video_id + ".mp4")
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (cam_width, cam_height))
        streams[str(stream_id)]["out"] = out
        streams[str(stream_id)]["recording"] = True

@app.route("/stop_recording/<stream_id>", methods=["POST"])
def stop_recording(stream_id):

    out = streams[str(stream_id)]["out"]
    recording = streams[str(stream_id)]["recording"]

    if recording:
        out.release()
        streams[str(stream_id)]["recording"] = False

        streams[str(stream_id)]["live"] = False

        update_live_status(stream_id)

    return redirect(url_for("homepage"))

def generate_frames(stream_id, count):
    
    cap = streams[str(stream_id)]["capture"]
    out = streams[str(stream_id)]["out"]
    recording = streams[str(stream_id)]["recording"]

    while True:
        ret, frame = cap.read()

        if recording:
            out.write(frame)

        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route("/video_feed/<stream_id>", methods = ["GET"])
def video_feed(stream_id):

    count = streams_count + 1
    return Response(generate_frames(stream_id, count), mimetype='multipart/x-mixed-replace; boundary=frame')

def display_live_streams():
    ls = Stream.get_live_streams()
    return ls
'''