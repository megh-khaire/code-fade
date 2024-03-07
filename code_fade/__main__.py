from pydriller import Repository
from tqdm import tqdm

from code_fade.github.api import extract_owner_repo, fetch_author_metadata


def generate_data(github_url):
    authors = {}
    code_changes = []
    total_commits = sum(1 for _ in Repository(github_url).traverse_commits())
    with tqdm(total=total_commits, desc="Analyzing Commits") as pbar:
        repository = Repository(github_url)
        for commit in repository.traverse_commits():
            author_email = commit.author.email
            if author_email in authors:
                authors[author_email]["last_commit"] = commit.author_date
            else:
                owner, repo_name = extract_owner_repo(github_url)
                author_metadata = fetch_author_metadata(owner, repo_name, commit.hash)
                author_metadata.update(
                    {
                        "repo": repo_name,
                        "email": author_email,
                        "first_commit": commit.author_date,
                        "last_commit": commit.author_date,
                    }
                )
                authors[author_email] = author_metadata

            for mod in commit.modified_files:
                file_path = mod.new_path or mod.old_path
                if file_path:
                    for added_line in mod.diff_parsed["added"]:
                        change = {
                            "repo": repo_name,
                            "sha": commit.hash,
                            "type": "ADD",
                            "file": file_path,
                            "line": added_line[0],
                            "added_at": commit.committer_date,
                            "added_by": author_email,
                        }
                        code_changes.append(change)

                    for deleted_line in mod.diff_parsed["deleted"]:
                        change = {
                            "repo": repo_name,
                            "sha": commit.hash,
                            "type": "REMOVE",
                            "file": file_path,
                            "line": deleted_line[0],
                            "removed_by": author_email,
                            "removed_at": commit.committer_date,
                        }
                        code_changes.append(change)
            pbar.update(1)
