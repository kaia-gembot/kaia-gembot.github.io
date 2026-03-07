#!/bin/bash
cd /home/joel/gembot_workspace/ventures/blog_generator

# Add all changes
git add .

# Commit with current timestamp
git commit -m "auto-update blog posts: $(date +'%Y-%m-%d %H:%M:%S')"

# Pull latest changes and rebase
git pull origin main --rebase

# Push to GitHub
git push origin main
