from openai import OpenAI

client = OpenAI()

def ai_agent(task):
    # Ask GPT to come up with a plan for the given task
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI agent that helps with tasks."},
            {"role": "user", "content": f"Your task is: {task}"}
        ]
    )
    return response.choices[0].message.content

# Example usage
print(ai_agent("Find three strategies to improve time management."))
