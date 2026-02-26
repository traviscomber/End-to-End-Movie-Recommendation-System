#!/usr/bin/env python3
import subprocess
import os

os.chdir('/vercel/share/v0-project')

# Add all changes
subprocess.run(['git', 'add', '-A'], check=True)

# Commit
subprocess.run(['git', 'commit', '-m', 'Phase 1-2: Add search API endpoints and search UI with recommendations'], check=True)

# Push
subprocess.run(['git', 'push', 'origin', 'project-development'], check=True)

print("Successfully pushed to GitHub")
