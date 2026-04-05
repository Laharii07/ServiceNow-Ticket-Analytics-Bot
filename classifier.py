import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Category rules — keyword → category
CATEGORY_RULES = {
    "Finance/Expense": ["amex", "expense", "reimbursement", "invoice", "receipt", "payroll", "payment"],
    "IT/Access":       ["login", "password", "access", "laptop", "computer", "printer", "outlook", "teams", "sharepoint"],
    "HR/Onboarding":   ["visa", "letter", "onboarding", "new joiner", "contract", "hr", "emergency contact"],
    "Travel/Booking":  ["flight", "hotel", "train", "booking", "travel", "transport", "uber"],
}

DEADLINE_KEYWORDS = ["urgent", "urgently", "tonight", "today", "by end of day", "eod", "deadline", "asap", "before friday"]

def classify_ticket(text: str) -> dict:
    text_lower = text.lower()
    doc = nlp(text_lower)
    
    # Category: score each category by keyword hits
    scores = {cat: 0 for cat in CATEGORY_RULES}
    for cat, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in text_lower:
                scores[cat] += 1
    
    best_cat = max(scores, key=scores.get)
    if scores[best_cat] == 0:
        best_cat = "General/Other"
    
    # Priority: if deadline keyword found → High
    has_deadline = any(kw in text_lower for kw in DEADLINE_KEYWORDS)
    priority = "High" if has_deadline else "Medium"
    
    return {
        "category": best_cat,
        "priority": priority,
        "has_deadline": has_deadline,
        "confidence": min(1.0, scores.get(best_cat, 0) / 3)
    }

# Test it
if __name__ == "__main__":
    test = "I need help with my Amex – urgent client dinner tonight"
    result = classify_ticket(test)
    print(result)
    # → {'category': 'Finance/Expense', 'priority': 'High', 'has_deadline': True, ...}
