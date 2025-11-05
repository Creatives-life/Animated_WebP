import os
import uuid
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Import your compress function from Animated_WebP
# Make sure Animated_WebP.py doesn't auto-run on import
from Animated_WebP import compress_animated_webp

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
ALLOWED_EXTENSIONS = {"webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024
app.secret_key = "change-this-in-production"

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        quality = int(request.form.get("quality", 80))
    except ValueError:
        quality = 80
    try:
        resize_ratio = float(request.form.get("resize_ratio", 1.0))
    except ValueError:
        resize_ratio = 1.0
    duration_val = request.form.get("duration", "").strip()
    duration = int(duration_val) if duration_val.isdigit() else None

    files = request.files.getlist("file")
    if not files:
        flash("No file uploaded")
        return redirect(url_for("index"))

    processed = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_prefix = uuid.uuid4().hex[:8]
            saved_name = f"{unique_prefix}_{filename}"
            input_path = os.path.join(app.config["UPLOAD_FOLDER"], saved_name)
            file.save(input_path)

            output_name = f"compressed_{saved_name}"
            output_path = os.path.join(app.config["OUTPUT_FOLDER"], output_name)

            ok = compress_animated_webp(input_path, output_path, quality=quality, resize_ratio=resize_ratio, duration=duration)

            if ok:
                processed.append({
                    "original": saved_name,
                    "output": output_name,
                    "original_size_kb": round(os.path.getsize(input_path)/1024, 2),
                    "output_size_kb": round(os.path.getsize(output_path)/1024, 2)
                })
            else:
                processed.append({
                    "original": saved_name,
                    "error": "Processing failed"
                })
        else:
            processed.append({"original": getattr(file, "filename", "unknown"), "error": "Invalid extension (allowed: .webp)"})

    return render_template("result.html", processed=processed)

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

