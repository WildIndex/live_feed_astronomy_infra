from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file's extension is allowed
def allowed_file(filename):
    allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file was submitted
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        return "No selected file"
    
    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"File '{filename}' uploaded successfully."
    else:
        return "Invalid file type. Allowed file types are: txt, pdf, png, jpg, jpeg, gif."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
