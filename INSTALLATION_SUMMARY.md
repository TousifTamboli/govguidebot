# 📦 Installation Summary - GovGuideBot

## 🎯 Complete Setup Process (From Clone to Run)

```
┌─────────────────────────────────────────────────────────────┐
│                    NEW SYSTEM SETUP                          │
└─────────────────────────────────────────────────────────────┘

Step 1: Clone Repository
├─ git clone https://github.com/TousifTamboli/govguidebot.git
└─ cd govguidebot

Step 2: Setup Environment
├─ Windows: Run setup.bat
└─ Linux/Mac: Run ./setup.sh

Step 3: Configure API Key
├─ Get key from: https://aistudio.google.com/app/apikey
└─ Add to .env file: GOOGLE_API_KEY=your_key_here

Step 4: Run Application
├─ Windows: run.bat
└─ Linux/Mac: ./run.sh

Step 5: Access App
└─ Open browser: http://localhost:7862

✅ DONE! Total time: ~5-10 minutes
```

---

## 🔄 Detailed Step-by-Step

### 1️⃣ Clone Repository (1 minute)

**Open Terminal/Command Prompt and run:**

```bash
git clone https://github.com/TousifTamboli/govguidebot.git
cd govguidebot
```

**What this does:**
- Downloads all project files from GitHub
- Creates a `govguidebot` folder
- Navigates into the project directory

---

### 2️⃣ Automated Setup (3-5 minutes)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**What this does:**
- ✅ Checks Python installation
- ✅ Creates virtual environment (`venv` folder)
- ✅ Activates virtual environment
- ✅ Upgrades pip
- ✅ Installs all dependencies from `requirements.txt`
- ✅ Checks for `.env` file

**Packages installed (50+):**
- gradio (UI framework)
- google-generativeai (Gemini AI)
- langchain (AI framework)
- chromadb (Vector database)
- pytesseract (OCR)
- opencv-python (Image processing)
- PyMuPDF (PDF processing)
- beautifulsoup4 (Web scraping)
- And many more...

---

### 3️⃣ Get API Key (2 minutes)

**Steps:**
1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

**Create `.env` file:**

**Option A - Automatic (during setup.bat/setup.sh):**
- Script will prompt for API key
- Enter key when asked

**Option B - Manual:**

Create a file named `.env` in project root:

**Windows (Command Prompt):**
```bash
echo GOOGLE_API_KEY=your_api_key > .env
```

**Windows (PowerShell):**
```powershell
"GOOGLE_API_KEY=your_api_key" | Out-File -FilePath .env -Encoding utf8
```

**Linux/Mac:**
```bash
echo "GOOGLE_API_KEY=your_api_key" > .env
```

**Or use any text editor:**
```
GOOGLE_API_KEY=your_actual_api_key_here
```

---

### 4️⃣ Run Application (10 seconds)

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Or manually:**

**Windows:**
```bash
venv\Scripts\activate
python app.py
```

**Linux/Mac:**
```bash
source venv/bin/activate
python app.py
```

**What happens:**
- Virtual environment activates
- App starts loading
- You'll see:
  ```
  Initializing GovGuideBot...
  ✓ Loaded: birth_certificate.json
  ✓ Loaded: caste_certificate.json
  ...
  * Running on local URL:  http://0.0.0.0:7862
  * Running on public URL: https://xxxxx.gradio.live
  ```

---

### 5️⃣ Access Application

**Open your browser and go to:**
- **Local:** http://localhost:7862
- **Public:** Use the gradio.live URL shown in terminal

**You should see:**
- GovGuideBot interface
- Chat input box
- Language selector
- Quick reply buttons

---

## 🎮 Using the Application

### Test the Chatbot

**Try these questions:**
```
"How do I apply for income certificate?"
"What documents are needed for caste certificate?"
"आय प्रमाणपत्र कैसे बनवाएं?"
```

### Test Document Checker (Ultra-Modern version)

1. Run: `python app_ultra_modern.py`
2. Scroll to "Document Validity Checker"
3. Upload Aadhaar card or certificate
4. Click "Quick Check"

---

## 📂 What Gets Created

After setup, your folder structure:

```
govguidebot/
├── venv/                    # Virtual environment (created by setup)
│   ├── Scripts/            # Windows
│   ├── bin/                # Linux/Mac
│   └── Lib/                # Python packages
├── .env                     # Your API key (create this)
├── app.py                   # Main application
├── requirements.txt         # Dependencies list
├── setup.bat               # Windows setup script
├── setup.sh                # Linux/Mac setup script
├── run.bat                 # Windows run script
├── run.sh                  # Linux/Mac run script
├── SETUP_GUIDE.md          # Detailed guide
├── QUICK_START.md          # Quick reference
└── ... (other project files)
```

---

## 🔄 Running Again Later

After initial setup, you only need:

**Windows:**
```bash
cd govguidebot
run.bat
```

**Linux/Mac:**
```bash
cd govguidebot
./run.sh
```

**That's it!** Takes ~10 seconds to start.

---

## ❌ Troubleshooting

### Problem: "python: command not found"
**Solution:** 
- Windows: Use `python` 
- Linux/Mac: Use `python3`

### Problem: "Module not found" errors
**Solution:**
```bash
# Activate virtual environment first
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Then install
pip install -r requirements.txt
```

### Problem: "API Key error"
**Solution:**
1. Check `.env` file exists
2. Verify API key is correct
3. No spaces around `=` in `.env`
4. API key starts with `AIza`

### Problem: "Port already in use"
**Solution:**
- App will automatically try different ports
- Or stop other apps using port 7862

### Problem: Setup script doesn't run
**Solution:**
- Windows: Right-click `setup.bat` → "Run as administrator"
- Linux/Mac: `chmod +x setup.sh` then `./setup.sh`

---

## 📊 System Requirements

**Minimum:**
- Python 3.8+
- 2 GB RAM
- 500 MB disk space
- Internet connection

**Recommended:**
- Python 3.10+
- 4 GB RAM
- 1 GB disk space
- Stable internet

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Clone repository | 30 seconds |
| Run setup script | 3-5 minutes |
| Get API key | 2 minutes |
| First run | 20 seconds |
| **Total first time** | **~8 minutes** |
| Subsequent runs | 10 seconds |

---

## 🎯 Success Checklist

- [ ] Python installed (check: `python --version`)
- [ ] Git installed (check: `git --version`)
- [ ] Repository cloned
- [ ] Virtual environment created (`venv` folder exists)
- [ ] Dependencies installed (no errors during setup)
- [ ] `.env` file created with API key
- [ ] App runs without errors
- [ ] Can access http://localhost:7862
- [ ] Chatbot responds to questions

---

## 📚 Additional Resources

- **Detailed Setup:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Quick Reference:** [QUICK_START.md](QUICK_START.md)
- **Full Documentation:** [README.md](README.md)
- **GitHub Repository:** https://github.com/TousifTamboli/govguidebot

---

## 🆘 Still Need Help?

1. Check error messages carefully
2. Review [SETUP_GUIDE.md](SETUP_GUIDE.md) troubleshooting section
3. Open an issue on GitHub
4. Make sure all prerequisites are installed

---

**🎉 Congratulations! You're ready to use GovGuideBot!**
