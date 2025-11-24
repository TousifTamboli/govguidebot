# 🚀 Complete Setup Guide - GovGuideBot

This guide will help you set up and run GovGuideBot on a new system from scratch.

## 📋 Prerequisites

Before starting, ensure you have:
- **Python 3.8 or higher** installed
- **Git** installed
- **Google AI API Key** ([Get it here](https://aistudio.google.com/app/apikey))
- **Internet connection**

---

## 🔧 Step-by-Step Setup

### Step 1: Install Python (if not installed)

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run installer and **check "Add Python to PATH"**
3. Verify installation:
   ```bash
   python --version
   ```

**Linux/Mac:**
```bash
# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Mac (using Homebrew)
brew install python3
```

---

### Step 2: Install Git (if not installed)

**Windows:**
- Download from https://git-scm.com/download/win
- Run installer with default settings

**Linux:**
```bash
sudo apt install git
```

**Mac:**
```bash
brew install git
```

Verify installation:
```bash
git --version
```

---

### Step 3: Clone the Repository

Open terminal/command prompt and run:

```bash
# Clone the repository
git clone https://github.com/TousifTamboli/govguidebot.git

# Navigate to project directory
cd govguidebot
```

---

### Step 4: Create Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

### Step 5: Install Dependencies

With virtual environment activated:

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install:
- Gradio (UI framework)
- Google Generative AI (Gemini)
- LangChain (AI framework)
- ChromaDB (Vector database)
- Tesseract OCR (Document processing)
- OpenCV (Image processing)
- And many more...

**Installation time:** 2-5 minutes depending on internet speed

---

### Step 6: Get Google AI API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key (starts with `AIza...`)

---

### Step 7: Create Environment File

Create a file named `.env` in the project root directory:

**Windows (using Command Prompt):**
```bash
echo GOOGLE_API_KEY=your_api_key_here > .env
```

**Windows (using PowerShell):**
```powershell
"GOOGLE_API_KEY=your_api_key_here" | Out-File -FilePath .env -Encoding utf8
```

**Linux/Mac:**
```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

**Or manually create `.env` file with this content:**
```env
GOOGLE_API_KEY=AIzaSyAAeKZy5WQGf8NfzkIiYkNNVaxcDRa0COU
```

⚠️ **Replace with your actual API key!**

---

### Step 8: Run the Application

Choose which version to run:

#### Option A: Basic Version (Recommended for first run)
```bash
python app.py
```

#### Option B: Modern Version
```bash
python app_modern.py
```

#### Option C: Ultra-Modern Version (with Document Checker)
```bash
python app_ultra_modern.py
```

---

### Step 9: Access the Application

After running, you'll see output like:
```
* Running on local URL:  http://0.0.0.0:7862
* Running on public URL: https://xxxxx.gradio.live
```

**Access the app:**
- **Local:** Open browser and go to `http://localhost:7862`
- **Public:** Use the gradio.live URL to share with others

---

## 🎯 Quick Test

Once the app is running:

1. **Test the Chatbot:**
   - Type: "How do I apply for income certificate?"
   - You should get a detailed response

2. **Test Document Checker (Ultra-Modern version only):**
   - Scroll down to "Document Validity Checker"
   - Upload an Aadhaar card or certificate image
   - Click "Quick Check"

---

## 🛑 Stopping the Application

Press `Ctrl + C` in the terminal to stop the app.

---

## 🔄 Running Again Later

After initial setup, you only need:

**Windows:**
```bash
cd govguidebot
venv\Scripts\activate
python app.py
```

**Linux/Mac:**
```bash
cd govguidebot
source venv/bin/activate
python app.py
```

---

## ❌ Troubleshooting

### Issue 1: "python: command not found"
**Solution:** Use `python3` instead of `python`

### Issue 2: "pip: command not found"
**Solution:** Use `python -m pip` instead of `pip`

### Issue 3: "Module not found" errors
**Solution:** Make sure virtual environment is activated and run:
```bash
pip install -r requirements.txt
```

### Issue 4: "API Key error" or "404 model not found"
**Solution:** 
1. Check your `.env` file has the correct API key
2. Verify the model name in `src/config.py` is `models/gemini-2.5-flash`

### Issue 5: Port already in use
**Solution:** The app will try different ports automatically, or you can change the port in the app file.

### Issue 6: SSL Certificate errors (Windows)
**Solution:** Already handled in the code with certifi package.

---

## 📦 Project Structure

After cloning, you'll have:
```
govguidebot/
├── app.py                    # Basic version - START HERE
├── app_modern.py             # Modern UI version
├── app_ultra_modern.py       # Full-featured version
├── requirements.txt          # Dependencies
├── .env                      # Your API key (create this)
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
├── SETUP_GUIDE.md           # This file
├── data/                    # Certificate data
│   ├── birth_certificate.json
│   ├── caste_certificate.json
│   ├── domicile_certificate.json
│   ├── income_certificate.json
│   └── non_creamy_certificate.json
└── src/                     # Source code
    ├── chatbot.py
    ├── config.py
    ├── data_loader.py
    ├── vector_store.py
    ├── web_scraper.py
    └── update_scheduler.py
```

---

## 🎓 What Each File Does

- **app.py**: Main application with chatbot interface
- **document_validity_checker.py**: Document validation with OCR
- **src/chatbot.py**: Core chatbot logic and AI integration
- **src/config.py**: Configuration (API key, model settings)
- **data/*.json**: Certificate information database
- **requirements.txt**: List of all Python packages needed

---

## 💡 Tips

1. **First Time Setup:** Takes 5-10 minutes
2. **Subsequent Runs:** Takes 10-20 seconds
3. **Keep Virtual Environment Active:** While working on the project
4. **Update Dependencies:** Run `pip install -r requirements.txt` if you pull updates
5. **API Quota:** Free tier has limits (15 requests/min, 1500/day)

---

## 🆘 Need Help?

- Check the main README.md for detailed documentation
- Open an issue on GitHub: https://github.com/TousifTamboli/govguidebot/issues
- Review error messages carefully - they usually indicate what's wrong

---

## ✅ Success Checklist

- [ ] Python installed and working
- [ ] Git installed and working
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] `.env` file created with API key
- [ ] App runs without errors
- [ ] Can access app in browser
- [ ] Chatbot responds to questions

---

**Congratulations! 🎉 You're ready to use GovGuideBot!**

For detailed features and usage, see the main [README.md](README.md)
