import os
import re
import shutil
import sys
from time import sleep

import requests
from dotenv import load_dotenv
from git import Repo

from code_fade.github.language_mapper import get_extension_from_language

load_dotenv()

HEADERS = {"Authorization": f'token {os.getenv("GITHUB_TOKEN")}'}


def clone_repo(git_url, directory, repo_name):
    try:
        full_path = os.path.join(directory, repo_name)
        print(f"Cloning {git_url} into {full_path}...")
        Repo.clone_from(git_url, full_path)
        print("Repository cloned successfully.")
        return full_path
    except Exception as e:
        print(f"Failed to clone repository: {e}")
        sys.exit(1)


def delete_repo(repo_path):
    try:
        shutil.rmtree(repo_path)
        print(f"Repository at {repo_path} deleted successfully.")
    except Exception as e:
        print(f"Failed to delete repository: {e}")
        sys.exit(1)


def get_primary_extension(owner, repo_name):
    API_URL = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
    response = requests.get(API_URL, headers=HEADERS)
    response_json = response.json()
    if response.status_code == 200 and response_json:
        primary_language = max(response_json, key=response_json.get)
        extension = get_extension_from_language(primary_language)
        return extension
    else:
        print("Failed to fetch repository extension!")
        sys.exit(1)


def extract_owner_repo(github_url):
    pattern = r"https?://github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, github_url)
    if match:
        owner, repo_name = match.groups()
        return owner, repo_name
    else:
        return None, None


def fetch_user_metadata(username):
    """
    Fetches metadata for a given GitHub username using the GitHub API.

    Parameters:
    - username: The GitHub username to fetch metadata for.

    Returns:
    A dictionary containing the user's metadata, or None if the user was not found or an error occurred.
    """
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch user metadata: HTTP {response.status_code}")
        return None


def fetch_author_username(owner, repo_name, commit_sha):
    """
    Fetches the GitHub username of the author of a specific commit.

    Parameters:
    - owner (str): The username or organization name of the repository owner.
    - repo (str): The name of the repository.
    - commit_sha (str): The SHA hash of the commit for which to retrieve the author's username.

    Returns:
    - str: The GitHub username of the commit author if found.
    - None: If the commit does not have an associated GitHub username or if an error occurs during the API request.
    """
    url = "https://api.github.com/repos/{owner}/{repo_name}/commits/{commit_sha}"
    response = requests.get(
        url.format(owner=owner, repo_name=repo_name, commit_sha=commit_sha),
        headers=HEADERS,
    )
    if response.status_code == 200:
        commit_data = response.json()
        if "author" in commit_data and commit_data["author"] is not None:
            return commit_data["author"]
        else:
            return commit_data["commit"]["author"]
    else:
        print(f"Failed to fetch commit data: {response.status_code}")
        return None


def fetch_author_metadata(owner, repo, commit_sha):
    """
    Retrieves selected metadata fields for the author of a specific commit from GitHub.

    This function first fetches the GitHub username of the commit's author using the
    `get_author_username` function. It then retrieves the author's metadata from GitHub
    using the `fetch_user_metadata` function. Finally, it filters this metadata to return
    only the specified fields of interest.

    Parameters:
    - owner (str): The username or organization name of the repository owner.
    - repo (str): The name of the repository.
    - commit_sha (str): The SHA hash of the commit for which to retrieve the author's metadata.

    Returns:
    - dict: A dictionary containing the specified fields of the author's metadata if available.
            The keys in the dictionary are the names of the metadata fields, and the values are
            the corresponding values for those fields from the author's GitHub profile.
    - None: If the username cannot be retrieved, the user's metadata cannot be fetched, or the
            specified commit does not exist.
    """
    required_fields = [
        "login",
        "name",
        "company",
        "location",
        "public_repos",
        "public_gists",
        "followers",
        "following",
        "created_at",
    ]
    user_data = fetch_author_username(owner, repo, commit_sha)
    if "login" in user_data:
        sleep(1)
        metadata = fetch_user_metadata(user_data["login"])
        sleep(1)
        if metadata:
            return {
                field: metadata[field] for field in required_fields if field in metadata
            }
    return None
