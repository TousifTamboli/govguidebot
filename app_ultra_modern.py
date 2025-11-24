# app_ultra_modern.py - Ultra Modern Chatbot UI Design
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

# Import the enhanced document checker
from document_validity_checker import (
    enhanced_check_document_validity, 
    create_document_report,
    get_validation_statistics,
    batch_check_documents,
    debug_document_analysis
)

# Initialize bot
print("Initializing GovGuideBot...")
bot = GovGuideBot(data_dir=Config.DATA_DIR)

# Initialize update scheduler
print("Starting update scheduler...")
try:
    from src.update_scheduler import update_scheduler
    update_scheduler.start_scheduler()
    print("✓ Update scheduler started successfully")
except Exception as e:
    print(f"⚠️ Update scheduler failed to start: {e}")
    print("Continuing without automatic updates...")

def chat_interface(message, history, language):
    """Gradio chat interface"""
    
    if not message.strip():
        return history, ""
    
    # Get response
    response = bot.chat(message, language=language)
    
    # Update history with new message format
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response['answer']})
    
    return history, ""

def reset_chat():
    """Reset conversation"""
    bot.reset_conversation()
    return [], "Conversation reset!"

def quick_reply_income(history):
    """Quick reply for income certificate"""
    message = "How do I apply for an income certificate in Maharashtra?"
    response = bot.chat(message, language="en")
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response['answer']})
    return history

def quick_reply_caste(history):
    """Quick reply for caste certificate"""
    message = "What documents are needed for caste certificate?"
    response = bot.chat(message, language="en")
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response['answer']})
    return history

def quick_reply_domicile(history):
    """Quick reply for domicile certificate"""
    message = "How to prove 15 years residence for domicile certificate?"
    response = bot.chat(message, language="en")
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response['answer']})
    return history

# Ultra Modern CSS Design
ultra_modern_css = """
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

/* Root Variables */
:root {
    --primary-purple: #8B5CF6;
    --primary-purple-light: #A78BFA;
    --primary-purple-dark: #7C3AED;
    --background-light: #F8FAFC;
    --background-white: #FFFFFF;
    --text-dark: #1E293B;
    --text-gray: #64748B;
    --text-light: #94A3B8;
    --border-light: #E2E8F0;
    --border-gray: #CBD5E1;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
}

/* Global Styles */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

body, .gradio-container {
    background: linear-gradient(135deg, #E0E7FF 0%, #F3E8FF 50%, #FDF2F8 100%) !important;
    min-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Main Container */
.main-chat-container {
    max-width: 900px !important;
    margin: 2rem auto !important;
    background: var(--background-white) !important;
    border-radius: var(--radius-xl) !important;
    box-shadow: var(--shadow-lg) !important;
    overflow: hidden !important;
    border: 1px solid var(--border-light) !important;
}

/* Header Section */
.chat-header {
    background: linear-gradient(135deg, var(--primary-purple) 0%, var(--primary-purple-dark) 100%) !important;
    color: white !important;
    padding: 1.5rem 2rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
}

.bot-info {
    display: flex !important;
    align-items: center !important;
    gap: 1rem !important;
}

.bot-avatar {
    width: 48px !important;
    height: 48px !important;
    background: rgba(255, 255, 255, 0.2) !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.5rem !important;
}

.bot-details h3 {
    margin: 0 !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
}

.bot-status {
    font-size: 0.875rem !important;
    opacity: 0.9 !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

.status-dot {
    width: 8px !important;
    height: 8px !important;
    background: #10B981 !important;
    border-radius: 50% !important;
    animation: pulse 2s infinite !important;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.header-actions {
    display: flex !important;
    gap: 0.75rem !important;
}

.header-btn {
    width: 36px !important;
    height: 36px !important;
    background: rgba(255, 255, 255, 0.2) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    color: white !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
}

.header-btn:hover {
    background: rgba(255, 255, 255, 0.3) !important;
    transform: scale(1.05) !important;
}

/* Chat Messages Area */
.chat-messages {
    height: 500px !important;
    max-height: 500px !important;
    overflow-y: auto !important;
    padding: 1.5rem !important;
    background: var(--background-light) !important;
}

.gradio-chatbot {
    height: 500px !important;
    max-height: 500px !important;
    border: none !important;
    background: transparent !important;
}

/* Message Bubbles */
.message-bubble {
    max-width: 75% !important;
    margin: 0.75rem 0 !important;
    padding: 1rem 1.25rem !important;
    border-radius: var(--radius-lg) !important;
    word-wrap: break-word !important;
    line-height: 1.5 !important;
}

.user-message {
    background: var(--primary-purple) !important;
    color: white !important;
    margin-left: auto !important;
    border-bottom-right-radius: var(--radius-sm) !important;
}

.bot-message {
    background: var(--background-white) !important;
    color: var(--text-dark) !important;
    border: 1px solid var(--border-light) !important;
    margin-right: auto !important;
    border-bottom-left-radius: var(--radius-sm) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* Quick Reply Buttons */
.quick-replies {
    padding: 1rem 1.5rem 0 1.5rem !important;
    background: var(--background-light) !important;
}

.quick-reply-btn {
    background: var(--background-white) !important;
    border: 1px solid var(--border-gray) !important;
    border-radius: var(--radius-xl) !important;
    padding: 0.5rem 1rem !important;
    margin: 0.25rem !important;
    color: var(--text-gray) !important;
    font-size: 0.875rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    display: inline-block !important;
}

.quick-reply-btn:hover {
    background: var(--primary-purple-light) !important;
    color: white !important;
    border-color: var(--primary-purple-light) !important;
    transform: translateY(-1px) !important;
}

/* Input Section */
.input-section {
    background: var(--background-white) !important;
    padding: 1.5rem !important;
    border-top: 1px solid var(--border-light) !important;
}

.input-wrapper {
    display: flex !important;
    align-items: flex-end !important;
    gap: 1rem !important;
    background: white !important;
    border: 1px solid var(--border-gray) !important;
    border-radius: var(--radius-lg) !important;
    padding: 0.75rem !important;
    transition: all 0.2s ease !important;
}

.input-wrapper:focus-within {
    border-color: var(--primary-purple) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
    background: white !important;
}

/* Ensure input section has white background */
.input-section {
    background: var(--background-white) !important;
    padding: 1.5rem !important;
    border-top: 1px solid var(--border-light) !important;
}

/* Force white background for all input elements */
.input-section * {
    color-scheme: light !important;
}

/* Text Input - White background with black text */
.message-input textarea,
.message-input input,
.gradio-textbox textarea,
.gradio-textbox input {
    background: white !important;
    border: 1px solid var(--border-gray) !important;
    border-radius: var(--radius-sm) !important;
    outline: none !important;
    resize: none !important;
    font-size: 0.95rem !important;
    color: #1a1a1a !important;
    flex: 1 !important;
    min-height: 40px !important;
    max-height: 100px !important;
    padding: 0.75rem 1rem !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.2s ease !important;
}

.message-input textarea:focus,
.message-input input:focus,
.gradio-textbox textarea:focus,
.gradio-textbox input:focus {
    border-color: var(--primary-purple) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
    background: white !important;
    color: #1a1a1a !important;
}

.message-input textarea::placeholder,
.message-input input::placeholder,
.gradio-textbox textarea::placeholder,
.gradio-textbox input::placeholder {
    color: #9ca3af !important;
    font-style: normal !important;
    opacity: 1 !important;
}

/* Ensure text visibility */
.gradio-textbox {
    background: white !important;
}

.gradio-textbox .wrap {
    background: white !important;
    border: 1px solid var(--border-gray) !important;
    border-radius: var(--radius-sm) !important;
}

/* Force text color in all states */
.gradio-textbox textarea,
.gradio-textbox input,
.gradio-textbox .wrap textarea,
.gradio-textbox .wrap input {
    color: #1a1a1a !important;
    background: white !important;
}

/* Override any dark mode styles */
.gradio-container .gradio-textbox textarea,
.gradio-container .gradio-textbox input {
    color: #1a1a1a !important;
    background: white !important;
}

/* Additional text visibility fixes */
textarea, input[type="text"] {
    color: #1a1a1a !important;
    background: white !important;
}

/* Ensure all form elements are light themed */
.gradio-container {
    color-scheme: light !important;
}

.gradio-container * {
    color-scheme: light !important;
}

/* Fix any inherited dark styles */
.gradio-textbox textarea:not(:focus),
.gradio-textbox input:not(:focus) {
    color: #1a1a1a !important;
    background: white !important;
    border-color: var(--border-gray) !important;
}

/* Document Validity Checker Specific Styles */
#validity-checker {
    margin-top: 2rem !important;
}

#validity-checker .gradio-markdown {
    background: white !important;
    color: #1a1a1a !important;
    padding: 1.5rem !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-light) !important;
    box-shadow: var(--shadow-sm) !important;
}

#validity-checker .gradio-markdown h1,
#validity-checker .gradio-markdown h2,
#validity-checker .gradio-markdown h3,
#validity-checker .gradio-markdown h4,
#validity-checker .gradio-markdown h5,
#validity-checker .gradio-markdown h6 {
    color: #1a1a1a !important;
    margin-top: 0 !important;
}

#validity-checker .gradio-markdown p,
#validity-checker .gradio-markdown li,
#validity-checker .gradio-markdown span,
#validity-checker .gradio-markdown div {
    color: #374151 !important;
}

#validity-checker .gradio-markdown strong {
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

#validity-checker .gradio-markdown em {
    color: #4B5563 !important;
}

/* Validity Results Styling */
.validity-results {
    background: white !important;
    color: #1a1a1a !important;
    padding: 1.5rem !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-light) !important;
    box-shadow: var(--shadow-sm) !important;
    min-height: 200px !important;
}

.validity-results h1,
.validity-results h2,
.validity-results h3,
.validity-results h4 {
    color: #1a1a1a !important;
    margin-bottom: 0.75rem !important;
}

.validity-results p,
.validity-results li,
.validity-results span {
    color: #374151 !important;
    line-height: 1.6 !important;
}

.validity-results strong {
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

.validity-results ul,
.validity-results ol {
    padding-left: 1.5rem !important;
}

.validity-results li {
    margin-bottom: 0.5rem !important;
}

/* File Upload Styling */
#validity-checker .gradio-file {
    background: white !important;
    border: 2px dashed var(--border-gray) !important;
    border-radius: var(--radius-md) !important;
    padding: 2rem !important;
    text-align: center !important;
    transition: all 0.2s ease !important;
}

#validity-checker .gradio-file:hover {
    border-color: var(--primary-purple) !important;
    background: #F8FAFC !important;
}

#validity-checker .gradio-file .file-preview {
    color: #374151 !important;
}

/* Button Styling for Document Checker */
#validity-checker .btn-primary {
    background: var(--primary-purple) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

#validity-checker .btn-primary:hover {
    background: var(--primary-purple-dark) !important;
    transform: translateY(-1px) !important;
}

#validity-checker .btn-secondary {
    background: white !important;
    color: var(--primary-purple) !important;
    border: 1px solid var(--primary-purple) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

#validity-checker .btn-secondary:hover {
    background: var(--primary-purple) !important;
    color: white !important;
}

/* Tab Styling */
#validity-checker .gradio-tabs {
    background: white !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-light) !important;
}

#validity-checker .gradio-tabs .tab-nav {
    background: var(--background-light) !important;
    border-bottom: 1px solid var(--border-light) !important;
}

#validity-checker .gradio-tabs .tab-nav button {
    color: var(--text-gray) !important;
    background: transparent !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
}

#validity-checker .gradio-tabs .tab-nav button.selected {
    color: var(--primary-purple) !important;
    background: white !important;
    border-bottom: 2px solid var(--primary-purple) !important;
}

#validity-checker .gradio-tabs .tabitem {
    background: white !important;
    padding: 1.5rem !important;
}

/* Force all text in validity checker to be dark */
#validity-checker * {
    color: #1a1a1a !important;
}

#validity-checker .gradio-markdown * {
    color: inherit !important;
}

#validity-checker .validity-results * {
    color: inherit !important;
}

/* Language Selector */
.language-select {
    min-width: 120px !important;
}

.language-select select,
.gradio-dropdown select {
    background: var(--background-white) !important;
    border: 1px solid var(--border-gray) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.5rem !important;
    font-size: 0.875rem !important;
    color: var(--text-gray) !important;
}

/* Send Button */
.send-btn {
    background: var(--primary-purple) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    width: 40px !important;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: white !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

.send-btn:hover {
    background: var(--primary-purple-dark) !important;
    transform: scale(1.05) !important;
}

/* Action Buttons */
.action-buttons {
    display: flex !important;
    gap: 0.75rem !important;
    margin-top: 1rem !important;
}

.action-btn {
    flex: 1 !important;
    background: var(--background-light) !important;
    border: 1px solid var(--border-gray) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.75rem 1rem !important;
    color: var(--text-gray) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

.action-btn:hover {
    background: var(--primary-purple) !important;
    color: white !important;
    border-color: var(--primary-purple) !important;
}

/* Scrollbar Styling */
.chat-messages::-webkit-scrollbar {
    width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
    background: var(--background-light);
}

.chat-messages::-webkit-scrollbar-thumb {
    background: var(--border-gray);
    border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
    background: var(--text-light);
}

/* Responsive Design */
@media (max-width: 768px) {
    .main-chat-container {
        margin: 1rem !important;
        border-radius: var(--radius-lg) !important;
    }
    
    .chat-header {
        padding: 1rem 1.5rem !important;
    }
    
    .bot-info h3 {
        font-size: 1.1rem !important;
    }
    
    .chat-messages {
        height: 400px !important;
        max-height: 400px !important;
        padding: 1rem !important;
    }
    
    .input-section {
        padding: 1rem !important;
    }
}

/* Loading Animation */
.loading-dots {
    display: inline-flex;
    gap: 4px;
}

.loading-dots span {
    width: 6px;
    height: 6px;
    background: var(--text-light);
    border-radius: 50%;
    animation: loading 1.4s ease-in-out infinite both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes loading {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}
"""

# Create Ultra Modern Gradio Interface
with gr.Blocks(
    title="🏛️ GovGuideBot - Maharashtra Government Assistant",
    css=ultra_modern_css,
    theme=gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
    )
) as demo:
    
    # Main Container
    with gr.Column(elem_classes="main-chat-container"):
        
        # Header Section
        gr.HTML("""
        <div class="chat-header">
            <div class="bot-info">
                <div class="bot-avatar">🏛️</div>
                <div class="bot-details">
                    <h3>GovGuideBot</h3>
                    <div class="bot-status">
                        <span class="status-dot"></span>
                        We're online • Auto-updated
                    </div>
                </div>
            </div>
            <div class="header-actions">
                <button class="header-btn" title="Refresh Chat">🔄</button>
                <button class="header-btn" title="Minimize">✕</button>
            </div>
        </div>
        """)
        
        # Chat Messages Area
        with gr.Column(elem_classes="chat-messages"):
            chatbot = gr.Chatbot(
                height=500,
                label="",
                show_label=False,
                container=False,
                type="messages",
                avatar_images=("👤", "🏛️"),
                bubble_full_width=False,
                elem_classes="gradio-chatbot"
            )
        
        # Quick Reply Buttons
        with gr.Row(elem_classes="quick-replies"):
            gr.HTML("""
            <div style="margin-bottom: 1rem;">
                <p style="color: var(--text-gray); font-size: 0.875rem; margin-bottom: 0.75rem; font-weight: 500;">Quick replies:</p>
            </div>
            """)
        
        with gr.Row():
            income_btn = gr.Button(
                "💰 Income Certificate", 
                elem_classes="quick-reply-btn",
                size="sm"
            )
            caste_btn = gr.Button(
                "🏷️ Caste Certificate", 
                elem_classes="quick-reply-btn",
                size="sm"
            )
            domicile_btn = gr.Button(
                "🏠 Domicile Certificate", 
                elem_classes="quick-reply-btn",
                size="sm"
            )
        
        with gr.Row():
            birth_btn = gr.Button(
                "👶 Birth Certificate", 
                elem_classes="quick-reply-btn",
                size="sm"
            )
            ncl_btn = gr.Button(
                "📜 NCL Certificate", 
                elem_classes="quick-reply-btn",
                size="sm"
            )
            help_btn = gr.Button(
                "❓ General Help", 
                elem_classes="quick-reply-btn",
                size="sm"
            )
        
        # Input Section
        with gr.Column(elem_classes="input-section"):
            gr.HTML("""
            <div class="input-wrapper">
            """)
            
            with gr.Row():
                with gr.Column(scale=5, elem_classes="message-input"):
                    msg = gr.Textbox(
                        placeholder="Enter message...",
                        label="",
                        show_label=False,
                        container=False,
                        lines=1,
                        max_lines=4
                    )
                
                with gr.Column(scale=1, elem_classes="language-select"):
                    language_selector = gr.Dropdown(
                        choices=[
                            ("🌐 Auto", "auto"),
                            ("🇬🇧 EN", "en"),
                            ("🇮🇳 हिं/मरा", "hi")
                        ],
                        value="auto",
                        label="",
                        show_label=False,
                        container=False
                    )
                
                with gr.Column(scale=0, min_width=50):
                    send_btn = gr.Button(
                        "✈️",
                        elem_classes="send-btn",
                        size="sm"
                    )
            
            gr.HTML("""
            </div>
            """)
            
            # Action Buttons
            with gr.Row(elem_classes="action-buttons"):
                clear_btn = gr.Button(
                    "🗑️ Clear Chat",
                    elem_classes="action-btn"
                )
                help_center_btn = gr.Button(
                    "📚 Help Center",
                    elem_classes="action-btn"
                )
                feedback_btn = gr.Button(
                    "💬 Feedback",
                    elem_classes="action-btn"
                )
    
    # Event Handlers
    send_btn.click(
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
    
    # Quick Reply Handlers
    income_btn.click(
        quick_reply_income,
        inputs=[chatbot],
        outputs=[chatbot]
    )
    
    caste_btn.click(
        quick_reply_caste,
        inputs=[chatbot],
        outputs=[chatbot]
    )
    
    domicile_btn.click(
        quick_reply_domicile,
        inputs=[chatbot],
        outputs=[chatbot]
    )

    # Document Validity Check Section (Integrated Feature)
    with gr.Column(elem_classes="main-chat-container", elem_id="validity-checker"):
        gr.HTML("""
        <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); color: white; padding: 1.5rem 2rem; text-align: center; margin-top: 2rem;">
            <h2 style="margin: 0; font-size: 1.5rem; font-weight: 600;">📋 Document Validity Checker</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">Upload your government document to verify its authenticity</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                gr.HTML("""
                <div style="padding: 1.5rem; text-align: center;">
                    <h4 style="color: #374151; margin-bottom: 1rem;">📤 Upload Document</h4>
                </div>
                """)
                
                with gr.Tabs():
                    with gr.Tab("Single Document"):
                        document_upload = gr.File(
                            label="Select Document to Validate (Images: JPG, PNG, TIFF | PDFs: PDF)",
                            file_types=["image", ".pdf"],
                            type="filepath"
                        )
                        
                        with gr.Row():
                            check_validity_btn = gr.Button(
                                "🔍 Quick Check",
                                variant="primary",
                                elem_classes="btn-primary",
                                size="sm"
                            )
                            
                            generate_report_btn = gr.Button(
                                "📄 Full Report",
                                variant="secondary",
                                elem_classes="btn-secondary",
                                size="sm"
                            )
                    
                    with gr.Tab("Batch Processing"):
                        batch_upload = gr.File(
                            label="Select Multiple Documents (Images & PDFs)",
                            file_types=["image", ".pdf"],
                            file_count="multiple",
                            type="filepath"
                        )
                        
                        batch_check_btn = gr.Button(
                            "🔍 Check All Documents",
                            variant="primary",
                            elem_classes="btn-primary",
                            size="lg"
                        )
                    
                    with gr.Tab("Analytics"):
                        stats_btn = gr.Button(
                            "📊 View Statistics",
                            variant="secondary",
                            elem_classes="btn-secondary",
                            size="lg"
                        )
                    
                    with gr.Tab("Debug"):
                        debug_btn = gr.Button(
                            "🔍 Debug Analysis",
                            variant="secondary",
                            elem_classes="btn-secondary",
                            size="lg"
                        )
            
            with gr.Column(scale=3):
                gr.HTML("""
                <div style="padding: 1.5rem;">
                    <h4 style="color: #374151; margin-bottom: 1rem;">📊 Analysis Results</h4>
                </div>
                """)
                
                validity_output = gr.Markdown(
                    """**📋 Document Analysis Results**

Upload a document and select an analysis option to see results.

**Available Analysis Options:**
- **🔍 Quick Check:** Fast validation of document authenticity
- **📄 Full Report:** Comprehensive analysis with detailed breakdown
- **📊 Batch Processing:** Check multiple documents at once
- **📈 Analytics:** View validation statistics and trends

**Supported Documents:**
- Aadhaar Card
- Caste Certificate  
- Income Certificate
- Birth Certificate
- Domicile Certificate
- Non-Creamy Layer Certificate""",
                    elem_classes="validity-results"
                )
        
        # Document validity event handlers
        check_validity_btn.click(
            enhanced_check_document_validity,
            inputs=[document_upload],
            outputs=[validity_output]
        )

        generate_report_btn.click(
            create_document_report,
            inputs=[document_upload],
            outputs=[validity_output]
        )

        batch_check_btn.click(
            batch_check_documents,
            inputs=[batch_upload],
            outputs=[validity_output]
        )

        stats_btn.click(
            get_validation_statistics,
            inputs=[],
            outputs=[validity_output]
        )

        debug_btn.click(
            debug_document_analysis,
            inputs=[document_upload],
            outputs=[validity_output]
        )
        
        gr.HTML("""
        <div style="padding: 1rem 1.5rem; background: #F9FAFB; border-top: 1px solid #E5E7EB; text-align: center;">
            <p style="margin: 0; color: #6B7280; font-size: 0.875rem;">
                <strong>Supported Documents:</strong> Aadhaar Card, Caste Certificate, Income Certificate, Birth Certificate, Domicile Certificate, Non-Creamy Layer Certificate
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #6B7280; font-size: 0.8rem;">
                <strong>File Formats:</strong> JPG, PNG, TIFF, PDF • <strong>Enhanced Features:</strong> Advanced OCR • ML-based Detection • Security Validation • Fraud Detection • Data Extraction • Batch Processing
            </p>
        </div>
        """)

# Event handlers are now inside the Blocks context above

# Launch app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7868,
        share=True,
        show_error=True
    )