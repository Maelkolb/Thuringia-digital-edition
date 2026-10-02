#!/usr/bin/env sh
# Publish the built site (./site) to the gh-pages branch, which GitHub Pages serves.
# The branch holds only the current build (one commit, replaced on every publish).
#   python pipeline/site/build.py && sh tools/publish_pages.sh
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
test -f "$ROOT/site/index.html" || { echo "build the site first: python pipeline/site/build.py"; exit 1; }
git -C "$ROOT" worktree add --detach "$TMP" >/dev/null
cd "$TMP"
git checkout --orphan gh-pages-build >/dev/null 2>&1
git rm -rq --cached . >/dev/null 2>&1 || true
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -r "$ROOT/site/." .
touch .nojekyll
git add -A
git commit -qm "Edition build $(date +%Y-%m-%d) from $(git -C "$ROOT" rev-parse --short HEAD)"
git push -qf origin HEAD:gh-pages
cd "$ROOT"
git worktree remove --force "$TMP"
git branch -D gh-pages-build >/dev/null 2>&1 || true
echo "published to gh-pages"
