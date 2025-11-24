// FINAL script.js

const messagesDiv = document.getElementById('messages');
const inputEl = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

let currentPlan = null;
let conflictFlag = false;
let lastCompany = "";

// 🧠 Add message to chatbox
function addMessage(text, sender = 'bot') {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ' + sender;

    const msgSpan = document.createElement('span');
    msgSpan.innerHTML = text;  // Allows bold + line breaks
    msgDiv.appendChild(msgSpan);

    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function handleUserInput() {
    const text = inputEl.value.trim();
    if (!text) return;
    addMessage(text, 'user'); // show user message
    inputEl.value = '';

    const lower = text.toLowerCase();

    // 👉 Start fresh for NEW company
    if (lower.startsWith("new company")) {
        currentPlan = null;
        conflictFlag = false;
        const newCompany = text.replace(/new company/i, "").trim();
        addMessage(`🔄 Starting fresh research on: <b>${newCompany}</b>`);
        lastCompany = newCompany;
        fetchCompanyData(newCompany);
        return;
    }

    // 👉 Detect new company without saying "new company"
    if (currentPlan && lower !== lastCompany && !lower.startsWith("update")) {
        addMessage(`🆕 It seems you are asking about a *NEW company*: <b>${text}</b><br>Starting fresh...`);
        currentPlan = null;
        conflictFlag = false;
        lastCompany = text;
        fetchCompanyData(text);
        return;
    }

    // Handle conflict response
    if (conflictFlag && lower === 'yes') {
        addMessage("🔎 Digging deeper into conflicting data...");
        conflictFlag = false;
        return;
    }

    // No current plan = treat input as company search
    if (!currentPlan) {
        lastCompany = text;
        fetchCompanyData(text);
        return;
    }

    // 🛠 UPDATE FEATURE (SAFE + FINAL)
    // 🛠 UPDATE FEATURE (FINAL POLISHED)
const updateMatch = text.match(/^update\s+(.+?)\s+with\s+(.+)/i);
if (updateMatch) {
    let section = updateMatch[1].trim(); 
    const newContent = updateMatch[2].trim();

    // Convert section correctly (e.g. "key contacts" → "Key Contacts")
    section = section
        .split(" ")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");

    addMessage(`🔧 Updating section "<b>${section}</b>"...`);

    const res = await fetch('/update_plan_section', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan: currentPlan, section, content: newContent })
    });

    const data = await res.json();
    currentPlan = data.plan;   // FIXED

    addMessage(`✔ Updated <b>${section}</b>:<br><b>${currentPlan[section]}</b>`);
    return;
}


    addMessage("❓ Try this format:<br><code>update strategy with focus on cloud solutions</code>");
}

// 🔎 Fetch Company Data
async function fetchCompanyData(company) {
    addMessage(`Searching for <b>${company}</b>...`);

    const res = await fetch('/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company })
    });
    const data = await res.json();

    if (data.conflict) {
        addMessage(`⚠ <b>${data.conflict}</b><br>Should I investigate further? (yes/no)`);
        conflictFlag = true;
    }

    addMessage("📄 Generating account plan...");
    const res2 = await fetch('/generate_account_plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company, profile: data.profile, news: data.news })
    });

    currentPlan = await res2.json();

    // 🌟 POLISHED final display
    for (let section in currentPlan) {
        addMessage(`<b>🧾 ${section}:</b><br>${currentPlan[section]}`);
    }

    addMessage("💡 You can now update any section using: <br><code>update overview with new info...</code>");
}

// ---------------- EVENT LISTENERS ----------------
sendButton.addEventListener('click', handleUserInput);
inputEl.addEventListener('keypress', e => {
    if (e.key === 'Enter') handleUserInput();
});
