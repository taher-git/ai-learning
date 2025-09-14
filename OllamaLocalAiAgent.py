import ollama
from duckduckgo_search import DDGS
import os

# =========================
# Tools
# =========================

# Chat with local Llama3 model
def chat_llama(prompt):
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# Web search using DuckDuckGo
def web_search(query, max_results=3):
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=max_results)]
    return "\n".join([f"- {r['title']} ({r['href']})" for r in results])

# Notes storage
NOTES_FILE = "notes.txt"

def save_note(content):
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(content + "\n")
    return "📝 Note saved."

def read_notes():
    if not os.path.exists(NOTES_FILE):
        return "No notes found."
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

# =========================
# Agent Logic
# =========================

def ai_agent(task):
    # System instructions for the agent
    system_prompt = f"""
    You are a personal AI assistant. The user asked: "{task}".
    - If they say "search:" then extract the query and perform a web search.
    - If they say "note:" then save the text after it into notes.
    - If they say "show notes", return all saved notes.
    - Otherwise, answer directly using your own reasoning.
    """

    # Ask Llama to decide action
    decision = chat_llama(system_prompt).lower()

    # Handle actions
    if decision.startswith("search:"):
        query = decision.replace("search:", "").strip()
        return web_search(query)

    elif decision.startswith("note:"):
        note_text = decision.replace("note:", "").strip()
        return save_note(note_text)

    elif "show notes" in decision:
        return read_notes()

    else:
        return decision

# =========================
# Main Loop
# =========================

if __name__ == "__main__":
    print("🤖 Personal Assistant Ready! (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye 👋")
            break
        print("Agent:", ai_agent(user_input))
