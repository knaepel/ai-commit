#!/usr/bin/env python3

import os
import re
import subprocess
import openai
import sys
from typing import Optional

OPENAI_API_KEY = "ENTER_TOKEN_HERE"

openai.api_key = OPENAI_API_KEY

def get_git_diff():
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return result.stdout

def get_ticket_number_from_branch():
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    branch_name = result.stdout.strip()
    match = re.search(r'(feature|bugfix)\/(\d+)', branch_name)
    if match:
        return f"#{match.group(2)}"
    return None

def get_ticket_number_from_argv(argv):
    if len(argv) > 1 and "#" in argv[1]:
        return argv[1]
    return None

def generate_commit_message(diff_output, ticket_number: Optional[str], short_description: Optional[str]):
    if ticket_number:
        title_start = ticket_number
    else:
        title_start = "..."

    prompt = f"Generate a Git commit message for the following changes. The first line is used as the commit title and the second line is used as the body. The first line should be less than 50 characters. The body (second line) is required. Start the title with '{title_start} '. Output format:\n\[title]\n[body] \n\nChanges: \n\n{diff_output}\n\nDeveloper justification: {short_description}\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Generate Git commit messages based on the provided changes. Do not create justifications or reasons for the changes that are not present in the given diff. Be concise and accurate."},
            {"role": "user", "content": prompt}
        ]
    )

    message = response['choices'][0]['message']['content'].strip()
    return message

def commit_changes(commit_message):
    result = subprocess.run(["git", "commit", "-m", commit_message])
    return result.returncode == 0

if __name__ == "__main__":
    ticket_number = get_ticket_number_from_argv(sys.argv)
    if not ticket_number:
        ticket_number = get_ticket_number_from_branch()

    if len(sys.argv) > 1:
        short_description_start_index = 1 if not ticket_number else 2
        short_description = ' '.join(sys.argv[short_description_start_index:])
    else:
        short_description = None

    diff_output = get_git_diff()

    if diff_output:
        commit_message = generate_commit_message(diff_output, ticket_number, short_description)
        if commit_message:
            success = commit_changes(commit_message)
            if success:
                print("Changes have been successfully committed.")
            else:
                print("Error occurred while committing changes.")
    else:
        print("No changes detected in the Git repository.")
