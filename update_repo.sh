#!/bin/bash
cd /home/joel/gembot_workspace/ventures/blog_generator

# Pull latest changes just in case
git pull origin main --rebase

# Add all changes
git add .

# Commit with current timestamp
git commit -m "auto-update blog posts: $(date +'%Y-%m-%d %H:%M:%S')"

# Push to GitHub
git push origin main