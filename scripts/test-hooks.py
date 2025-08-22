#!/usr/bin/env python3
"""
Test script to verify git hooks are working correctly.

This script creates a temporary test file with intentional issues
to verify that the pre-commit hooks catch and fix them.
"""

import subprocess
import sys
from pathlib import Path


def create_test_file():
    """Create a test Python file with intentional issues."""
    test_content = '''# Test file with intentional formatting issues

import json
import sys
import os

def bad_function(  x,y  ):
    """Function with bad formatting."""
    if x==y:
        return {"result":True}
    else:
        return {"result": False}

class   TestClass:
    def __init__(self):
        pass

    def method_with_issues(self):
        unused_var = "this will be flagged"
        print("trailing whitespace here:   ")
        return None

if __name__ == "__main__":
    result = bad_function(1,2)
    print( result)
'''

    test_file = Path("temp_test_file.py")
    test_file.write_text(test_content)
    return test_file


def run_pre_commit():
    """Run pre-commit on the test file."""
    print("🧪 Running pre-commit hooks...")

    try:
        # Stage the test file
        subprocess.run(["git", "add", "temp_test_file.py"], check=True)

        # Run pre-commit
        result = subprocess.run(
            [sys.executable, "-m", "pre_commit", "run", "--files", "temp_test_file.py"],
            capture_output=True,
            text=True,
        )

        print("Pre-commit output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)

        return result.returncode == 0

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running pre-commit: {e}")
        return False
    except FileNotFoundError:
        print("❌ pre-commit not found. Please install it first.")
        return False


def cleanup():
    """Clean up test files."""
    test_file = Path("temp_test_file.py")
    if test_file.exists():
        test_file.unlink()
        # Unstage if it was staged
        subprocess.run(
            ["git", "reset", "temp_test_file.py"], capture_output=True, check=False
        )


def main():
    """Main test function."""
    print("🧪 Testing git hooks setup")
    print("=" * 40)

    if not Path(".git").exists():
        print("❌ Not in a git repository!")
        sys.exit(1)

    if not Path(".pre-commit-config.yaml").exists():
        print("❌ Pre-commit config not found!")
        sys.exit(1)

    try:
        # Create test file with issues
        print("📝 Creating test file with formatting issues...")
        test_file = create_test_file()
        print(f"Created: {test_file}")

        # Run pre-commit
        success = run_pre_commit()

        # Show results
        if test_file.exists():
            print("\n📄 File after pre-commit:")
            print(test_file.read_text())

        if success:
            print("✅ All hooks passed!")
        else:
            print("⚠️  Hooks found issues (this is expected for the test)")
            print("Check the output above to see what was fixed/flagged.")

    finally:
        cleanup()
        print("\n🧹 Cleaned up test files")


if __name__ == "__main__":
    main()
