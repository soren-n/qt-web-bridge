#!/usr/bin/env python3
"""
Simple setup script for git hooks in qt-webview-bridge project.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description="", check=True):
    """Run a command and print the result."""
    print(f"\n{description}")
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        if check:
            raise
        return e


def main():
    """Main setup function."""
    print("Setting up git hooks for qt-webview-bridge")
    print("=" * 50)

    # Check if we're in a git repository
    if not Path(".git").exists():
        print("Not in a git repository!")
        print("Please run this script from the project root.")
        sys.exit(1)

    # Check if pre-commit config exists
    if not Path(".pre-commit-config.yaml").exists():
        print(".pre-commit-config.yaml not found!")
        print("Please ensure the pre-commit configuration file exists.")
        sys.exit(1)

    try:
        # Install pre-commit hooks
        print("Installing pre-commit hooks...")
        run_command(
            [sys.executable, "-m", "pre_commit", "install"],
            "Installing pre-commit git hooks",
        )

        # Test hooks on all files
        print("Testing hooks on all files...")
        result = run_command(
            [sys.executable, "-m", "pre_commit", "run", "--all-files"],
            "Running pre-commit on all files",
            check=False,
        )

        if result.returncode == 0:
            print("All hooks passed!")
        else:
            print("Some hooks failed or made changes.")
            print("This is normal for the first run - hooks may auto-fix issues.")

        print("\n" + "=" * 50)
        print("Git hooks setup complete!")
        print("\nHooks will now run automatically on git commit.")

    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nSetup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
