#!/usr/bin/env python

import pickle
import itertools

# Load scraped data
with open("markdown-it-data.pickle", "rb") as md_file:
    md_it_data = pickle.load(md_file)
with open("github-data.pickle", "rb") as github_file:
    github_data = pickle.load(github_file)

# Put into vimscript-friendly format, eg:
#
# let s:emoji_code = {
#     \ '+1': 0x1f44d,
#     ...
# }

print("let s:emoji_code = {")

# Use intersection
keys = set(md_it_data.keys()) & set(github_data.keys())

# # Use Github
# keys = github_data.keys()

for i, key in enumerate(sorted(keys)):
    value = github_data[key]
    if i < len(keys) - 1:
        # General case
        print(f"    \ '{key}': {value},")
    else:
        # Last one, omit trailing comma
        print(f"    \ '{key}': {value}")

print("}")
