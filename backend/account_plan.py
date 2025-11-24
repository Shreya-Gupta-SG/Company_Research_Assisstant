# account_plan.py
def generate_account_plan(company, profile, news_items):
    """
    Generate a smart account plan WITHOUT using OpenAI.
    Uses rule-based logic to extract insights from news articles.
    This makes the project 100% FREE & ASSESSMENT READY.
    """

    # --- BASIC DETAILS ---
    name = profile.get("name", company)
    summary = profile.get("summary", "No summary available")
    description = profile.get("description", "Not available")
    source = profile.get("source", "Wikipedia / Public Data")

    # --- SMART INSIGHT EXTRACTION FROM NEWS ---
    opportunities = []
    risks = []
    strategy = []

    for article in news_items:
        text = (article.get('title', '') + " " + article.get('description', '')).lower()

        # Opportunity detection
        if "acquisition" in text or "merger" in text or "expansion" in text:
            opportunities.append("Potential expansion or M&A activity detected.")
        if "partnership" in text:
            opportunities.append("Possible strategic partnership opportunity.")
        if "ai" in text or "automation" in text:
            opportunities.append("AI/automation development → technology collaboration possible.")

        # Risk detection
        if "lawsuit" in text or "legal" in text:
            risks.append("Legal challenges mentioned in news.")
        if "loss" in text or "layoff" in text or "decrease" in text:
            risks.append("Financial or workforce instability reported.")

        # Strategy suggestions
        if "investment" in text:
            strategy.append("Approach via solution-driven investment proposals.")
        if "innovation" in text:
            strategy.append("Focus pitch on innovation & R&D collaboration.")

    # --- FALLBACK IF NOTHING FOUND ---
    if not opportunities:
        opportunities.append("General opportunity for industry collaboration.")
    if not risks:
        risks.append("No major risks detected from news.")
    if not strategy:
        strategy.append("Build relationship via business discussions first.")

    # --- FINAL STRUCTURED PLAN ---
    plan = {
        "Overview": f"{name} — {summary}\n\nDescription: {description}\nSource: {source}",
        "Key Contacts": (
            "Key contacts not auto-detected.\n"
            "You may include roles like:\n"
            "- CEO / Director\n"
            "- CFO / Finance Head\n"
            "- IT / Procurement Head"
        ),
        "Recent News": format_news(news_items),
        "Opportunities": "\n".join(opportunities),
        "Risks": "\n".join(risks),
        "Strategy": "\n".join(strategy),
    }

    return plan


def format_news(news_items):
    """Convert news into a clean bullet format."""
    if not news_items:
        return "No recent news found."

    news_text = "Top News:\n"
    for art in news_items[:5]:
        title = art.get("title", "No title")
        url = art.get("url", "#")
        news_text += f"- {title} (Source: {url})\n"
    return news_text


def update_plan_section(plan, section, content):
    section = section.strip().title()  # fixes lowercase / mismatch
    if section in plan:
        plan[section] += f"\n\n🔄 UPDATED: {content}"   # append new info
    else:
        plan[section] = content  # if new section, create it
    return plan

