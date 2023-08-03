import os
from flask import Flask, render_template, request, send_file, redirect
from flask_socketio import SocketIO
from werkzeug.exceptions import RequestEntityTooLarge
from functions import openai_api, run_editor

app = Flask(__name__)
app.config["UPLOAD_DIRECTORY"] = 'text_files/'
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024 #16MB
app.config["ALLOWED_EXTENSIONS"] = [".txt"] #Would like to add .doc and .docx later
socketio = SocketIO(app)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    
@app.route('/upload', methods=["POST"])
def upload():
    try:
        file = request.files['file']
        # Would be nice to check the file size here. Not sure if MAX_CONTENT checks it here or after file.save, 
        # but it takes a long time for it to check files that are 1 GB+
        key = request.form['key']
        extension = os.path.splitext(file.filename)[1]
        if extension not in app.config["ALLOWED_EXTENSIONS"]:
            return "Cannot upload that file type"

        if file:
            file.save("text_files/original.txt")
    except RequestEntityTooLarge:
        return "File is too large."
    run_editor(key)
    return redirect('/results')

#This is not in use, but would like to get it working ASAP
@app.route('/progress', methods=["GET"])
def progress(edit_progress):
    if request.method == "GET":
        return render_template("progress.html", progress = edit_progress)


@app.route('/results')
def results():    
    with open("text_files/edited.txt", "r", encoding='utf-8', errors="ignore") as f:
        edited_text = f.read()
    edited_text = edited_text.split("\n\n")
    return render_template("results.html", text_to_display=edited_text)
        

@app.route('/download')
def download(): 
    return send_file("text_files\\edited.txt", as_attachment=True, download_name="edited.txt")


@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

if __name__ == "__main__":
    app.run(debug=True)
