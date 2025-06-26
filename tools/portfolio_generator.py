import asyncio
from .git_operations import clone_and_get_repos
from .gitingest import analyze_repos
from .skill_analysis import analyze_skills
from .timeline_builder import build_timeline
from .blog_generator import generate_blogs
from .utils import get_username_from_github_url

async def generate_portfolio(github_url):
    username = get_username_from_github_url(github_url)
    repos = await clone_and_get_repos(github_url)
    code_analysis = await analyze_repos(repos)
    skills = await analyze_skills(repos)
    timeline = await build_timeline(repos)
    blogs = await generate_blogs(repos)
    # Optionally, add AI-generated video scripts and learning recommendations here
    return {
        "username": username,
        "repos": code_analysis["repos"],
        "summary": code_analysis["summary"],
        "skills": skills,
        "timeline": timeline,
        "blogs": blogs,
        # "video_scripts": ...,
        # "learning_recommendations": ...
    } 