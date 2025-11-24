import os
import requests
from flask import Flask, request, jsonify, send_from_directory, session
from newsapi import NewsApiClient
from dotenv import load_dotenv
from account_plan import generate_account_plan, update_plan_section
import re

# Load API keys
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Only working API now

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
app.secret_key = "super_secret_key"     # REQUIRED for chat memory / session

# ---------------- FRONTEND ROUTE ---------------- #
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')


# ------------- MAIN RESEARCH API ---------------- #
@app.route('/research', methods=['POST'])
def research():
    """
    Research a company using free APIs:
      - Wikipedia (NO KEY REQUIRED)
      - NewsAPI (if key exists)
      - Conflict detection
      - Chat memory: remembers last company/context
    """
    data = request.get_json()
    company = data.get("company", "").strip()

    # SAVE COMPANY INTO SESSION FOR FURTHER CHAT
    session["last_company"] = company  

    # ----------- 1. WIKIPEDIA (FREE) -----------
    profile = {}
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company}"
        resp = requests.get(url)
        data_wp = resp.json()

        # If ambiguous: try "(company)"
        if data_wp.get("type") == "disambiguation":
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company} (company)"
            resp = requests.get(url)
            data_wp = resp.json()

        profile = {
            "name": data_wp.get("title", company),
            "description": data_wp.get("description", "Not available"),
            "summary": data_wp.get("extract", "No valid summary available"),
            "source": "Wikipedia API (Free)"
        }
    except Exception as e:
        print("Wikipedia Error:", e)

    # ----------- 2. NEWSAPI (IF KEY EXISTS) -----------
    news_items = []
    if NEWS_API_KEY:
        try:
            newsapi = NewsApiClient(api_key=NEWS_API_KEY)
            all_articles = newsapi.get_everything(
                q=company,
                language='en',
                sort_by='publishedAt',
                page_size=5
            )
            news_items = all_articles.get('articles', [])
        except Exception as e:
            print("NewsAPI Error:", e)

    # ----------- 3. CONFLICT DETECTION -----------
    conflict_message = None
    text_pool = " ".join((n.get("title", "") + " " + n.get("description", "")) for n in news_items)

    # ⚠️ Your missing line is HERE (improved version below)
    amounts = re.findall(r'\$\s?[\d,]+(?:\.\d+)?', text_pool)

    if len(set(amounts)) >= 2:
        conflict_message = (
            "⚠ I found some complex or conflicting data in news. "
            "Should I investigate further? (yes / no)"
        )

    # SAVE CONTEXT FOR CHAT
    session["context"] = {
        "profile": profile,
        "news": news_items,
        "conflict": conflict_message,
    }

    return jsonify({
        "profile": profile,
        "news": news_items,
        "conflict": conflict_message
    })


# ------------- CHAT-LIKE CONTINUATION API ---------------- #
@app.route('/continue', methods=['POST'])
def continue_chat():
    """
    Keeps the conversation going based on last researched company.
    """
    user_message = request.get_json().get("message", "")

    if "last_company" not in session:
        return jsonify({"reply": "Please research a company first!"})

    company = session["last_company"]
    context = session.get("context", {})

    reply = f"You asked about: {user_message}\n\n"
    reply += f"Context from previous research on *{company}*:\n"
    reply += f"- Summary: {context.get('profile', {}).get('summary', 'No data')}\n"

    if context.get("conflict"):
        reply += f"- ⚠ Conflict found in news: {context['conflict']}\n"

    reply += "\nLet me know what to check next — competitors, revenue, market share, etc."

    return jsonify({"reply": reply})


# ---------------- ACCOUNT PLAN ROUTES ---------------- #
@app.route('/generate_account_plan', methods=['POST'])
def generate_account_plan_route():
    data = request.get_json()
    company = data.get("company", "")
    profile = data.get("profile", {})
    news_items = data.get("news", [])

    plan = generate_account_plan(company, profile, news_items)
    return jsonify(plan)


@app.route('/update_plan_section', methods=['POST'])
def update_section_route():
    data = request.get_json()
    plan = data.get("plan", {})
    section = data.get("section", "").lower()   # 🔥 make section lowercase
    content = data.get("content", "")

    updated_plan = update_plan_section(plan, section, content)

    # 🔥 IMPORTANT: wrap response inside "plan" object for frontend
    return jsonify({"plan": updated_plan})


# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)
