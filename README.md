# Customer Service Email Intelligence System

An AI-driven customer service dashboard built with Python, Flask, SQLite, and Scikit-Learn that automatically classifies incoming customer emails by intent and sentiment, prioritizes them, and generates smart draft responses.

## Features
- **Interactive Dashboard:** View pending and resolved customer emails.
- **NLP Engine:** Scikit-Learn models for identifying email Intent (shipping, refund, support, complaint, feedback) and Sentiment (Positive, Neutral, Negative). 
- **Auto-Prioritization:** Automatically flags emails as High, Medium, or Low priority.
- **Smart Response Generation:** Drafts contextual replies based on the AI's classification.
- **Dark Mode Support:** Built-in dark theme for the agent dashboard.

---

## How to Run This Project in VS Code

### Prerequisites
- Python 3.8+ installed on your machine.
- Visual Studio Code.

### Step-by-Step Instructions
1. **Open the Project:**
   Open Visual Studio Code, go to `File > Open Folder`, and select the project directory (`MINI PROJECT (23-03-26)`).

2. **Open a New Terminal:**
   In VS Code, go to the top menu and click `Terminal > New Terminal`.

3. **Create a Virtual Environment:**
   Run the following command in the terminal to keep dependencies isolated:
   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment:**
   - On **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\activate
     ```
   - On **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Application:**
   ```bash
   python app.py
   ```
   *Note: Running `app.py` for the first time will automatically initialize the `emails.db` SQLite database and train the NLP models (generating `nlp_model.pkl`).*

7. **View the Dashboard:**
   Open your web browser and navigate to: [http://127.0.0.1:5001/](http://127.0.0.1:5001/)

---

## API Integration Guide

Currently, this system uses a local machine learning model (`scikit-learn`) and simulated manual inputs. If you want to connect this system to real platforms, here is where and how you can integrate external APIs:

### 1. Connecting a Real Email API (e.g., Gmail API, MS Graph, SendGrid)
**Where to add it:** `app.py`

- **Fetching Real Emails:** Instead of using the frontend "Simulate" button to mock an email, you can integrate the Gmail API to pull real unread emails. You can add a background scheduler (like `APScheduler` or a cron job) that periodically fetches emails and inserts them into our SQLite database using the `/api/emails` logic.
- **Sending the Approved Draft:** In the `@app.route('/api/emails/<int:email_id>/approve', methods=['PUT'])` route, right before `conn.commit()`, you can utilize `smtplib` or an API like SendGrid to actually send the `edited_response` back to the customer's email address (`email.sender`).

### 2. Using an Advanced Generative AI API (e.g., OpenAI / ChatGPT)
**Where to add it:** `nlp_engine.py` and `response_generator.py`

To upgrade the text analysis from traditional Scikit-Learn logic to advanced Large Language Models:
- **Upgrading Analysis:** In `nlp_engine.py`, replace the `analyze_text()` machine learning prediction lines with an API call to `openai.ChatCompletion.create()`. You can pass the email body to the LLM and prompt it to return a JSON object containing the computed Intent, Sentiment, and Confidence score.
- **Upgrading Drafts:** In `response_generator.py`, instead of using static Python dictionaries/templates, you can call the OpenAI API. Pass the customer's original email and the categorized Intent, and ask the LLM to generate a highly personalized, dynamic response.
