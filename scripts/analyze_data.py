#!/usr/bin/env python

import pickle
import itertools

# Load scraped data
with open("markdown-it-data.pickle", "rb") as md_file:
    md_it_data = pickle.load(md_file)
with open("github-data.pickle", "rb") as github_file:
    github_data = pickle.load(github_file)
# Parse our vim-emoji data
with open("github_complete.txt", "rb") as our_file:
    # Examples:
    # '+1': 0x1f44d,
    # 'woman_in_steamy_room': [0x1f9d6, 0x200d, 0x2640],
    our_data = {}
    for line in our_file.readlines():
        # Remove single quotes, chop off trailing comma
        line = line.decode("ascii").replace("'", "")[:-1]

        # Get key, value
        key, value = line.split(": ")

        # Assign
        our_data[key] = value


# Compare datasets
md_it_keys = set(md_it_data.keys())
github_keys = set(github_data.keys())
our_keys = set(our_data.keys())

print("Github count: ", len(github_keys))
print("markdown-it count: ", len(md_it_keys))
print("our count: ", len(our_keys))
print()

print("In Github only: ", len(github_keys - (md_it_keys | our_keys)))
print("In markdown-it only: ", len(md_it_keys - (md_it_keys | github_keys)))
print("In ours only: ", len(our_keys - (md_it_keys | github_keys)))
print()


def eval_combinations(**kwargs):
    for a, b in itertools.permutations(sorted(kwargs.keys()), 2):
        print(f"In {a} but not in {b}:", len(kwargs[a] - kwargs[b]))


eval_combinations(
    **{"ours": our_keys, "Github": github_keys, "markdown-it": md_it_keys}
)
print()

