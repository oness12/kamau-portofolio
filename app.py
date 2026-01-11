from flask import (
    Flask,
    render_template,
    request,
    abort,
    send_from_directory,
    redirect,
    session
)
import os
import json
import shutil

app = Flask(__name__)

# =========================
# SECURITY (LOCAL ADMIN)
# =========================
app.secret_key = "local-admin-secret"   # change if you want
ADMIN_PIN = "1234"                      # 🔒 change this PIN

# =========================
# BASE DIRECTORIES
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

CV_DIR = os.path.join(UPLOADS_DIR, "cv")
PROJECTS_DIR = os.path.join(UPLOADS_DIR, "projects")

CONTACT_JSON = os.path.join(DATA_DIR, "contact.json")
PROJECT_DESCRIPTIONS_JSON = os.path.join(DATA_DIR, "project_descriptions.json")

# =========================
# ENSURE FOLDERS EXIST
# =========================
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CV_DIR, exist_ok=True)
os.makedirs(PROJECTS_DIR, exist_ok=True)

# =========================
# ENSURE DATA FILES EXIST
# =========================
if not os.path.exists(CONTACT_JSON):
    with open(CONTACT_JSON, "w") as f:
        json.dump(
            {
                "email": "",
                "github": "",
                "linkedin": ""
            },
            f,
            indent=2
        )

if not os.path.exists(PROJECT_DESCRIPTIONS_JSON):
    with open(PROJECT_DESCRIPTIONS_JSON, "w") as f:
        json.dump({}, f, indent=2)

# =========================
# HELPERS
# =========================
def load_contact():
    with open(CONTACT_JSON, "r") as f:
        return json.load(f)

def load_project_descriptions():
    with open(PROJECT_DESCRIPTIONS_JSON, "r") as f:
        return json.load(f)

def preview_csv(filepath, max_rows=5):
    rows = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= max_rows:
                    break
                rows.append(line.strip().split(","))
    except Exception:
        pass
    return rows

# =========================
# HEALTH CHECK
# =========================
@app.route("/health")
def health():
    return {"status": "ok"}

# =========================
# PUBLIC PAGES
# =========================
@app.route("/")
def home():
    return render_template(
        "public/index.html",
        year=2026
    )

@app.route("/about")
def about():
    return render_template(
        "public/about.html",
        year=2026
    )

@app.route("/contact")
def contact():
    return render_template(
        "public/contact.html",
        contact=load_contact(),
        year=2026
    )

@app.route("/resume")
def resume():
    return render_template(
        "public/resume.html",
        year=2026
    )

@app.route("/projects")
def projects():
    files = []
    previews = {}
    descriptions = load_project_descriptions()

    for item in os.listdir(PROJECTS_DIR):
        path = os.path.join(PROJECTS_DIR, item)

        # Ignore folders (old system remnants)
        if not os.path.isfile(path):
            continue

        files.append(item)

        if item.lower().endswith(".csv"):
            previews[item] = preview_csv(path)

    return render_template(
        "public/projects.html",
        files=files,
        previews=previews,
        descriptions=descriptions,
        year=2026
    )

# =========================
# SERVE PROJECT FILES
# =========================
@app.route("/uploads/projects/<filename>")
def serve_project_file(filename):
    return send_from_directory(
        PROJECTS_DIR,
        filename,
        as_attachment=True
    )

# =========================
# CV DOWNLOAD
# =========================
@app.route("/cv")
def download_cv():
    files = os.listdir(CV_DIR)
    if not files:
        abort(404)
    return send_from_directory(
        CV_DIR,
        files[0],
        as_attachment=True
    )

# =========================
# ADMIN LOGIN
# =========================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        pin = request.form.get("pin")
        if pin == ADMIN_PIN:
            session["admin"] = True
            return redirect("/admin")
        return render_template(
            "admin/login.html",
            error="Invalid PIN"
        )

    return render_template("admin/login.html")

# =========================
# ADMIN DASHBOARD
# =========================
@app.route("/admin")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin/login")

    files = []
    descriptions = load_project_descriptions()

    for item in os.listdir(PROJECTS_DIR):
        if os.path.isfile(os.path.join(PROJECTS_DIR, item)):
            files.append(item)

    return render_template(
        "admin/dashboard.html",
        files=files,
        descriptions=descriptions
    )

# =========================
# ADMIN — UPLOAD PROJECT
# =========================
@app.route("/admin/upload-project-file", methods=["POST"])
def upload_project_file():
    if not session.get("admin"):
        abort(403)

    file = request.files.get("file")
    description = request.form.get("description", "").strip()

    if not file or file.filename == "":
        return {"error": "File required"}, 400

    if not description:
        return {"error": "Description required"}, 400

    file.save(os.path.join(PROJECTS_DIR, file.filename))

    descriptions = load_project_descriptions()
    descriptions[file.filename] = description

    with open(PROJECT_DESCRIPTIONS_JSON, "w") as f:
        json.dump(descriptions, f, indent=2)

    return redirect("/admin")

# =========================
# ADMIN — EDIT DESCRIPTION
# =========================
@app.route("/admin/edit-description", methods=["POST"])
def edit_description():
    if not session.get("admin"):
        abort(403)

    filename = request.form.get("filename")
    description = request.form.get("description", "").strip()

    if not filename or not description:
        return {"error": "Invalid input"}, 400

    descriptions = load_project_descriptions()
    descriptions[filename] = description

    with open(PROJECT_DESCRIPTIONS_JSON, "w") as f:
        json.dump(descriptions, f, indent=2)

    return redirect("/admin")

# =========================
# ADMIN — DELETE PROJECT
# =========================
@app.route("/admin/delete-project", methods=["POST"])
def delete_project():
    if not session.get("admin"):
        abort(403)

    filename = request.form.get("filename")
    if not filename:
        return {"error": "Filename required"}, 400

    path = os.path.join(PROJECTS_DIR, filename)

    if not os.path.exists(path):
        return {"error": "File not found"}, 404

    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    except PermissionError:
        return {"error": "Permission denied"}, 500

    descriptions = load_project_descriptions()
    if filename in descriptions:
        del descriptions[filename]
        with open(PROJECT_DESCRIPTIONS_JSON, "w") as f:
            json.dump(descriptions, f, indent=2)

    return redirect("/admin")

# =========================
# ADMIN — UPLOAD CV
# =========================
@app.route("/admin/upload-cv", methods=["POST"])
def upload_cv():
    if not session.get("admin"):
        abort(403)

    file = request.files.get("cv")
    if not file or file.filename == "":
        return {"error": "Invalid file"}, 400

    for existing in os.listdir(CV_DIR):
        os.remove(os.path.join(CV_DIR, existing))

    ext = os.path.splitext(file.filename)[1]
    file.save(os.path.join(CV_DIR, f"cv{ext}"))

    return redirect("/admin")

# =========================
# START SERVER
# =========================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


