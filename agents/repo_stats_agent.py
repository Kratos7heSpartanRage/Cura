from typing import Dict, Any


class RepoStatsAgent:
    def generate_stats(self, repo_facts: Dict[str, Any]) -> Dict[str, Any]:
        python_files = repo_facts.get("python_files", [])
        entry_points = repo_facts.get("entry_points", [])
        directories = repo_facts.get("directory_structure", [])

        return {
            "total_python_files": len(python_files),
            "total_directories": len(directories),
            "entry_points": entry_points,
            "has_entry_point": len(entry_points) > 0,
        }
