@echo off
echo Setting up Git repository...
git init
git add .
git commit -m "initial commit - classroom attendance system"
echo.
echo Done! Now push to GitHub:
echo   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
echo   git push -u origin main
pause
