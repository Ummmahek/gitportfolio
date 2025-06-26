import os
import tempfile
import shutil
from git import Repo

async def clone_and_get_repos(github_url):
    temp_dir = tempfile.mkdtemp()
    try:
        repo_path = os.path.join(temp_dir, "repo")
        Repo.clone_from(github_url, repo_path)
        return [repo_path]
    except Exception as e:
        shutil.rmtree(temp_dir)
        raise e 