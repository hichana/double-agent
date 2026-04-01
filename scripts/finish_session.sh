#!/bin/bash
# Call this at the end of every code session to merge the current worktree branch to main and clean up
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
git branch -d "$BRANCH"
git worktree prune
echo "Done. Main pushed, branch deleted, worktrees pruned."
