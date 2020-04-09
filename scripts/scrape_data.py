#!/usr/bin/env python

import requests
import pickle

# Sanity check for datasets
def sanity_check(data):
    assert data["+1"] == "0x1f44d"
    assert data["-1"] == "0x1f44e"


# Get emojis from markdown-it
# This maps directly from the emoji plaintext name to a unicode character
url = "https://raw.githubusercontent.com/markdown-it/markdown-it-emoji/master/lib/data/full.json"
md_it_data = requests.get(url).json()

for key, value in md_it_data.items():
    # Convert unicode values to hex representation
    unicode_blocks = [hex(ord(c)) for c in value]

    if len(unicode_blocks) == 1:
        new_value = unicode_blocks[0]
    else:
        new_value = f"[{', '.join(unicode_blocks)}]"
    md_it_data[key] = new_value

sanity_check(md_it_data)
pickle.dump(md_it_data, open("markdown-it-data.pickle", "wb"))
print("markdown-it emoji count: ", len(md_it_data))


# Get emojis from Github API
# This maps from the emoji plaintext name to a Github URL, eg:
# > "nut_and_bolt": "https://github.githubassets.com/images/icons/emoji/unicode/1f529.png?v8",
# > "zimbabwe": "https://github.githubassets.com/images/icons/emoji/unicode/1f1ff-1f1fc.png?v8",
# > "octocat": "https://github.githubassets.com/images/icons/emoji/octocat.png?v8",
url = "https://api.github.com/emojis"
github_data = requests.get(url).json()

for key, value in list(github_data.items()):
    # Toss out non-unicode emojis (like octocat)
    if "unicode" not in value:
        github_data.pop(key)
        continue

    # Parse URL
    unicode_blocks = value.split("unicode/")[1].split(".png")[0].split("-")
    unicode_blocks = ["0x" + b for b in unicode_blocks]

    # Parse blocks
    if len(unicode_blocks) == 1:
        new_value = unicode_blocks[0]
    else:
        new_value = f"[{', '.join(unicode_blocks)}]"
    github_data[key] = new_value

sanity_check(github_data)
pickle.dump(github_data, open("github-data.pickle", "wb"))
print("Github emoji count: ", len(github_data))
