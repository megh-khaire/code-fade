from pydriller import Repository
from datetime import datetime, timezone
from tqdm import tqdm
import matplotlib.pyplot as plt

# Define the repository to analyze
repository_path = 'https://github.com/ishepard/pydriller'  # Example repository

# Initialize dictionaries
author_experience = {}
code_lifespan = {}
author_code_lifespan = {}

# Get the total number of commits for the progress bar
total_commits = sum(1 for _ in Repository(repository_path).traverse_commits())

with tqdm(total=total_commits, desc="Analyzing Commits") as pbar:
    repo = Repository(repository_path)
    for commit in repo.traverse_commits():
        author_name = commit.author.name
        if author_name not in author_experience:
            author_experience[author_name] = {'first_commit': commit.author_date, 'last_commit': commit.author_date}
        else:
            author_experience[author_name]['last_commit'] = commit.author_date

        for mod in commit.modified_files:
            file_path = mod.new_path or mod.old_path
            if file_path:
                for added_line in mod.diff_parsed['added']:
                    line_key = (file_path, added_line[0])
                    code_lifespan[line_key] = {'added': commit.committer_date, 'author': author_name, 'removed': None}

                for deleted_line in mod.diff_parsed['deleted']:
                    line_key = (file_path, deleted_line[0])
                    if line_key in code_lifespan:
                        code_lifespan[line_key]['removed'] = commit.committer_date

        pbar.update(1)

# Update author_experience with experience in days
for author, dates in author_experience.items():
    experience_days = (dates['last_commit'] - dates['first_commit']).days
    author_experience[author] = experience_days

# Aggregate code lifespan by author
for line, info in code_lifespan.items():
    author = info['author']
    if info['removed']:
        lifespan_days = (info['removed'] - info['added']).days
    else:
        now_aware = datetime.now(timezone.utc)
        lifespan_days = (now_aware - info['added']).days
    if author in author_code_lifespan:
        author_code_lifespan[author].append(lifespan_days)
    else:
        author_code_lifespan[author] = [lifespan_days]

# Calculate average code lifespan for each author
for author in author_code_lifespan:
    author_code_lifespan[author] = sum(author_code_lifespan[author]) / len(author_code_lifespan[author])

# Prepare data for plotting
experiences = []
lifespans = []

for author in author_experience:
    if author in author_code_lifespan:
        experiences.append(author_experience[author])
        lifespans.append(author_code_lifespan[author])

# Ensure that experiences and lifespans lists have the same length
assert len(experiences) == len(lifespans), "The experiences and lifespans lists should have the same length."

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(experiences, lifespans, alpha=0.5)
plt.title('Author Experience vs. Code Lifespan')
plt.xlabel('Experience (days)')
plt.ylabel('Average Code Lifespan (days)')
plt.grid(True)
plt.show()
