import re

def get_username_from_github_url(url):
    # Extract username from https://github.com/username/repo or https://github.com/username
    match = re.match(r"https?://github.com/([^/]+)", url)
    if match:
        return match.group(1)
    return "user" 