import subprocess
import json

def local_ai_agent(prompt):
    # Run llama3 locally via ollama
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode("utf-8")

# Example usage
while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = local_ai_agent(user_input)
    print("Agent:", response.strip())
