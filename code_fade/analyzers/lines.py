import os
from datetime import datetime, timezone

from pydriller import Repository
from tqdm import tqdm

import code_fade.github.api as cfga
from code_fade.db.authors import fetch_author
from code_fade.db.lines import bulk_push_lines
from code_fade.utils.core import hash_line
from code_fade.utils.format import convert_to_iso


def calculate_code_lifespan(added_at, removed_at=None):
    date_added = datetime.fromisoformat(added_at)
    date_deleted = (
        datetime.fromisoformat(removed_at) if removed_at else datetime.now(timezone.utc)
    )
    lifespan = date_deleted - date_added
    return lifespan.days


def hash_code(code):
    if not code:
        return set()

    hashed_code = []
    for line in code.split("\n"):
        if line:
            hashed_code.append(line)
    return set(hashed_code)


def calculate_line_diffs(old_code, new_code):
    old_hashed_code = hash_code(old_code)
    new_hashed_code = hash_code(new_code)
    added_lines = new_hashed_code - old_hashed_code
    deleted_lines = old_hashed_code - new_hashed_code
    return added_lines, deleted_lines


def generate_line_changes(owner, repo_name, repo_path):
    authors = {}
    files = {}
    changed_lines = []
    total_commits = sum(1 for _ in Repository(repo_path).traverse_commits())
    primary_extension = cfga.get_primary_extension(owner, repo_name)
    with tqdm(total=total_commits, desc="Analyzing Commits") as pbar:
        repository = Repository(repo_path)
        for commit in repository.traverse_commits():
            author_email = commit.author.email
            if author_email not in authors:
                authors[author_email] = fetch_author(repo_name, author_email)["login"]
            author = authors[author_email]
            for mod in commit.modified_files:
                file_path = mod.new_path or mod.old_path
                if file_path:
                    _, file_extension = os.path.splitext(file_path)
                    if file_extension == primary_extension:
                        file_hash = hash_line(file_path)
                        if file_hash not in files:
                            files[file_hash] = {}
                        old_content = mod.source_code_before
                        new_content = mod.source_code
                        added_lines, deleted_lines = calculate_line_diffs(
                            old_content, new_content
                        )
                        for line_hash in added_lines:
                            files[file_hash][line_hash] = {
                                "repo": repo_name,
                                "sha": commit.hash,
                                "line": line_hash,
                                "file": file_path,
                                "added_at": convert_to_iso(commit.committer_date),
                                "added_by": author,
                            }
                        for line_hash in deleted_lines:
                            if line_hash not in files[file_hash]:
                                continue
                            changed_line = files[file_hash].pop(line_hash)
                            removed_at = convert_to_iso(commit.committer_date)
                            lifespan = calculate_code_lifespan(
                                changed_line["added_at"], removed_at
                            )
                            changed_line.update(
                                {
                                    "removed_at": convert_to_iso(commit.committer_date),
                                    "removed_by": author,
                                    "lifespan": lifespan,
                                }
                            )
                            changed_lines.append(changed_line)
            if len(changed_lines) > 100:
                bulk_push_lines(changed_lines)
                changed_lines = []
            pbar.update(1)

        # Push all remaining lines
        if len(changed_lines) > 0:
            bulk_push_lines(changed_lines)
            changed_lines = []
        remaining_lines = []
        for file_hash in files:
            for line_hash in files[file_hash]:
                line = files[file_hash][line_hash]
                line["lifespan"] = calculate_code_lifespan(line["added_at"])
                remaining_lines.append(line)
        if remaining_lines:
            bulk_push_lines(remaining_lines)
