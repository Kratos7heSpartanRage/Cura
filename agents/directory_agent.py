# agents/directory_agent.py

from tools.file_scanner import scan_directory

class DirectoryAgent:
    def analyze(self, path: str):
        files = scan_directory(path)

        return {
            "total_files": len(files),
            "files": files
        }
