# 🏛️ GovGuideBot - Maharashtra Government Certificate Assistant

An intelligent AI-powered chatbot that helps citizens of Maharashtra, India navigate government certificate application processes. Built with Google's Gemini AI and enhanced with advanced document validation capabilities.

## ✨ Features

### 🤖 Intelligent Chatbot
- **Multi-language Support**: English, Hindi, and Marathi
- **5 Certificate Types**: Birth, Caste, Domicile, Income, Non-Creamy Layer
- **Step-by-step Guidance**: Detailed application procedures
- **Smart Fallback**: Uses Gemini AI for queries outside the specialized database
- **Auto-Update System**: Monitors government websites for policy changes

### 📋 Advanced Document Validity Checker
- **Multi-format Support**: JPG, PNG, TIFF, PDF
- **Advanced OCR**: Multiple preprocessing techniques for better accuracy
- **ML-based Detection**: Intelligent document type identification
- **Detailed Analysis**: Confidence scores, field detection, and comprehensive reports

### Prerequisites
- Docker installed in your system

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/TousifTamboli/govguidebot.git
cd govguidebot
```

2. **Run docker-compose**
```bash
docker-compose up --build
```

7. **Access the app**
- Local: `http://localhost:5001/`
- The app will also provide a public URL for sharing

</details>

## 📁 Project Structure

```
govguidebot/
├── app.py                          # Basic version
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (not in git)
├── data/                          # Certificate data
│   ├── birth_certificate.json
│   ├── caste_certificate.json
│   ├── domicile_certificate.json
│   ├── income_certificate.json
│   └── non_creamy_certificate.json
└── src/                           # Source code
    ├── chatbot.py                 # Main chatbot logic
    ├── config.py                  # Configuration
    ├── data_loader.py             # Data loading utilities
    ├── vector_store.py            # Vector database
    ├── web_scraper.py             # Government website scraper
    └── update_scheduler.py        # Auto-update scheduler
```

## 🎯 Usage Examples

### Chatbot Queries
```
"How do I apply for income certificate?"
"What documents are needed for caste certificate?"
"आय प्रमाणपत्र कैसे बनवाएं?" (Hindi)
"जात प्रमाणपत्रासाठी कोणती कागदपत्रे लागतात?" (Marathi)
```

### Document Validation
1. Navigate to the "Document Validity Checker" section
2. Upload your document (image or PDF)
3. Choose analysis type:
   - **Quick Check**: Fast validation
   - **Full Report**: Comprehensive analysis
   - **Debug**: Detailed extraction info
4. View results with confidence scores

## 🔧 Configuration

### Model Selection
Edit `src/config.py` to change the AI model:
```python
MODEL_NAME = "models/gemini-2.5-flash"  # Current model
```

Available models:
- `models/gemini-2.5-flash` (Recommended - Fast & Accurate)
- `models/gemini-2.5-pro` (More powerful, slower)
- `models/gemini-2.0-flash` (Good for high volume)

### Rate Limits
Free tier limits (configurable in `src/config.py`):
- 15 requests per minute
- 1500 requests per day

## 🛠️ Technologies Used

- **AI/ML**: Google Gemini AI, LangChain
- **OCR**: Tesseract, OpenCV, PyMuPDF
- **UI**: Gradio
- **Vector DB**: ChromaDB
- **Web Scraping**: BeautifulSoup, Requests
- **Scheduling**: APScheduler

## 📊 Supported Documents

### Certificates
- ✅ Aadhaar Card
- ✅ Birth Certificate
- ✅ Caste Certificate
- ✅ Domicile Certificate
- ✅ Income Certificate
- ✅ Non-Creamy Layer Certificate

## 🔐 Security Features

- **Fraud Detection**: Identifies suspicious documents
- **Authenticity Markers**: Verifies government seals and signatures
- **Security Scoring**: Multi-factor validation
- **Red Flag Detection**: Warns about potential issues

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Tousif Tamboli**
- GitHub: [@TousifTamboli](https://github.com/TousifTamboli)

## 🙏 Acknowledgments

- Google Gemini AI for the powerful language model
- Maharashtra Government for certificate information
- Open source community for amazing tools and libraries

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Your Email]

## 🔄 Updates

The system automatically monitors government websites for updates:
- Every time when run

---

**Note**: This is an AI-powered assistant. For official verification, always contact the relevant government authority.

Made with ❤️ for the people of Maharashtra
