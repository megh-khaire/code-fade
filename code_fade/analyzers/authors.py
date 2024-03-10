from datetime import datetime, timezone

from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta
from pydriller import Repository
from tqdm import tqdm

import code_fade.github.api as cfga
from code_fade.db.authors import fetch_author
from code_fade.utils.format import convert_to_iso


def calculate_author_experience(created_at, first_commit, last_commit):
    repo_experience = relativedelta(
        datetime.fromisoformat(
            last_commit), datetime.fromisoformat(first_commit)
    )
    experience = relativedelta(datetime.now(timezone.utc), parse_date(
        created_at)).years if created_at else -1
    return experience, repo_experience.years


def generate_author_metadata(owner, repo_name, repo_path):
    authors = {}
    email_username_map = {}
    repository = Repository(repo_path)
    total_commits = sum(1 for _ in repository.traverse_commits())
    with tqdm(total=total_commits, desc="Collecting Author Data") as pbar:
        for commit in repository.traverse_commits():
            author_email = commit.author.email
            # Ignore authors that have been already added
            if fetch_author(repo_name, author_email):
                continue
            commit_date = convert_to_iso(commit.author_date)
            if author_email in email_username_map: # Author already exists with the same email:
                username = email_username_map[author_email]
                created_at = authors[username]["created_at"]
                first_commit = authors[username]["first_commit"]
                total_exp, repo_exp = calculate_author_experience(
                    created_at, first_commit, commit_date
                )
                authors[username].update(
                    {
                        "last_commit": commit_date,
                        "repo_experience": repo_exp,
                        "career_experience": total_exp,
                    }
                )
            else:
                author_metadata = cfga.fetch_author_metadata(
                    owner, repo_name, commit.hash
                )
                # Ignore authors that have been deleted
                if not author_metadata:
                    continue
                username = author_metadata["login"]
                # Author already exists with a different email:
                if username in authors:
                    # Ignore authors that have been deleted
                    if "created_at" in authors[username] and "first_commit" in authors[username]:
                        created_at = authors[username]["created_at"]
                        first_commit = authors[username]["first_commit"]
                        total_exp, repo_exp = calculate_author_experience(
                            created_at, first_commit, commit_date
                        )
                        authors[username].update(
                            {
                                "last_commit": commit_date,
                                "repo_experience": repo_exp,
                                "career_experience": total_exp,
                            }
                        )
                        authors[username]["emails"].append(author_email)
                        email_username_map[author_email] = username
                else:
                    author_metadata.update(
                        {
                            "repo": repo_name,
                            "emails": [author_email],
                            "first_commit": commit_date,
                        }
                    )
                    authors[username] = author_metadata
                    email_username_map[author_email] = username
            pbar.update(1)
    return email_username_map, authors
