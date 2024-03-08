import argparse
import traceback

import code_fade.github.api as cfga
from code_fade.analyzers.authors import generate_author_metadata
from code_fade.analyzers.lines import generate_line_changes
from code_fade.db.authors import bulk_push_authors, delete_all_repo_authors
from code_fade.db.lines import delete_all_repo_lines
from code_fade.github.api import delete_repo
from code_fade.db.core import create_indexes


def main(github_url, repo_directory="./data"):
    try:
        create_indexes()
        owner, repo_name = cfga.extract_owner_repo(github_url)
        repo_path = cfga.clone_repo(github_url, repo_directory, repo_name)
        email_username_map, authors = generate_author_metadata(
            owner, repo_name, repo_path
        )
        bulk_push_authors(list(authors.values()))
        generate_line_changes(owner, repo_name, repo_path)
    except Exception as e:
        print("Exception: ", e)
        traceback.print_exc()
        print("Executing cleanup...")
        print("Deleting all authors...")
        delete_all_repo_authors(repo_name)
        print("Deleting all lines...")
        delete_all_repo_lines(repo_name)
    finally:
        delete_repo(repo_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code Fade!")
    parser.add_argument(
        "github_url", type=str, help="GitHub repository URL to clone and process."
    )
    parser.add_argument(
        "--repo_directory",
        type=str,
        default="./data",
        help="Directory to clone the repository into. Default is './data'.",
    )

    args = parser.parse_args()

    main(args.github_url, args.repo_directory)
