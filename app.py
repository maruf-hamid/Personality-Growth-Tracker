import os
from functools import wraps

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    """Decorator to require login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


#Questions
QUESTIONS = [
    {
        "id": 1, "trait": "E",
        "text": "... is reserved",
        "options": [
            {"label": "Disagree",          "value": 5},
            {"label": "Slightly disagree", "value": 4},
            {"label": "Neutral",           "value": 3},
            {"label": "Slightly agree",    "value": 2},
            {"label": "Agree",             "value": 1},
        ]
    },
    {
        "id": 2, "trait": "A",
        "text": "... is generally trusting",
        "options": [
            {"label": "Disagree",          "value": 1},
            {"label": "Slightly disagree", "value": 2},
            {"label": "Neutral",           "value": 3},
            {"label": "Slightly agree",    "value": 4},
            {"label": "Agree",             "value": 5},
        ]
    },
    {
        "id": 3, "trait": "C",
        "text": "... tends to be lazy",
        "options": [
            {"label": "Disagree",          "value": 5},
            {"label": "Slightly disagree", "value": 4},
            {"label": "Neutral",           "value": 3},
            {"label": "Slightly agree",    "value": 2},
            {"label": "Agree",             "value": 1},
        ]
    },
    {
        "id": 4, "trait": "N",
        "text": "... is relaxed, handles stress well",
        "options": [
            {"label": "Disagree",          "value": 5},
            {"label": "Slightly disagree", "value": 4},
            {"label": "Neutral",           "value": 3},
            {"label": "Slightly agree",    "value": 2},
            {"label": "Agree",             "value": 1},
        ]
    },
    {
        "id": 5, "trait": "O",
        "text": "... has few artistic interests",
        "options": [
            {"label": "Disagree",          "value": 5},
            {"label": "Slightly disagree", "value": 4},
            {"label": "Neutral",           "value": 3},
            {"label": "Slightly agree",    "value": 2},
            {"label": "Agree",             "value": 1},
        ]
    },
    {
        "id": 6, "trait": "E",
        "text": "... is outgoing, sociable",
        "options": [
            {"label": "Disagree",          "value": 1},
            {"label": "Slightly disagree", "value": 2},
            {"label": "Neutral",           "value": 3},
            {"label": "Slightly agree",    "value": 4},
            {"label": "Agree",             "value": 5},
        ]
    },
    {
        "id": 7, "trait": "A",
        "text": "... tends to find fault with others",
        "options": [
            {"label": "Disagree",          "value": 5},
            {"label": "Slightly disagree", "value": 4},
            {"label": "Neutral",           "value": 3},
            {"label": "Slightly agree",    "value": 2},
            {"label": "Agree",             "value": 1},
        ]
    },
    {
        "id": 8, "trait": "C",
        "text": "... does a thorough job",
        "options": [
            {"label": "Disagree",          "value": 1},
            {"label": "Slightly disagree", "value": 2},
            {"label": "Neutral",           "value": 3},
            {"label": "Slightly agree",    "value": 4},
            {"label": "Agree",             "value": 5},
        ]
    },
    {
        "id": 9, "trait": "N",
        "text": "... gets nervous easily",
        "options": [
            {"label": "Disagree",          "value": 1},
            {"label": "Slightly disagree", "value": 2},
            {"label": "Neutral",           "value": 3},
            {"label": "Slightly agree",    "value": 4},
            {"label": "Agree",             "value": 5},
        ]
    },
    {
        "id": 10, "trait": "O",
        "text": "... has an active imagination",
        "options": [
            {"label": "Disagree",          "value": 1},
            {"label": "Slightly disagree", "value": 2},
            {"label": "Neutral",           "value": 3},
            {"label": "Slightly agree",    "value": 4},
            {"label": "Agree",             "value": 5},
        ]
    },
]

# Trait display info
TRAITS = {
    "O": {"name": "Openness",          "low": "Preserver", "mid": "Moderate",   "high": "Explorer"},
    "C": {"name": "Conscientiousness", "low": "Flexible",  "mid": "Balanced",   "high": "Focused"},
    "E": {"name": "Extraversion",      "low": "Introvert", "mid": "Ambivert",   "high": "Extrovert"},
    "A": {"name": "Agreeableness",     "low": "Challenger","mid": "Negotiator", "high": "Adapter"},
    "N": {"name": "Neuroticism",       "low": "Resilient", "mid": "Responsive", "high": "Reactive"},
}


def get_label(score):
    """Return low/mid/high label key based on score 2–10."""
    if score <= 4:
        return "low"
    elif score <= 7:
        return "mid"
    else:
        return "high"


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username     = request.form.get("username", "").strip()
        password     = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        # Validate inputs
        if not username:
            return render_template("register.html", error="Username is required.")
        if not password:
            return render_template("register.html", error="Password is required.")
        if password != confirmation:
            return render_template("register.html", error="Passwords do not match.")

        # Check if username already taken
        existing = db.execute("SELECT id FROM users WHERE username = ?", username)
        if existing:
            return render_template("register.html", error="Username already taken.")

        # Store new user
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            generate_password_hash(password)
        )

        # Log them in automatically
        rows = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username:
            return render_template("login.html", error="Username is required.")
        if not password:
            return render_template("login.html", error="Password is required.")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("login.html", error="Invalid username or password.")

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/test", methods=["GET", "POST"])
@login_required
def test():
    if request.method == "POST":
        # ── Step 1: Read values from form ──────────────────────────────
        # Each question submits q1, q2, ... q10 with a numeric value 1–5
        trait_scores = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}

        for q in QUESTIONS:
            raw = request.form.get(f"q{q['id']}")
            if raw:
                trait_scores[q["trait"]] += int(raw)

        # ── Step 2: Store the 5 trait scores in the database ──────────
        db.execute(
            "INSERT INTO results (user_id, O, C, E, A, N) VALUES (?, ?, ?, ?, ?, ?)",
            session["user_id"],
            trait_scores["O"],
            trait_scores["C"],
            trait_scores["E"],
            trait_scores["A"],
            trait_scores["N"]
        )

        # ── Step 3: Redirect to results ────────────────────────────────
        return redirect("/results")
    else:
        return render_template("test.html", questions=QUESTIONS)


@app.route("/description")
@login_required
def description():
    return render_template("description.html")


@app.route("/history")
@login_required
def history():
    rows = db.execute(
        "SELECT O, C, E, A, N, taken_at FROM results WHERE user_id = ? ORDER BY taken_at DESC",
        session["user_id"]
    )

    # Build a list where each entry has the timestamp + all 5 trait details
    history = []
    for row in rows:
        traits = []
        for t in ["O", "C", "E", "A", "N"]:
            score = row[t]
            level = get_label(score)
            traits.append({
                "key":   t,
                "name":  TRAITS[t]["name"],
                "score": score,
                "label": TRAITS[t][level],
                "level": level,
            })
        history.append({
            "taken_at": row["taken_at"],
            "traits":   traits,
        })

    return render_template("history.html", history=history)


@app.route("/results")
@login_required
def results():
    # Fetch the most recent result for this user
    row = db.execute(
        "SELECT O, C, E, A, N, taken_at FROM results WHERE user_id = ? ORDER BY taken_at DESC LIMIT 1",
        session["user_id"]
    )

    if not row:
        return render_template("results.html", result=None)

    row = row[0]

    # ── Calculate label (low/mid/high) for each trait ──────────────────
    result = []
    for t in ["O", "C", "E", "A", "N"]:
        score = row[t]
        level = get_label(score)
        result.append({
            "key":   t,
            "name":  TRAITS[t]["name"],
            "score": score,
            "label": TRAITS[t][level],
            "level": level,
        })

    return render_template("results.html", result=result, taken_at=row["taken_at"])
