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
import uuid

app = Flask(__name__)
app.secret_key = "local-admin-secret"
ADMIN_PIN = "1234"

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

PROJECTS_DIR = os.path.join(UPLOADS_DIR, "projects")
CV_DIR = os.path.join(UPLOADS_DIR, "cv")

CONTACT_JSON = os.path.join(DATA_DIR, "contact.json")
PROJECT_DESCRIPTIONS_JSON = os.path.join(DATA_DIR, "project_descriptions.json")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROJECTS_DIR, exist_ok=True)
os.makedirs(CV_DIR, exist_ok=True)

# =========================
# DATA FILES
# =========================
if not os.path.exists(CONTACT_JSON):
    with open(CONTACT_JSON, "w") as f:
        json.dump({
            "email": "kamauthetech@gmail.com",
            "github": "https://github.com/oness12",
            "linkedin": "https://linkedin.com"
        }, f, indent=2)

if not os.path.exists(PROJECT_DESCRIPTIONS_JSON):
    with open(PROJECT_DESCRIPTIONS_JSON, "w") as f:
        json.dump({}, f, indent=2)

# =========================
# HELPERS
# =========================
def load_contact():
    with open(CONTACT_JSON) as f:
        return json.load(f)

def load_descriptions():
    with open(PROJECT_DESCRIPTIONS_JSON) as f:
        return json.load(f)

# =========================
# PUBLIC ROUTES
# =========================
@app.route("/")
def home():
    return render_template("public/index.html", year=2026)

@app.route("/about")
def about():
    return render_template("public/about.html", year=2026)

@app.route("/contact")
def contact():
    return render_template(
        "public/contact.html",
        contact=load_contact(),
        year=2026
    )

@app.route("/projects")
def projects():
    descriptions = load_descriptions()
    files = sorted(
        [f for f in os.listdir(PROJECTS_DIR) if os.path.isfile(os.path.join(PROJECTS_DIR, f))]
    )

    return render_template(
        "public/projects.html",
        files=files,
        descriptions=descriptions,
        year=2026
    )

# =========================
# CV PAGES (FIXED)
# =========================
@app.route("/resume")
def resume():
    return render_template("public/resume.html", year=2026)

@app.route("/cv")
def serve_cv():
    files = os.listdir(CV_DIR)
    if not files:
        abort(404)
    return send_from_directory(CV_DIR, files[0])

# =========================
# FILE SERVING
# =========================
@app.route("/uploads/projects/<filename>")
def serve_project(filename):
    return send_from_directory(PROJECTS_DIR, filename, as_attachment=True)

# =========================
# ADMIN AUTH
# =========================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("pin") == ADMIN_PIN:
            session["admin"] = True
            return redirect("/admin")
        return render_template("admin/login.html", error="Invalid PIN")

    return render_template("admin/login.html")

@app.route("/admin")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin/login")

    descriptions = load_descriptions()
    files = sorted(os.listdir(PROJECTS_DIR))

    return render_template(
        "admin/dashboard.html",
        files=files,
        descriptions=descriptions
    )

# =========================
# ADMIN ACTIONS
# =========================
@app.route("/admin/upload-project-file", methods=["POST"])
def upload_project():
    if not session.get("admin"):
        abort(403)

    file = request.files.get("file")
    description = request.form.get("description", "").strip()

    if not file:
        abort(400)

    safe_name = f"{uuid.uuid4()}_{file.filename}"
    file.save(os.path.join(PROJECTS_DIR, safe_name))

    descriptions = load_descriptions()
    descriptions[safe_name] = description

    with open(PROJECT_DESCRIPTIONS_JSON, "w") as f:
        json.dump(descriptions, f, indent=2)

    return redirect("/admin")

@app.route("/admin/delete-project", methods=["POST"])
def delete_project():
    if not session.get("admin"):
        abort(403)

    filename = request.form.get("filename")
    path = os.path.join(PROJECTS_DIR, filename)

    if os.path.exists(path):
        os.remove(path)

    descriptions = load_descriptions()
    descriptions.pop(filename, None)

    with open(PROJECT_DESCRIPTIONS_JSON, "w") as f:
        json.dump(descriptions, f, indent=2)

    return redirect("/admin")

@app.route("/admin/upload-cv", methods=["POST"])
def upload_cv():
    if not session.get("admin"):
        abort(403)

    file = request.files.get("cv")
    if not file:
        abort(400)

    # Only one CV allowed
    for f in os.listdir(CV_DIR):
        os.remove(os.path.join(CV_DIR, f))

    ext = os.path.splitext(file.filename)[1]
    file.save(os.path.join(CV_DIR, f"cv{ext}"))

    return redirect("/admin")

# =========================
# SERVER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
