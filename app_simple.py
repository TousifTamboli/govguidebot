# app_simple.py - GovGuideBot without update system
import os
import ssl
import certifi

# Fix SSL certificate issue on Windows
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['CURL_CA_BUNDLE'] = certifi.where()
ssl._create_default_https_context = ssl._create_unverified_context

import gradio as gr
from src.chatbot import GovGuideBot
from src.config import Config

# Initialize bot
print("Initializing GovGuideBot...")
bot = GovGuideBot(data_dir=Config.DATA_DIR)

def chat_interface(message, history, language):
    """Gradio chat interface"""
    
    if not message.strip():
        return history, ""
    
    # Get response
    response = bot.chat(message, language=language)
    
    # Update history
    history.append((message, response['answer']))
    
    return history, ""

def reset_chat():
    """Reset conversation"""
    bot.reset_conversation()
    return [], "Conversation reset!"

# Create Gradio interface
with gr.Blocks(title="GovGuideBot - Maharashtra Government Documents Assistant", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # 🏛️ GovGuideBot
    ### AI Assistant for Maharashtra Government Documents
    
    Get help with:
    - Income Certificate (उत्पन्न प्रमाणपत्र)
    - Caste Certificate (जात प्रमाणपत्र)
    - Domicile Certificate (अधिवास प्रमाणपत्र)
    - Birth Certificate (जन्म प्रमाणपत्र)
    - Non-Creamy Layer Certificate (गैर क्रीमी स्तर प्रमाणपत्र)
    - And more...
    
    **Languages supported:** English, Hindi (हिंदी), Marathi (मराठी)
    """)
    
    with gr.Row():
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(
                height=500,
                label="Chat with GovGuideBot",
                type="messages"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ask me about government documents... (English/Hindi/Marathi)",
                    label="Your Message",
                    scale=4
                )
                language_selector = gr.Dropdown(
                    choices=[
                        ("Auto-detect", "auto"),
                        ("English", "en"),
                        ("Hindi/Marathi", "hi")
                    ],
                    value="auto",
                    label="Language",
                    scale=1
                )
            
            with gr.Row():
                submit_btn = gr.Button("Send 📤", variant="primary")
                clear_btn = gr.Button("Clear Chat 🗑️")
        
        with gr.Column(scale=1):
            gr.Markdown("""
            ### 📚 Quick Links
            - [Aaple Sarkar Portal](https://aaplesarkar.mahaonline.gov.in/)
            - [Maharashtra e-District](https://edistrict.maharashtra.gov.in/)
            
            ### 💡 Example Questions
            
            **English:**
            - "How do I apply for an income certificate in Pune?"
            - "What documents are needed for caste certificate?"
            - "Where is the nearest tehsil office in Mumbai?"
            - "How to get NCL certificate?"
            - "Birth certificate for home birth"
            
            **Hindi:**
            - "मुझे आय प्रमाणपत्र कैसे मिलेगा?"
            - "जाति प्रमाणपत्र के लिए क्या चाहिए?"
            
            **Marathi:**
            - "उत्पन्न दाखला कसा मिळेल?"
            - "जात प्रमाणपत्रासाठी काय लागते?"
            
            ### ⚡ Features
            - ✅ Free AI-powered assistance
            - ✅ Multilingual support
            - ✅ District-specific information
            - ✅ Step-by-step guidance
            - ✅ Office locations & contacts
            - ✅ 5 Certificate types covered
            """)
    
    # Event handlers
    submit_btn.click(
        chat_interface,
        inputs=[msg, chatbot, language_selector],
        outputs=[chatbot, msg]
    )
    
    msg.submit(
        chat_interface,
        inputs=[msg, chatbot, language_selector],
        outputs=[chatbot, msg]
    )
    
    clear_btn.click(
        reset_chat,
        outputs=[chatbot, msg]
    )
    
    gr.Markdown("""
    ---
    **Note:** This is an AI assistant. For official information, please visit government portals or contact offices directly.
    
    **Comprehensive Coverage:** Income, Caste, Domicile, Birth & NCL Certificates
    """)

# Launch app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7864,
        share=True  # Creates public URL
    )