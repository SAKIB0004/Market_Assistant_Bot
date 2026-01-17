import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s :  - %(levelname)s : ] : %(message)s : ')


list_of_files = [
    "app/__init__.py",
    "app/main.py",
    "app/router.py",
    "app/prompts.py",
    "app/llm.py",
    "app/news.py",
    "app/safety.py",

    "web/index.html",
    ".env",
    "requirements.txt",

]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for file: {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Created empty file: {filepath}")
    else:
        logging.info(f"File already exists and is not empty: {filepath}")

logging.info("File and directory setup complete.")
# This script creates a predefined set of directories and files for a project structure.
