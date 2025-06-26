# 🚀 GitPortfolio

*Turn your GitHub repositories into a dynamic, interactive portfolio website using AI!*

## 🌟 Unique Features
- **Interactive Portfolio Website**: Not just a resume, but a full portfolio site.
- **Project Timelines**: Visualize your project journey and milestones.
- **Skill Progression Graphs**: See how your skills evolved over time.
- **Auto-generated Blog Posts**: AI writes blog posts about your major projects.
- **Live Demo Detection**: If your repo has a deployable app, it's linked and showcased.

## 🛠 Tech Stack
- **Backend**: Python 3.11, FastAPI
- **Frontend**: Jinja2 Templates, Tailwind CSS (CDN)
- **Git Operations**: GitPython
- **Containerization**: Docker, Uvicorn

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Git
- Docker (optional, for containerized deployment)

### Local Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/gitportfolio.git
   cd gitportfolio
   ```
2. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Run the Application:**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8080
   ```
   Access at [http://localhost:8080](http://localhost:8080).

### Docker Deployment
1. **Build the Docker Image:**
   ```bash
   docker build -t gitportfolio .
   ```
2. **Run the Container:**
   ```bash
   docker run -p 8080:8080 gitportfolio
   ```

## 📦 File Structure
- `app.py` — Main FastAPI app
- `tools/` — Portfolio generation, git operations, analysis modules
- `templates/` — Jinja2 HTML templates
- `static/` — Static assets (favicon, manifest, JS)

## 📬 Contact
Created with ❤ by [Your Name]. 