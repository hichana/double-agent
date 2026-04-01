#!/bin/bash
# Call this at the end of every code session to merge the current worktree branch to main and push.
# Branch deletion and worktree pruning are handled automatically by the
# 'double-agent-worktree-cleanup' scheduled task (runs every 2 hours).
set -e
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" == "main" ]]; then
  echo "Already on main, just pushing"
  git push origin main
  exit 0
fi
echo "Merging $BRANCH to main..."
git checkout main
git merge --no-ff "$BRANCH" -m "Merge branch '$BRANCH'"
git push origin main
echo "Done. Main pushed. Scheduled cleanup will prune branch and worktree."
