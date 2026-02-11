# tools/file_scanner.py

import os

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    "cura-env",
    "node_modules",
    ".idea",
    ".vscode"
}

IGNORE_FILES = {
    ".DS_Store"
}

def scan_directory(root_path):
    project_map = []

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if file in IGNORE_FILES:
                continue

            full_path = os.path.join(root, file)

            project_map.append({
                "file_name": file,
                "path": full_path,
                "extension": os.path.splitext(file)[1]
            })

    return project_map
