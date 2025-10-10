# review_utils.py
import re
import javalang
from openai import OpenAI

client = OpenAI()

def static_checks(java_code):
    issues = []
    lines = java_code.split("\n")
    for i, line in enumerate(lines, start=1):
        if line.strip() and not line.strip().endswith((";", "{", "}", "//", "/*")):
            if not re.match(r".*class .*|.*if.*|.*for.*|.*while.*|.*else.*", line):
                issues.append(f"Line {i}: Possible missing semicolon.")
    if "System.out.println" in java_code:
        issues.append("Avoid using System.out.println in production code. Use Logger instead.")
    if re.search(r'catch\s*\(.*\)\s*\{\s*\}', java_code):
        issues.append("Empty catch block found. Handle exceptions properly.")
    return issues

def ai_suggestions(java_code, static_issues):
    prompt = f"""
    You are a senior Java reviewer.
    The following static analysis issues were detected:
    {static_issues}

    Based on these findings, suggest practical improvements or refactoring ideas.

    Code:
    {java_code}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in Java static analysis and clean code."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
