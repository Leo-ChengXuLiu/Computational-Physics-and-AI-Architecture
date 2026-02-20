import os
import shutil
import subprocess
import requests
import json
from datetime import datetime
from config import *

# ================= setup zone =================
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
INBOX_DIR = os.path.join(REPO_ROOT, "_Inbox")
DEFAULT_FOLDER = "Uncategorized"


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3" 
# ===========================================

def ask_ai_for_folder(filename):
    print(f"asking ai: '{filename}' ...")
    

    prompt = f"""
    You are a helpful assistant for a Physics student at UCL.
    Task: Categorize the following course file into a single, concise folder name (in English).
    
    Filename: "{filename}"
    
    Rules:
    1. Use standard physics categories like: Quantum_Mechanics, Thermodynamics, Electromagnetism, Classical_Mechanics, Math_Methods, Astrophysics, Computing, Labs.
    2. If it's clearly a specific topic (e.g., "triso fuel"), generalize it (e.g., "Nuclear_Physics").
    3. Output ONLY the folder name. Do not output anything else. No punctuation.
    4. If you represent uncertain, output "Uncategorized".
    
    Folder Name:
    """

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
        
        if response.status_code == 200:
            result = response.json().get("response", "").strip()
            folder_name = result.replace(" ", "_").replace(".", "").replace('"', "")
            print(f"💡 AI decied to put file in: 📂 {folder_name}")
            return folder_name
        else:
            print(f"Error : {response.status_code}")
            return DEFAULT_FOLDER
            
    except Exception as e:
        print(f"Erron on connection with local ai: {e}")
        return DEFAULT_FOLDER

def git_push():
    """Git push"""
    try:
        subprocess.run(["git", "add", "."], cwd=REPO_ROOT, check=True)
        
        status = subprocess.run(["git", "status", "-s"], cwd=REPO_ROOT, capture_output=True, text=True)
        if not status.stdout.strip():
            print("No change no upload")
            return

        commit_msg = f"AI Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_ROOT, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_ROOT, check=True)
        print("Success upload")
    except subprocess.CalledProcessError as e:
        print(f"Unsuccess upload")

def organize_files():
    if not os.path.exists(INBOX_DIR):
        os.makedirs(INBOX_DIR)
        return

    files = [f for f in os.listdir(INBOX_DIR) if not f.startswith('.')]
    if not files:
        print("Inbox is empty")
        return

    for filename in files:
        src_path = os.path.join(INBOX_DIR, filename)
        if os.path.isdir(src_path): continue
        folder_name = ask_ai_for_folder(filename)
        
        dest_dir = os.path.join(REPO_ROOT, folder_name)
        os.makedirs(dest_dir, exist_ok=True)
        
        shutil.move(src_path, os.path.join(dest_dir, filename))

if __name__ == "__main__":
    organize_files()
    git_push()
    print("-------------------------")