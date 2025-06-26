import datetime

async def generate_blogs(repo_paths):
    # Simulate blog posts for demo
    blogs = [
        {
            "title": "How I Built My First Portfolio Project",
            "content": "In this post, I share the journey of building my first project, the challenges faced, and the technologies learned.",
            "date": str(datetime.date(2022, 6, 1)),
        },
        {
            "title": "Automating My Portfolio with AI",
            "content": "Discover how I leveraged AI to automate the creation of my developer portfolio, including skill graphs and project timelines.",
            "date": str(datetime.date(2024, 2, 15)),
        },
    ]
    return blogs 