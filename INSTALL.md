# 🚀 Installation Guide

## Quick Install (Recommended)

### Windows
1. **Download the project**
   ```bash
   git clone https://github.com/TousifTamboli/govguidebot.git
   cd govguidebot
   ```

2. **Run the setup script**
   ```bash
   setup.bat
   ```
   This will automatically:
   - Create virtual environment
   - Install all dependencies
   - Set up your API key

3. **Run the app**
   ```bash
   venv\Scripts\activate
   python app.py
   ```

## Manual Installation

### Step 1: Prerequisites
- **Python 3.8 - 3.12** (Python 3.13+ not yet supported)
- **Git** (optional, for cloning)

Check your Python version:
```bash
python --version
```

### Step 2: Download Project
```bash
git clone https://github.com/TousifTamboli/govguidebot.git
cd govguidebot
```

Or download ZIP from GitHub and extract it.

### Step 3: Create Virtual Environment
```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 5: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If you get errors**, install packages individually:
```bash
# Core packages (required)
pip install gradio google-generativeai python-dotenv certifi

# LangChain (required)
pip install langchain langchain-google-genai langchain-core

# Vector database (required)
pip install chromadb pandas numpy

# Web scraping (required)
pip install requests beautifulsoup4 lxml schedule

# Document checker (optional - skip if errors)
pip install pytesseract opencv-python PyMuPDF pdf2image Pillow
```

### Step 6: Set Up API Key

1. **Get Google AI API Key**
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy your key

2. **Create .env file**
   Create a file named `.env` in the project root:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

### Step 7: Run the Application
```bash
python app.py
```

Open your browser to: `http://localhost:7862`

## Troubleshooting

### Python Version Issues
**Error:** `audioop-lts requires Python 3.13+`
**Solution:** Use Python 3.8-3.12. The requirements.txt has been updated to remove this dependency.

### Import Errors
**Error:** `ModuleNotFoundError: No module named 'xxx'`
**Solution:** 
```bash
pip install xxx
```

### Tesseract OCR Not Found
**Error:** `TesseractNotFoundError`
**Solution:** 
- **Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Linux:** `sudo apt-get install tesseract-ocr`
- **Mac:** `brew install tesseract`

**Note:** Document validation will work without Tesseract, but with reduced accuracy.

### API Key Errors
**Error:** `404 model not found` or `429 quota exceeded`
**Solution:**
1. Check your API key is correct in `.env`
2. Verify the model name in `src/config.py`
3. Wait 1-2 minutes if you hit rate limits

### Port Already in Use
**Error:** `Address already in use`
**Solution:** 
- Stop other running instances
- Or change port in the app file (search for `7862`)

## Running Different Versions

### Basic Version (Recommended for beginners)
```bash
python app.py
```
- Simple interface
- Core chatbot features
- Lightweight

### Modern Version
```bash
python app_modern.py
```
- Enhanced UI
- Better styling
- All core features

### Ultra-Modern Version (Full-featured)
```bash
python app_ultra_modern.py
```
- Advanced UI
- Document validation
- All features

## Verifying Installation

Test if everything works:
```bash
python -c "import gradio; import google.generativeai; print('✅ Installation successful!')"
```

## Getting Help

If you encounter issues:
1. Check this guide first
2. Look at error messages carefully
3. Open an issue on GitHub: https://github.com/TousifTamboli/govguidebot/issues
4. Include:
   - Your Python version
   - Error message
   - What you were trying to do

## Next Steps

After installation:
1. ✅ Run the app: `python app.py`
2. ✅ Open browser: `http://localhost:7862`
3. ✅ Try asking: "How do I apply for income certificate?"
4. ✅ Test document validation (ultra-modern version)

Enjoy using GovGuideBot! 🎉
