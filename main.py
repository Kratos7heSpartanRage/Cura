# main.py

import argparse
from core.orchestrator import CuraOrchestrator


def main():
    parser = argparse.ArgumentParser(description="Cura - Code Curator AI Agent")
    parser.add_argument("--path", required=True, help="Path to project folder")
    args = parser.parse_args()

    orchestrator = CuraOrchestrator()
    final_readme = orchestrator.run(args.path)

    print("\n✅ Analysis Complete\n")
    print("README_GENERATED.md has been created successfully.")


if __name__ == "__main__":
    main()
