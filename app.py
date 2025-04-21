from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from dag.job import data_pipeline  # updated import

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)

        # Dagster execution
        result = data_pipeline.execute_in_process(
            run_config={
                "ops": {
                    "read_csv_op": {
                        "inputs": {
                            "filepath": filepath
                        }
                    }
                }
            }
        )

        if result.success:
            return redirect(url_for('view_file', filename=filename))
        else:
            return "Dagster pipeline failed. Check Dagit logs."

    return "Invalid file type"

@app.route("/view/<filename>")
def view_file(filename):
    return f"File {filename} uploaded and processed successfully!"

if __name__ == "__main__":
    app.run(debug=True)
