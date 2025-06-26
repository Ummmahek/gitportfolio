from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tools.portfolio_generator import generate_portfolio
from tools.utils import get_username_from_github_url
import os
import httpx
import pdfplumber
import io

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# In-memory store for generated portfolios (for demo; use DB in prod)
PORTFOLIOS = {}

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

async def hf_summarize(text):
    url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    payload = {"inputs": text[:1000]}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HF_HEADERS, json=payload, timeout=60)
        result = response.json()
        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"]
        return "No summary available."

async def hf_generate_blog(prompt):
    url = "https://api-inference.huggingface.co/models/gpt2"
    payload = {"inputs": prompt}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HF_HEADERS, json=payload, timeout=60)
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        return "No blog generated."

async def hf_ner(text):
    url = "https://api-inference.huggingface.co/models/dbmdz/bert-large-cased-finetuned-conll03-english"
    payload = {"inputs": text[:2000]}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HF_HEADERS, json=payload, timeout=60)
        result = response.json()
        return result if isinstance(result, list) else []

# Example skill keywords for demo
SKILL_KEYWORDS = set([
    'python', 'java', 'javascript', 'c++', 'c', 'html', 'css', 'react', 'node', 'sql', 'machine learning', 'deep learning', 'nlp', 'ai', 'data science', 'docker', 'git', 'linux', 'aws', 'azure', 'cloud', 'pytorch', 'tensorflow', 'flask', 'fastapi', 'django', 'typescript', 'php', 'ruby', 'go', 'rust', 'kubernetes', 'devops', 'graphql', 'mongodb', 'postgresql', 'mysql', 'bash', 'shell', 'matlab', 'r', 'scala', 'swift', 'kotlin', 'android', 'ios', 'vue', 'angular', 'bootstrap', 'tailwind', 'firebase', 'hadoop', 'spark', 'tableau', 'powerbi', 'excel', 'jira', 'agile', 'scrum', 'leadership', 'communication', 'teamwork', 'problem solving', 'project management'
])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.jinja", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, github_url: str = Form(...)):
    username = get_username_from_github_url(github_url)
    portfolio_data = await generate_portfolio(github_url)
    PORTFOLIOS[username] = portfolio_data
    return RedirectResponse(url=f"/portfolio/{username}", status_code=303)

@app.get("/portfolio/{username}", response_class=HTMLResponse)
async def portfolio(request: Request, username: str):
    data = PORTFOLIOS.get(username)
    if not data:
        return templates.TemplateResponse("error.jinja", {"request": request, "message": "Portfolio not found."})
    return templates.TemplateResponse("portfolio.jinja", {"request": request, "data": data, "username": username})

@app.get("/timeline/{username}", response_class=HTMLResponse)
async def timeline(request: Request, username: str):
    data = PORTFOLIOS.get(username)
    if not data:
        return templates.TemplateResponse("error.jinja", {"request": request, "message": "Portfolio not found."})
    return templates.TemplateResponse("timeline.jinja", {"request": request, "timeline": data.get("timeline"), "username": username})

@app.get("/skills/{username}", response_class=HTMLResponse)
async def skills(request: Request, username: str):
    data = PORTFOLIOS.get(username)
    if not data:
        return templates.TemplateResponse("error.jinja", {"request": request, "message": "Portfolio not found."})
    return templates.TemplateResponse("skills.jinja", {"request": request, "skills": data.get("skills"), "username": username})

@app.get("/blog/{username}", response_class=HTMLResponse)
async def blog(request: Request, username: str):
    data = PORTFOLIOS.get(username)
    if not data:
        return templates.TemplateResponse("error.jinja", {"request": request, "message": "Portfolio not found."})
    return templates.TemplateResponse("blog.jinja", {"request": request, "blogs": data.get("blogs"), "username": username})

@app.post("/api/analyze_resume")
async def analyze_resume(file: UploadFile):
    content = await file.read()
    text = content.decode(errors='ignore')
    summary = await hf_summarize(text)
    entities = await hf_ner(text)
    found_skills = set()
    for ent in entities:
        word = ent.get('word', '').lower()
        if word in SKILL_KEYWORDS:
            found_skills.add(word)
    for skill in SKILL_KEYWORDS:
        if skill in text.lower():
            found_skills.add(skill)
    return JSONResponse({"summary": summary, "skills": sorted(found_skills)})

@app.post("/api/generate_blog")
async def generate_blog(prompt: str = Form(...)):
    blog = await hf_generate_blog(prompt)
    return JSONResponse({"blog": blog})

@app.get("/api/skills/{username}")
async def api_skills(username: str):
    data = PORTFOLIOS.get(username)
    if not data:
        return JSONResponse({"error": "Portfolio not found."}, status_code=404)
    # Return skills as JSON for frontend graphs
    return JSONResponse(data.get("skills", {})) 