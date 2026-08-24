import anthropic
from pydantic import BaseModel

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

class Triage(BaseModel):
    summary: str
    priority: str      # "low" | "medium" | "high" | "urgent"
    category: str
    suggested_action: str

ticket = """Subject: Can't reset my password — reset email never arrives
Body: I've clicked "Forgot password" about ten times and no email ever shows up
(checked spam too). I'm locked out of my account and I have a client demo in an
hour. Please help."""

resp = client.messages.parse(
    model="claude-haiku-4-5",     # cheap, fast tier — right choice for triage
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Triage this support ticket. Return summary, priority, "
                   f"category, and a suggested next action.\n\n{ticket}",
    }],
    output_format=Triage,
)

t = resp.parsed_output
print(f"Priority : {t.priority}")
print(f"Category : {t.category}")
print(f"Summary  : {t.summary}")
print(f"Action   : {t.suggested_action}")
