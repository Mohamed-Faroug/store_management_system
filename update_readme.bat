@echo off
echo Updating README.md with fixed license links...
git add README.md
git commit -m "Fix: Updated license links in README.md"
git push origin main
echo Done! License links are now working.
pause
