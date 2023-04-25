# Git Commit Message Generator

This Python script automatically generates Git commit messages using OpenAI's GPT-3.5-turbo, based on the changes you've made to your code. The generated messages include a commit title and commit body. The script can also identify a ticket number, making it easy to reference related tasks or issues.

## Requirements

- Python 3.6+
- OpenAI API key

## Dependencies

- `openai` Python library

To install the required dependencies, run the following command:

```
pip install openai
```

## How to use

1. Clone this repository to your local machine:

```
git clone https://github.com/knaepel/ai-commit.git
```

2. Change to the repository directory:

```
cd ai-commit
```

3. Enter your OpenAI API key in the script:

Replace `OPENAI_API_KEY` with your actual API key:

```python
OPENAI_API_KEY = "your_api_key_here"
```

4. Make the script executable:

```
chmod +x ai-commit.py
```

5. Execute the Python script:

```
./ai-commit.py [<ticket_number>] [short_description]
```

The `ticket_number` and `short_description` arguments are optional. The script will attempt to extract the ticket number from the command arguments or from the branch name. If there is no ticket number or short description provided, it will generate a commit message without them. You should replace `<ticket_number>` with the actual task or issue number, formatted like "#123".

## Example

With a ticket number and short description:

```
./ai-commit.py "#123" "Implemented new feature X"
```

Without a ticket number, but with a short description:

```
./ai-commit.py "Refactored the function Y"
```

With neither a ticket number nor a short description:

```
./ai-commit.py
```

The Git commit message generator will analyze the changes you've made, use GPT-3.5-turbo to generate a commit message, and commit your changes to the repository.

## Note

Remember to be within a Git repository while using this script to generate commit messages.
