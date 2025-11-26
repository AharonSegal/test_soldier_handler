# ╔══════════════════════════════════════════════════════╗
# ║   GIT BASH ENVIRONMENT SETUP (WINDOWS)               ║
# ╚══════════════════════════════════════════════════════╝
"""
git init
python -m venv venv
python -m pip install --upgrade pip
source venv/Scripts/activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pip freeze > requirements.txt
git add .  
git commit -m "initial commit"
git push -u origin main


"""
pip install fastapi
pip install pydantic
pip install 'pydantic[email]'
pip install SQLAlchemy
pip install sqlmodel
pip install uvicorn
pip install requests
pip install python-dotenv
"""
"""

# ╔══════════════════════════════════════════════════════╗
# ║   BASIC GIT COMMANDS (REFERENCE)                     ║
# ╚══════════════════════════════════════════════════════╝
"""
git add .                    
git commit -m " "      
git push                     


git init                        # New repo
git clone <url>                 # Clone from remote
git status                      # View changes
git log --oneline               # Condensed history
git remote -v                   # Show remote URL
git add <file>                  # Stage file
git add .                       # Stage all
git push -u origin main         # First push
git pull                        # Fetch + merge
git fetch                       # Fetch only
git branch                      # List branches
git checkout -b "aharon"         # Create + switch
git switch <branch>             # Switch only
"""



"""
============================================================
        🚀 FASTAPI + GIT + ENV QUICK SETUP TEMPLATE
============================================================



============================================================
2️⃣ INSTALL FASTAPI + UVICORN
============================================================

pip install fastapi uvicorn
pip install python-dotenv requests
pip freeze > requirements.txt

============================================================
4️⃣ RUN THE APP
============================================================

# Run with uvicorn
uvicorn main:app --reload

# Then open in browser:
http://127.0.0.1:8000

# Or test the interactive docs:
http://127.0.0.1:8000/docs


============================================================
5️⃣ BASIC GIT WORKFLOW
============================================================

# Configure Git (first time)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
