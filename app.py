from flask import Flask, render_template, request, redirect, session
import sqlite3
from textblob import TextBlob
import pickle
from google import genai
from config import ADMIN_USERNAME, ADMIN_PASSWORD, GEMINI_API_KEY, SECRET_KEY

# ---------------- GEMINI AI SETUP ----------------
GEMINI_API_KEY = GEMINI_API_KEY
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def generate_ai_reply(subject, content, intent, sentiment, priority):
    """Generate a smart customer service reply using Gemini AI."""
    prompt = f"""You are a professional customer service representative. Write a polite, empathetic, and helpful reply to the following customer email.

Email Subject: {subject}
Email Content: {content}

AI Analysis:
- Detected Intent: {intent}
- Detected Sentiment: {sentiment}
- Priority Level: {priority}

Instructions:
- Be warm and professional
- Address their specific issue directly
- Keep the reply concise (3-5 sentences max)
- Do NOT mention that you are an AI
- Start with a greeting and end with a closing

Write only the reply message, nothing else."""

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        # Fallback replies if API fails
        fallbacks = {
            "refund":    "Thank you for reaching out. Your refund request has been received and our team will process it within 3-5 business days. We apologize for any inconvenience caused.",
            "complaint": "We sincerely apologize for the experience you've had. Your concern has been escalated to our team and we will resolve this as quickly as possible.",
            "inquiry":   "Thank you for your question! Our support team has received your inquiry and will get back to you with a detailed response within 24 hours.",
            "feedback":  "Thank you so much for your kind feedback! We truly appreciate you taking the time to share your experience with us."
        }
        return fallbacks.get(intent, "Thank you for contacting us. Our team will get back to you shortly.")

app = Flask(__name__)
app.secret_key = SECRET_KEY

ADMIN_USERNAME = ADMIN_USERNAME
ADMIN_PASSWORD = ADMIN_PASSWORD

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("intent_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------- INIT DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            content TEXT,
            sentiment TEXT,
            intent TEXT,
            auto_reply TEXT,
            status TEXT,
            priority TEXT,
            confidence REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["user"] = ADMIN_USERNAME
            return redirect("/dashboard")
        else:
            return "Invalid Credentials"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ---------------- HOME ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        subject = request.form["subject"]
        content = request.form["content"]

        # Sentiment
        analysis = TextBlob(content)
        polarity = analysis.sentiment.polarity

        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # Intent + Confidence
        X_new = vectorizer.transform([content])
        intent = model.predict(X_new)[0]
        confidence = round(max(model.predict_proba(X_new)[0]) * 100, 2)

        # Priority Logic (needed before AI reply for context)
        if intent == "complaint" and sentiment == "Negative":
            priority = "High"
        elif intent == "refund":
            priority = "Medium"
        elif intent == "complaint":
            priority = "Medium"
        else:
            priority = "Low"

        status = "Pending"

        # Manual Review override
        if confidence < 60:
            status = "Needs Review"
            priority = "High"

        # Escalation
        if priority == "High" and sentiment == "Negative":
            status = "Escalated"

        # Auto Reply via Gemini AI
        auto_reply = generate_ai_reply(subject, content, intent, sentiment, priority)

        # If confidence is low, prepend a note
        if confidence < 60:
            auto_reply = "[Under Review] " + auto_reply



        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO emails
            (subject, content, sentiment, intent, auto_reply, status, priority, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (subject, content, sentiment, intent, auto_reply, status, priority, confidence))
        conn.commit()
        conn.close()

    return render_template("index.html")

# ---------------- DASHBOARD (ADVANCED) ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    status = request.args.get("status")
    priority = request.args.get("priority")
    intent = request.args.get("intent")
    sentiment = request.args.get("sentiment")
    sort = request.args.get("sort")

    query = "SELECT * FROM emails WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    if priority:
        query += " AND priority = ?"
        params.append(priority)

    if intent:
        query += " AND intent = ?"
        params.append(intent)

    if sentiment:
        query += " AND sentiment = ?"
        params.append(sentiment)

    # Sorting
    if sort == "latest":
        query += " ORDER BY id DESC"
    elif sort == "high_conf":
        query += " ORDER BY confidence DESC"
    elif sort == "low_conf":
        query += " ORDER BY confidence ASC"
    else:
        query += " ORDER BY id ASC"

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(query, params)
    emails = c.fetchall()
    conn.close()

    return render_template("dashboard.html", emails=emails)

# ---------------- RESOLVE ----------------
@app.route("/resolve/<int:id>")
def resolve(id):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE emails SET status='Resolved' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# ---------------- DELETE SINGLE ----------------
@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM emails WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# ---------------- CLEAR ALL ----------------
@app.route("/clear", methods=["POST"])
def clear_all():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM emails")
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# ---------------- EDIT ----------------
@app.route("/edit/<int:id>")
def edit(id):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM emails WHERE id=?", (id,))
    email = c.fetchone()
    conn.close()
    return render_template("edit.html", email=email)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if "user" not in session:
        return redirect("/login")

    updated_reply = request.form["auto_reply"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE emails SET auto_reply=? WHERE id=?", (updated_reply, id))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# ---------------- STATS ----------------
@app.route("/stats")
def stats():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    def count(q):
        c.execute(q)
        return c.fetchone()[0]

    total = count("SELECT COUNT(*) FROM emails")
    pending = count("SELECT COUNT(*) FROM emails WHERE status='Pending'")
    resolved = count("SELECT COUNT(*) FROM emails WHERE status='Resolved'")
    escalated = count("SELECT COUNT(*) FROM emails WHERE status='Escalated'")
    review = count("SELECT COUNT(*) FROM emails WHERE status='Needs Review'")

    positive = count("SELECT COUNT(*) FROM emails WHERE sentiment='Positive'")
    neutral = count("SELECT COUNT(*) FROM emails WHERE sentiment='Neutral'")
    negative = count("SELECT COUNT(*) FROM emails WHERE sentiment='Negative'")

    high_priority = count("SELECT COUNT(*) FROM emails WHERE priority='High'")
    medium_priority = count("SELECT COUNT(*) FROM emails WHERE priority='Medium'")
    low_priority = count("SELECT COUNT(*) FROM emails WHERE priority='Low'")

    conn.close()

    return render_template("stats.html",
                           total=total,
                           pending=pending,
                           resolved=resolved,
                           escalated=escalated,
                           review=review,
                           positive=positive,
                           neutral=neutral,
                           negative=negative,
                           high_priority=high_priority,
                           medium_priority=medium_priority,
                           low_priority=low_priority)

# ---------------- SETTINGS ----------------
@app.route("/settings")
def settings():
    if "user" not in session:
        return redirect("/login")
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)