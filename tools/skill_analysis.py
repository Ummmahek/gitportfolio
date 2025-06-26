import os
from collections import Counter

async def analyze_skills(repo_paths):
    lang_counter = Counter()
    for repo_path in repo_paths:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.py'):
                    lang_counter['Python'] += 1
                if file.endswith('.js'):
                    lang_counter['JavaScript'] += 1
                if file.endswith('.ts'):
                    lang_counter['TypeScript'] += 1
                if file.endswith('.java'):
                    lang_counter['Java'] += 1
                if file.endswith('.go'):
                    lang_counter['Go'] += 1
                if file.endswith('.rb'):
                    lang_counter['Ruby'] += 1
                if file.endswith('.php'):
                    lang_counter['PHP'] += 1
                if file.endswith('.cpp') or file.endswith('.cc'):
                    lang_counter['C++'] += 1
                if file.endswith('.c'):
                    lang_counter['C'] += 1
                if file.endswith('.rs'):
                    lang_counter['Rust'] += 1
                if file.endswith('.html'):
                    lang_counter['HTML'] += 1
                if file.endswith('.css'):
                    lang_counter['CSS'] += 1
    # Simulate skill progression for demo
    skill_progression = [
        {"year": 2022, "skills": ["Python", "HTML"]},
        {"year": 2023, "skills": ["Python", "JavaScript", "CSS"]},
        {"year": 2024, "skills": list(lang_counter.keys())},
    ]
    return {"skills": dict(lang_counter), "progression": skill_progression} 