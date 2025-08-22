#!/usr/bin/env python3
"""Setup git commit message template for conventional commits."""

import subprocess
import sys
from pathlib import Path


def main():
    """Set up git commit message template."""
    # Get the repository root
    repo_root = Path(__file__).parent.parent
    template_path = repo_root / ".gitmessage"

    if not template_path.exists():
        print(f"❌ Commit template not found at {template_path}")
        sys.exit(1)

    try:
        # Set the commit template
        subprocess.run(
            ["git", "config", "commit.template", str(template_path)],
            check=True,
            cwd=repo_root,
        )
        print(f"✅ Git commit template set to {template_path}")
        print("\n📝 Usage:")
        print("- Run 'git commit' (without -m) to use the template")
        print("- Follow conventional commit format: type(scope): description")
        print("- Use 'feat:' for new features, 'fix:' for bug fixes")
        print("- Add 'BREAKING CHANGE:' in footer for major releases")

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to set git commit template: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
