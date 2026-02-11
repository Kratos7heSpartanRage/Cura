import os
from typing import Dict, List


class RepoFactsExtractor:
    def __init__(self, root_path: str):
        self.root_path = root_path

    def extract(self) -> Dict:
        facts = {
            "has_requirements": False,
            "has_license": False,
            "has_readme": False,
            "entry_points": [],
            "python_files": [],
            "directory_structure": [],
        }

        for root, dirs, files in os.walk(self.root_path):
            relative_root = os.path.relpath(root, self.root_path)
            facts["directory_structure"].append(relative_root)

            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, self.root_path)

                if file == "requirements.txt":
                    facts["has_requirements"] = True

                if file.lower().startswith("license"):
                    facts["has_license"] = True

                if file.lower() == "readme.md":
                    facts["has_readme"] = True

                if file.endswith(".py"):
                    facts["python_files"].append(relative_path)

                    if self._is_entry_point(full_path):
                        facts["entry_points"].append(relative_path)

        return facts

    def _is_entry_point(self, file_path: str) -> bool:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return '__name__ == "__main__"' in content
        except Exception:
            return False
