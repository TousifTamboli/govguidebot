# ⚡ Quick Start Guide

## 🚀 For New System (First Time Setup)

### Windows
```bash
# 1. Clone repository
git clone https://github.com/TousifTamboli/govguidebot.git
cd govguidebot

# 2. Run automated setup
setup.bat

# 3. Run the app
run.bat
```

### Linux/Mac
```bash
# 1. Clone repository
git clone https://github.com/TousifTamboli/govguidebot.git
cd govguidebot

# 2. Make scripts executable
chmod +x setup.sh run.sh

# 3. Run automated setup
./setup.sh

# 4. Run the app
./run.sh
```

---

## 🔄 Running Again (After Setup)

### Windows
```bash
cd govguidebot
run.bat
```

### Linux/Mac
```bash
cd govguidebot
./run.sh
```

---

## 📝 Manual Setup (If Scripts Don't Work)

### Step 1: Clone
```bash
git clone https://github.com/TousifTamboli/govguidebot.git
cd govguidebot
```

### Step 2: Create Virtual Environment
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create .env File
Create a file named `.env` with:
```
GOOGLE_API_KEY=your_api_key_here
```
Get API key from: https://aistudio.google.com/app/apikey

### Step 5: Run
```bash
python app.py
```

### Step 6: Open Browser
Go to: http://localhost:7862

---

## 🎯 Available Versions

```bash
python app.py              # Basic version (recommended)
python app_modern.py       # Modern UI
python app_ultra_modern.py # Full-featured with document checker
```

---

## ❌ Common Issues

### "python: command not found"
Use `python3` instead of `python`

### "Module not found"
Make sure virtual environment is activated:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

Then: `pip install -r requirements.txt`

### "API Key error"
Check your `.env` file has the correct API key

---

## 📚 Full Documentation

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

For features and usage, see [README.md](README.md)
