#!/usr/bin/env python3
"""
Setup script for git hooks in qt-webview-bridge project.

This script installs and configures pre-commit hooks for:
- Ruff (linting and formatting)
- MyPy (type checking) 
- Basic file checks (trailing whitespace, etc.)
- Optional pytest (manual trigger)

Usage:
    python setup-hooks.py
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description="", check=True):
    """Run a command and print the result."""
    print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        if check:
            raise
        return e


def check_python_version():
    """Check Python version compatibility."""
    version = sys.version_info
    if version < (3, 11):
        print(f"❌ Python {version.major}.{version.minor} is not supported.")
        print("This project requires Python 3.11 or higher.")
        sys.exit(1)
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")


def install_pre_commit():
    """Install pre-commit if not already installed."""
    try:
        result = run_command([sys.executable, "-c", "import pre_commit"], 
                           "Checking if pre-commit is installed", check=False)
        if result.returncode == 0:
            print("✅ pre-commit is already installed")
            return
    except:
        pass
    
    print("📦 Installing pre-commit...")
    run_command([sys.executable, "-m", "pip", "install", "pre-commit>=3.0.0"],
                "Installing pre-commit framework")


def setup_hooks():
    """Set up the pre-commit hooks."""
    print("🎣 Installing pre-commit hooks...")
    run_command([sys.executable, "-m", "pre_commit", "install"],
                "Installing pre-commit git hooks")
    
    print("🎣 Installing pre-commit hooks for push (optional)...")
    run_command([sys.executable, "-m", "pre_commit", "install", "--hook-type", "pre-push"],
                "Installing pre-push hooks", check=False)


def test_hooks():
    """Test the hooks on all files."""
    print("🧪 Testing hooks on all files...")
    result = run_command([sys.executable, "-m", "pre_commit", "run", "--all-files"],
                        "Running pre-commit on all files", check=False)
    
    if result.returncode == 0:
        print("✅ All hooks passed!")
    else:
        print("⚠️  Some hooks failed or made changes.")
        print("This is normal for the first run - hooks may auto-fix issues.")
        print("Run 'git add .' and commit again if files were modified.")


def main():
    """Main setup function."""
    print("🚀 Setting up git hooks for qt-webview-bridge")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not Path(".git").exists():
        print("❌ Not in a git repository!")
        print("Please run this script from the project root.")
        sys.exit(1)
    
    # Check if pre-commit config exists
    if not Path(".pre-commit-config.yaml").exists():
        print("❌ .pre-commit-config.yaml not found!")
        print("Please ensure the pre-commit configuration file exists.")
        sys.exit(1)
    
    try:
        check_python_version()
        install_pre_commit()
        setup_hooks()
        test_hooks()
        
        print("\n" + "=" * 50)
        print("🎉 Git hooks setup complete!")
        print("\nHooks will now run automatically on git commit.")
        print("\nUseful commands:")
        print("  pre-commit run --all-files    # Run hooks manually")
        print("  pre-commit run ruff           # Run only ruff")
        print("  pre-commit run mypy           # Run only mypy")
        print("  pre-commit run pytest --hook-stage manual  # Run tests")
        print("  pre-commit autoupdate         # Update hook versions")
        print("  pre-commit uninstall          # Remove hooks")
        
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()