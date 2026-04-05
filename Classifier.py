import openai

def classify_with_gpt(text: str) -> dict:
    client = openai.OpenAI()  # reads OPENAI_API_KEY from environment
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # cheapest, fastest — costs ~$0.001 per ticket
        messages=[{
            "role": "system",
            "content": """You are a helpdesk classifier. Reply ONLY with JSON like:
{"category": "Finance/Expense", "priority": "High", "reason": "mentions Amex and urgent deadline"}
Categories: Finance/Expense, IT/Access, HR/Onboarding, Travel/Booking, General/Other
Priorities: High (deadline or blocked work), Medium, Low"""
        }, {
            "role": "user",
            "content": text
        }],
        response_format={"type": "json_object"}
    )
    
    import json
    return json.loads(response.choices[0].message.content)
