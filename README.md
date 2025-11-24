## 🧠 Company Research Assistant

Your Personal AI Agent for Real-Time Company Insights & Account Planning
An AI-powered tool designed to help sales teams, business analysts, and students research any company and instantly generate a strategic account plan based on live data like news, opportunities, risks, and key contacts.

## 📁 Project Structure
COMPANY/
│
├── backend/
│   ├── app.py                # Flask backend API
│   ├── account_plan.py       # AI logic & account planning
│   ├── requirements.txt      # All dependencies
│   ├── .env                  # API keys (not pushed to GitHub)
│   └── venv/                 # Virtual environment
│
├── frontend/
│   ├── index.html            # UI template
│   ├── script.js             # Chatbot logic
│   └── style.css             # UI styling
│
└── README.md                 # Project documentation

## 🚀 Features
✔ AI-powered company research (profile + news)
✔ Dynamic account planning with sections:
  Key Contacts
  Opportunities
  Overview
  Recent News
  Risks
  Strategy
   ✔ Real-time data fetching
   ✔ Update any section with natural language (update strategy with focus on AI collaboration)
   ✔ Detects new company automatically
   ✔ User-friendly chat interface with animations

## 🏗️ Architecture Overview
🔹 Frontend (Vanilla JS)
File	Purpose
index.html	UI container for chatbot
script.js	Chat logic, fetch calls to backend
style.css	Gradient background + message styling
🔹 Backend (Flask)
File	Purpose
app.py	API endpoints (/research, /generate_account_plan, /update_plan_section)
account_plan.py	AI logic to generate each section
.env	API keys like NEWS_API_KEY, OPENAI_API_KEY

## ⚙️ Setup Instructions
🔹 1️⃣ Clone the Repository
git clone https://github.com/your-username/company-research-assistant.git
cd company-research-assistant
🔹 2️⃣ Create Virtual Environment
cd backend
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux
🔹 3️⃣ Install Dependencies
pip install -r requirements.txt
🔹 4️⃣ Create .env File (Inside /backend/)
OPENAI_API_KEY=YOUR_KEY
NEWS_API_KEY=YOUR_KEY
🔹 5️⃣ Run Backend Server
python app.py
🔹 6️⃣ Run Frontend
Open frontend/index.html in your browser
(or use Live Server in VS Code)

## 🧠 Design Decisions
Flask instead of FastAPI: Lightweight, easy integration with frontend
Modular backend (account_plan.py): Easy AI modification
Update feature: Makes agent more interactive
Automatic company detection: Makes experience seamless

## 📌 Future Improvements
Convert frontend to React / Next.js
Add user login + history saving
Deploy using Render / Railway / Docker

---

## 👩‍💻 Author
Developed by **Shreya Gupta**
LinkedIn: [https://www.linkedin.com/in/your-profile link](https://www.linkedin.com/in/shreya-gupta-29161b222/)
