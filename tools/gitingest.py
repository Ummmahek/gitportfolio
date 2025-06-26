import os
import glob
import json

def detect_tech_stack(repo_path):
    stack = set()
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                stack.add('Python')
            if file.endswith('.js'):
                stack.add('JavaScript')
            if file.endswith('.ts'):
                stack.add('TypeScript')
            if file.endswith('.java'):
                stack.add('Java')
            if file.endswith('.go'):
                stack.add('Go')
            if file.endswith('.rb'):
                stack.add('Ruby')
            if file.endswith('.php'):
                stack.add('PHP')
            if file.endswith('.cpp') or file.endswith('.cc'):
                stack.add('C++')
            if file.endswith('.c'):
                stack.add('C')
            if file.endswith('.rs'):
                stack.add('Rust')
            if file.endswith('.html'):
                stack.add('HTML')
            if file.endswith('.css'):
                stack.add('CSS')
    return list(stack)

def parse_readme(repo_path):
    readme_path = None
    for name in ["README.md", "readme.md", "README.txt", "README"]:
        candidate = os.path.join(repo_path, name)
        if os.path.exists(candidate):
            readme_path = candidate
            break
    if readme_path:
        with open(readme_path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""

def detect_live_demo(readme_text):
    # Simple heuristic: look for 'demo', 'live', or 'app' links
    import re
    urls = re.findall(r'https?://\S+', readme_text)
    for url in urls:
        if any(word in url.lower() for word in ["demo", "live", "app"]):
            return url
    return None

async def analyze_repos(repo_paths):
    repos_info = []
    for repo_path in repo_paths:
        tech_stack = detect_tech_stack(repo_path)
        readme = parse_readme(repo_path)
        live_demo = detect_live_demo(readme)
        repos_info.append({
            "name": os.path.basename(repo_path),
            "tech_stack": tech_stack,
            "readme": readme[:1000],  # Truncate for display
            "live_demo": live_demo,
        })
    summary = f"Analyzed {len(repo_paths)} repositories. Tech stacks: {', '.join(set(sum([r['tech_stack'] for r in repos_info], [])))}."
    return {"repos": repos_info, "summary": summary} 