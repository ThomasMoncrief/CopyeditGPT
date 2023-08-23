import os, global_var
from flask import Flask, render_template, request, send_file, redirect
from werkzeug.exceptions import RequestEntityTooLarge
from functions import prep_editor, run_editor
import docx

#from flask_socketio import SocketIO
# this will come into use when we start using web sockets in order to get a better progress page running.

app = Flask(__name__)
app.config["UPLOAD_DIRECTORY"] = 'text_files/'
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024 #16MB
app.config["ALLOWED_EXTENSIONS"] = [".txt", ".docx"] #Would like to add LaTex and RTF compatibility later.
#socketio = SocketIO(app)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")


@app.route('/upload', methods=["POST"])
def upload():
    global_var.key = request.form['key']
    if request.form['upload'] == "upload_file":
        try:
            file = request.files['file']
            if not file:
                return "Must upload a file"
            # Would be nice to check the file size here. Not sure if MAX_CONTENT checks it here or after file.save, 
            # but it takes a long time for it to check files that are 1 GB+
            global_var.extension = os.path.splitext(file.filename)[1]
            if global_var.extension not in app.config["ALLOWED_EXTENSIONS"]:
                return "Cannot upload that file type. Must be '.txt' or '.docx'"

            file.save("text_files/original" + global_var.extension)

        except RequestEntityTooLarge:
            return "File is too large."
    
    if request.form['upload'] == "upload_text":        
        #reset paragraph formatting sent by the HTML form
        text = request.form['text_box'].split("\r\n")
        if text == [""]:
            return "Text box is blank"
        submit_text = open("text_files/original.txt", "w", encoding='utf-8', errors="ignore")
        for paragraph in text:
            submit_text.write(paragraph + "\n")
        submit_text.close()
        global_var.extension = ".txt"
    
    global_var.submit_text = prep_editor(global_var.extension)
    return redirect('/progress')


@app.route('/progress', methods=["GET", "POST"])
def progress():
    if request.method == "GET":
        return render_template("progress.html", chunks=global_var.chunk_count, wait=global_var.chunk_count * 15)
    if request.method == "POST":
        run_editor(global_var.submit_text)
        return redirect('/results')


@app.route('/results')
def results():    
    with open("text_files/edited.txt", "r", encoding='utf-8', errors="ignore") as f:
        edited_text = f.read()
    edited_text = edited_text.split("\n")
    return render_template("results.html", text_to_display=edited_text)


@app.route('/download')
def download(): 
    file_type = request.args.get('type')
    if file_type == "txt":
        return send_file("text_files/edited.txt", as_attachment=True)
    
    #*Need to match original document's formatting. Otherwise it is difficult to reject changes. 
    if file_type == "docx":
        edited = docx.Document()
        with open("text_files/edited.txt", "r", encoding='utf-8', errors="ignore") as f:
            edited_text = f.read()
        edited_text = edited_text.split("\n")
        for paragraph in edited_text:
            edited.add_paragraph(paragraph)
        edited.save("text_files/edited.docx")
        return send_file("text_files/edited.docx")


if __name__ == "__main__":
    app.run(debug=True)
