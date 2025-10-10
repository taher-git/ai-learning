import re
import javalang
import os
from openai import OpenAI
import json

categories = {
    "Bug": [],
    "Refactor": [],
    "Style": []
}

def analyze_java_code(code):
    """
    Analyze structure of Java code using javalang parser
    """
    tree = javalang.parse.parse(code)
    info = {
        "classes": [],
        "methods": [],
        "imports": [],
    }

    # Get class and method names
    for _, node in tree:
        if isinstance(node, javalang.tree.ClassDeclaration):
            info["classes"].append(node.name)
        elif isinstance(node, javalang.tree.MethodDeclaration):
            info["methods"].append(node.name)
        elif isinstance(node, javalang.tree.Import):
            info["imports"].append(node.path)

    return info

def check_security_issues(code: str):
    issues = []
    patterns = {
        "Hardcoded password": r'password\s*=\s*["\'].*["\']',
        "Potential SQL Injection": r'Statement\s*\w*\s*=\s*conn\.createStatement',
        "Weak encryption": r'(MD5|SHA1)',
        "User input in file path": r'FileInputStream\s*\(.*userInput.*\)',
    }
    for desc, pat in patterns.items():
        if re.search(pat, code, re.IGNORECASE):
            issues.append(desc)
    return issues

def check_performance_issues(code: str):
    issues = []
    patterns = {
        "Inefficient loop": r'for\s*\(.*list\.size\(\).*',
        "Repeated object creation": r'new\s+\w+\(.*\)\s*;',
        "Unclosed stream": r'File(Input|Output)Stream',
    }
    for desc, pat in patterns.items():
        if re.search(pat, code):
            issues.append(desc)
    return issues

client = OpenAI()
def ai_code_review(java_code, structure):
    """
    Sends structured info + code to GPT for intelligent review
    """
    prompt = f"""
    You are an expert Java reviewer.
    Here is code structure:
    Classes: {structure['classes']}
    Methods: {structure['methods']}
    Imports: {structure['imports']}

    Review this Java code for:
    - Code smells
    - Redundant logic
    - Unused methods/imports
    - Better design patterns
    - Security flaws (injection, weak crypto, unsafe I/O)
    - Readability and maintainability.
    - Suggest  exact fixes, variable renaming, comment improvements, and structure changes

    Code:
    {java_code}
    """
    ai_review = call_gpt_api(prompt)
    return ai_review

def ai_code_review_by_category(java_code):
    prompt = f"""
    You are a senior Java code reviewer.
    Classify your review under these 3 categories:

    1. Bug — potential runtime or logic errors
    2. Refactor — code structure, redundancy, modularization
    3. Style — naming, comments, readability

    Each issue must have a severity level (High / Medium / Low).

    Return *only* JSON in this format:
    {{
    "Bug": [{{"issue": "string", "severity": "High"}}],
    "Refactor": [{{"issue": "string", "severity": "Medium"}}],
    "Style": [{{"issue": "string", "severity": "Low"}}]
    }}
    
    Code:
    {java_code}
    """
    ai_review = call_gpt_api(prompt)
    ai_review = re.sub(r'```(json)?', '', ai_review).strip()
    ai_results = json.loads(ai_review)

    combined = {
        "Bug": ai_results.get("Bug", []),
        "Refactor": ai_results.get("Refactor", []),
        "Style": ai_results.get("Style", [])
    }

    return combined

def call_gpt_api(prompt):
    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior Java code reviewer."},
                {"role": "user", "content": prompt}
            ]
        )
    return response.choices[0].message.content

if __name__ == "__main__":
    java_code = open("AI Agent Demo/backend/Code Reviewer/data/Calculator").read()  # or paste code here
    structure = analyze_java_code(java_code)
    security_issues = check_security_issues(java_code)
    performance_review = check_performance_issues(java_code)
    # review = ai_code_review(java_code, structure)
    review = ai_code_review_by_category(java_code)
    print("\n=== AI Code Review ===\n")
    print("Security Issues Found:", security_issues)
    print(review)
