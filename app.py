# app.py

from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from api import insert_bulk_users
from process import clean_data, read_in_csv

app = Flask(__name__)

# Set upload folder and size limit
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Only allow CSV files
ALLOWED_EXTENSIONS = {'csv'}

# Check if a file is an allowed type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page: form for uploading CSV
@app.route("/")
def index():
    return render_template("upload.html")

# Route for handling file upload
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Redirect to /view/<filename> to show contents
        insert_bulk_users(clean_data(read_in_csv(filepath)))
        return redirect(url_for('view_file', filename=filename))

    return "Invalid file type"

@app.route("/view/<filename>")
def view_file(filename):
    return f"File {filename} uploaded and processed successfully!"


# Entry point
if __name__ == "__main__":
    app.run(debug=True)
