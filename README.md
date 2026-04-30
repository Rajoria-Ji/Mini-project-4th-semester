# Customer Service Email Intelligence System

An AI-driven customer service dashboard built with **Python**, **Flask**, **SQLite**, **Scikit-Learn**, and **Google Gemini AI** that automatically classifies incoming customer emails by intent and sentiment, prioritizes them, and generates smart, personalized responses.

---

## Features

- **Interactive Dashboard:** View, filter, sort, and manage pending, resolved, escalated, and review-flagged customer emails.
- **NLP Engine:** Scikit-Learn (TF-IDF + Naïve Bayes) for intent detection — Refund, Complaint, Inquiry, Feedback.
- **Sentiment Analysis:** TextBlob-powered real-time polarity scoring (Positive, Neutral, Negative).
- **Auto-Prioritization:** Automatically flags emails as High 🔥, Medium ⚡, or Low 🟢 priority based on intent + sentiment logic.
- **Gemini AI Replies:** Google Gemini 2.0 Flash generates personalized, context-aware customer service replies.
- **Confidence Scoring:** Shows model confidence percentage; low-confidence emails are flagged for manual review.
- **Analytics Page:** Interactive Chart.js doughnut charts showing sentiment and priority distributions.
- **Dark / Light Theme:** Full theme system with accent color picker, font size, and table density settings.
- **Admin Controls:** Delete individual records, clear all records, resolve tickets, edit auto-replies.
- **Public Deployment:** ngrok tunnel support for instant public URL access without a cloud server.

---

## How to Run This Project

### Prerequisites
- Python 3.8+ installed
- Visual Studio Code (recommended)
- Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))
- ngrok account (free at [ngrok.com](https://ngrok.com)) — *only for public URL*

---

### Step-by-Step Setup

**1. Clone the Repository**
```bash
git clone https://github.com/Rajoria-Ji/Mini-project-4th-semester.git
cd Mini-project-4th-semester
```

**2. Create & Activate a Virtual Environment**
```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate
```
```bash
# Mac/Linux
python -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Secrets**

Copy the example config and fill in your values:
```bash
copy config.example.py config.py
```
Edit `config.py`:
```python
ADMIN_USERNAME = "your_username"
ADMIN_PASSWORD = "your_password"
GEMINI_API_KEY = "your_google_gemini_api_key"
SECRET_KEY     = "any_random_string"
```

**5. Train the ML Model**
```bash
python model.py
```
This generates `intent_model.pkl` and `vectorizer.pkl`.

**6. Run the Application**
```bash
python app.py
```
Open your browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### Admin Login
| Field | Value |
|---|---|
| Username | As set in `config.py` |
| Password | As set in `config.py` |

---

### Go Live (Public URL via ngrok)

1. Get your free auth token from [ngrok.com](https://ngrok.com)
2. Open `tunnel.py` and paste your token on line 15
3. Run:
```bash
python tunnel.py
```
Your app will be accessible from anywhere via a public HTTPS URL.

---

## Project Structure

```
Mini-project-4th-semester/
│
├── app.py                  # Flask backend (routes, ML pipeline, Gemini integration)
├── model.py                # ML model training (TF-IDF + Naïve Bayes)
├── tunnel.py               # ngrok public URL launcher
├── config.example.py       # Config template (copy to config.py and fill in secrets)
├── requirements.txt        # Python dependencies
│
├── templates/
│   ├── index.html          # Customer email submission page
│   ├── login.html          # Admin login page
│   ├── dashboard.html      # Main admin dashboard
│   ├── stats.html          # Analytics & charts page
│   ├── edit.html           # Edit auto-reply page
│   └── settings.html       # Theme & display settings
│
├── static/
│   ├── theme.css           # Light/dark theme CSS overrides
│   └── theme-init.js       # Theme preference loader (prevents FOUC)
│
├── intent_model.pkl        # Trained Naïve Bayes classifier
├── vectorizer.pkl          # Trained TF-IDF vectorizer
└── .gitignore              # Excludes config.py and database.db
```

---

## API Integration Guide

### Google Gemini AI (Already Integrated ✅)
The system uses **Google Gemini 2.0 Flash** (`google-genai` SDK) to generate personalized email replies. Configure your API key in `config.py`.

### Connecting a Real Email API (Gmail / Outlook / SendGrid)
**Where to add it:** `app.py` — `/` route

Instead of the manual submission form, integrate Gmail API or `imaplib` to automatically pull unread emails and insert them into the database. Use `smtplib` or SendGrid to send the approved reply back to the customer.

### Upgrading the ML Model
**Where to add it:** `model.py`

Replace the Naïve Bayes classifier with a fine-tuned BERT model (`transformers` library) for higher accuracy on complex emails.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask 3.0 (Python) |
| ML Classification | scikit-learn (TF-IDF + Naïve Bayes) |
| Sentiment Analysis | TextBlob |
| Generative AI | Google Gemini 2.0 Flash |
| Database | SQLite 3 |
| Frontend | HTML5 + Vanilla CSS + JavaScript |
| Charts | Chart.js |
| Icons | Font Awesome 6.5 |
| Public Tunnel | ngrok (pyngrok) |

---

## Screenshots

> Dashboard with dark mode, filter chips, confidence bars, and status badges.
> Analytics page with Chart.js doughnut charts and KPI cards.
> Settings page with theme toggle, accent colors, font size, and table density.

---

*Built as a Mini Project — 4th Semester | AI & Web Technologies*
