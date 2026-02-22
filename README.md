# Personality Growth Tracker
#### Video Demo:  <URL (https://youtu.be/6042QrQiIuU)>
#### Description:

A web application built with Flask that lets users take the **Big Five (OCEAN) personality test** and track their results over time.

---

## What is the Big Five (OCEAN)?

The Big Five is a widely used psychological model that measures personality across five traits:

| **O** | Openness | Preserver | Moderate | Explorer |
| **C** | Conscientiousness | Flexible | Balanced | Focused |
| **E** | Extraversion | Introvert | Ambivert | Extrovert |
| **A** | Agreeableness | Challenger | Negotiator | Adapter |
| **N** | Neuroticism | Resilient | Responsive | Reactive |

The test has **10 questions** — 2 per trait. Each answer has a value from 1 to 5. The two scores for each trait are added together, giving a score between 2 and 10 per trait.

---

## Features

- User registration and login with hashed passwords
- 10-question personality assessment
- Automatic OCEAN score calculation per trait
- Results page showing a full breakdown table with progress bars
- History page showing all past attempts ordered by date and time
- No right or wrong answers — values are summed, not graded

---

## Tech Stack

- **Python / Flask** — backend web framework
- **CS50 SQL** — SQLite database wrapper
- **SQLite** — local database
- **Bootstrap 5** — frontend styling
- **Jinja2** — HTML templating
- **Werkzeug** — password hashing

---

## How Scoring Works

1. User submits the form with 10 answers (`q1` through `q10`)
2. Flask reads each answer's numeric value (1–5)
3. Values are grouped and summed by trait (2 questions × max 5 = 10 per trait)
4. The 5 trait scores are saved to the database
5. Each score is classified:
   - **2–4** → Low
   - **5–7** → Mid
   - **8–10** → High

Individual answers are not stored — only the final trait scores.

---

## Running Locally

**1. Clone or download the project**

**2. Install dependencies**
```bash
pip install flask flask-session cs50 werkzeug
```

**3. Run the app**
```bash
flask run
```

**4. Open in browser**
```
http://127.0.0.1:5000
```

The database and tables are created automatically on first run.

---

## Deployment

This app is recommended to be deployed on **PythonAnywhere** (pythonanywhere.com) as it natively supports Flask and SQLite with no code changes required.

**Steps:**
1. Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload all project files via the Files tab
3. Open a Bash console and install dependencies:
   ```bash
   pip install --user flask flask-session cs50 werkzeug
   ```
4. Go to the **Web** tab → Add a new web app → Choose Flask
5. Set the source code path to your `app.py`
6. Reload the web app

> **Note:** Vercel is not recommended for this project as it does not support SQLite persistence or filesystem-based sessions.

---

## Author

**Maruf**
