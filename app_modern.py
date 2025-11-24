# app_modern.py - Modern UI GovGuideBot with shadcn-inspired design
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

# Custom CSS for modern shadcn-inspired design
custom_css = """
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Root variables for consistent theming */
:root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222.2 84% 4.9%;
    --muted: 210 40% 96%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96%;
    --accent-foreground: 222.2 84% 4.9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.75rem;
}

/* Global styles */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Main container */
.gradio-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 2rem;
}

/* Main content card */
.main-content {
    background: hsl(var(--card));
    border: 1px solid hsl(var(--border));
    border-radius: var(--radius);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    backdrop-filter: blur(10px);
}

/* Header styling */
.header-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: var(--radius) var(--radius) 0 0;
    text-align: center;
}

.header-section h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-section h3 {
    font-size: 1.25rem;
    font-weight: 400;
    opacity: 0.9;
    margin-bottom: 1rem;
}

/* Chat container - Fixed overflow and proper sizing */
.chat-container {
    background: hsl(var(--background)) !important;
    border-radius: var(--radius) !important;
    border: 1px solid hsl(var(--border)) !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    height: 500px !important;
    max-height: 500px !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding: 1rem !important;
}

/* Chatbot wrapper - Ensure proper containment */
.gradio-chatbot {
    height: 500px !important;
    max-height: 500px !important;
    overflow: hidden !important;
}

/* Individual chat messages - Prevent overflow */
.gradio-chatbot .message-wrap {
    max-width: 100% !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}

.gradio-chatbot .message {
    max-width: 85% !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    white-space: pre-wrap !important;
    padding: 0.75rem 1rem !important;
    margin: 0.5rem 0 !important;
    border-radius: var(--radius) !important;
    line-height: 1.5 !important;
}

/* User messages */
.gradio-chatbot .user {
    background: hsl(var(--primary)) !important;
    color: hsl(var(--primary-foreground)) !important;
    margin-left: auto !important;
    margin-right: 0 !important;
}

/* Bot messages */
.gradio-chatbot .bot {
    background: hsl(var(--muted)) !important;
    color: hsl(var(--muted-foreground)) !important;
    margin-left: 0 !important;
    margin-right: auto !important;
}

/* Modern Chat Input Container */
.input-container {
    background: #F8F8F8 !important;
    border: 1px solid #DDDDDD !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    margin: 1rem 0 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    transition: all 0.2s ease-in-out !important;
}

.input-container:hover {
    border-color: #CCCCCC !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
}

/* Modern Chat Input Field */
.gradio-textbox textarea,
.gradio-textbox input {
    background: white !important;
    border: 1px solid #DDDDDD !important;
    border-radius: 10px !important;
    color: #333333 !important;
    font-size: 0.95rem !important;
    padding: 0.875rem 3rem 0.875rem 1rem !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
    resize: none !important;
    min-height: 44px !important;
    max-height: 120px !important;
    line-height: 1.4 !important;
}

/* Placeholder styling */
.gradio-textbox textarea::placeholder,
.gradio-textbox input::placeholder {
    color: #AAAAAA !important;
    font-style: italic !important;
    opacity: 1 !important;
}

/* Focus state */
.gradio-textbox textarea:focus,
.gradio-textbox input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    outline: none !important;
    background: white !important;
}

/* Chat input wrapper with send icon */
.chat-input-wrapper {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

/* Send icon styling */
.send-icon {
    position: absolute !important;
    right: 12px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    width: 20px !important;
    height: 20px !important;
    color: #667eea !important;
    cursor: pointer !important;
    transition: all 0.2s ease-in-out !important;
    z-index: 10 !important;
}

.send-icon:hover {
    color: #5a67d8 !important;
    transform: translateY(-50%) scale(1.1) !important;
}

/* Dropdown styling - Clean white */
.gradio-dropdown select,
.gradio-dropdown .wrap {
    background: white !important;
    border: 1px solid hsl(var(--border)) !important;
    border-radius: calc(var(--radius) - 2px) !important;
    color: hsl(var(--foreground)) !important;
}

/* Modern Chat Buttons */
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.875rem 1.75rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 3px 12px rgba(102, 126, 234, 0.3) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

.btn-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
}

.btn-secondary {
    background: white !important;
    color: #667eea !important;
    border: 2px solid #667eea !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease-in-out !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

.btn-secondary:hover {
    background: #667eea !important;
    color: white !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
}

/* Sidebar styling */
.sidebar {
    background: hsl(var(--card));
    border: 1px solid hsl(var(--border));
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-left: 1rem;
}

.sidebar h4 {
    color: hsl(var(--foreground));
    font-weight: 600;
    margin-bottom: 1rem;
    font-size: 1.1rem;
}

.sidebar ul {
    list-style: none;
    padding: 0;
}

.sidebar li {
    padding: 0.5rem 0;
    border-bottom: 1px solid hsl(var(--border));
    color: hsl(var(--muted-foreground));
    font-size: 0.9rem;
}

.sidebar li:last-child {
    border-bottom: none;
}

/* Feature cards */
.feature-card {
    background: hsl(var(--card));
    border: 1px solid hsl(var(--border));
    border-radius: var(--radius);
    padding: 1rem;
    margin: 0.5rem 0;
    transition: all 0.2s ease-in-out;
}

.feature-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}

/* Modern Language Selector */
.language-selector select,
.language-selector .wrap,
.gradio-dropdown {
    background: white !important;
    border: 1px solid #DDDDDD !important;
    border-radius: 10px !important;
    color: #333333 !important;
    padding: 0.875rem 1rem !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
    min-height: 44px !important;
}

.language-selector:hover select,
.language-selector:hover .wrap {
    border-color: #CCCCCC !important;
}

.language-selector select:focus,
.language-selector .wrap:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    outline: none !important;
}

/* Fix any dark mode overrides */
.gradio-container,
.gradio-container * {
    color-scheme: light !important;
}

/* Ensure all form elements are white */
input, textarea, select {
    background: white !important;
    color: hsl(var(--foreground)) !important;
}

/* Chat container scrollbar */
.gradio-chatbot::-webkit-scrollbar {
    width: 6px;
}

.gradio-chatbot::-webkit-scrollbar-track {
    background: hsl(var(--muted));
    border-radius: 3px;
}

.gradio-chatbot::-webkit-scrollbar-thumb {
    background: hsl(var(--muted-foreground) / 0.3);
    border-radius: 3px;
}

.gradio-chatbot::-webkit-scrollbar-thumb:hover {
    background: hsl(var(--muted-foreground) / 0.5);
}

/* Status indicators */
.status-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 0.5rem;
}

.status-online {
    background: #10b981;
}

.status-updating {
    background: #f59e0b;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Responsive design */
@media (max-width: 768px) {
    .gradio-container {
        padding: 1rem;
    }
    
    .header-section h1 {
        font-size: 2rem;
    }
    
    .sidebar {
        margin-left: 0;
        margin-top: 1rem;
    }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: hsl(var(--muted));
}

::-webkit-scrollbar-thumb {
    background: hsl(var(--muted-foreground));
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: hsl(var(--foreground));
}

/* Loading animation */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid hsl(var(--muted));
    border-radius: 50%;
    border-top-color: hsl(var(--primary));
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
"""

# Create modern Gradio interface
with gr.Blocks(
    title="🏛️ GovGuideBot - Maharashtra Government Assistant", 
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
    ),
    css=custom_css
) as demo:
    
    # Header Section
    with gr.Row(elem_classes="header-section"):
        gr.HTML("""
        <div style="text-align: center; color: white;">
            <h1>🏛️ GovGuideBot</h1>
            <h3>AI-Powered Maharashtra Government Documents Assistant</h3>
            <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;">
                <span class="status-indicator status-online"></span>
                <span style="font-size: 0.9rem;">Live & Updated</span>
                <span class="status-indicator status-updating"></span>
                <span style="font-size: 0.9rem;">Auto-Sync Active</span>
            </div>
        </div>
        """)
    
    # Main content area
    with gr.Row():
        # Chat section
        with gr.Column(scale=3, elem_classes="main-content"):
            gr.HTML("""
            <div style="padding: 1.5rem; border-bottom: 1px solid hsl(var(--border));">
                <h3 style="margin: 0; color: hsl(var(--foreground)); font-weight: 600;">
                    💬 Chat Assistant
                </h3>
                <p style="margin: 0.5rem 0 0 0; color: hsl(var(--muted-foreground)); font-size: 0.9rem;">
                    Get instant help with Maharashtra government certificates
                </p>
            </div>
            """)
            
            chatbot = gr.Chatbot(
                height=500,
                label="",
                show_label=False,
                container=False,
                elem_classes="chat-container",
                avatar_images=("👤", "🤖"),
                bubble_full_width=False,
                type="messages"
            )
            
            # Modern Chat Input Section
            gr.HTML("""
            <div style="padding: 0 1.5rem 1rem 1.5rem;">
                <div style="background: #F8F8F8; border: 1px solid #DDDDDD; border-radius: 12px; padding: 0.75rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);">
                    <div style="display: flex; gap: 0.75rem; align-items: flex-end;">
                        <div style="flex: 1; position: relative;">
            """)
            
            with gr.Row():
                with gr.Column(scale=4):
                    msg = gr.Textbox(
                        placeholder="💬 Ask about income certificate, caste certificate, domicile, birth certificate, NCL...",
                        label="",
                        show_label=False,
                        container=False,
                        lines=1,
                        max_lines=3,
                        elem_classes="chat-input-wrapper"
                    )
                
                with gr.Column(scale=1, min_width=120):
                    language_selector = gr.Dropdown(
                        choices=[
                            ("🌐 Auto-detect", "auto"),
                            ("🇬🇧 English", "en"),
                            ("🇮🇳 हिंदी/मराठी", "hi")
                        ],
                        value="auto",
                        label="",
                        show_label=False,
                        container=False,
                        elem_classes="language-selector"
                    )
            
            gr.HTML("""
                        </div>
                    </div>
                </div>
            </div>
            """)
            
            # Modern Button Section
            gr.HTML("""
            <div style="padding: 0 1.5rem 1.5rem 1.5rem;">
                <div style="display: flex; gap: 0.75rem; justify-content: center;">
            """)
            
            with gr.Row():
                submit_btn = gr.Button(
                    "✈️ Send Message", 
                    variant="primary",
                    elem_classes="btn-primary",
                    scale=2,
                    size="lg"
                )
                clear_btn = gr.Button(
                    "🗑️ Clear Chat", 
                    variant="secondary",
                    elem_classes="btn-secondary",
                    scale=1,
                    size="lg"
                )
            
            gr.HTML("""
                </div>
            </div>
            """)
        
        # Sidebar
        with gr.Column(scale=1, elem_classes="sidebar"):
            gr.HTML("""
            <div class="feature-card">
                <h4>📋 Supported Certificates</h4>
                <ul>
                    <li>💰 Income Certificate</li>
                    <li>🏷️ Caste Certificate</li>
                    <li>🏠 Domicile Certificate</li>
                    <li>👶 Birth Certificate</li>
                    <li>📜 Non-Creamy Layer (NCL)</li>
                </ul>
            </div>
            """)
            
            gr.HTML("""
            <div class="feature-card">
                <h4>🌍 Languages Supported</h4>
                <ul>
                    <li>🇬🇧 English</li>
                    <li>🇮🇳 हिंदी (Hindi)</li>
                    <li>🇮🇳 मराठी (Marathi)</li>
                </ul>
            </div>
            """)
            
            gr.HTML("""
            <div class="feature-card">
                <h4>💡 Example Questions</h4>
                <ul>
                    <li>"How to apply for income certificate in Pune?"</li>
                    <li>"What documents needed for OBC certificate?"</li>
                    <li>"Birth certificate online process"</li>
                    <li>"NCL income limit 2025"</li>
                </ul>
            </div>
            """)
            
            gr.HTML("""
            <div class="feature-card">
                <h4>🚀 Key Features</h4>
                <ul>
                    <li>✅ Real-time Government Updates</li>
                    <li>✅ District-specific Information</li>
                    <li>✅ Step-by-step Guidance</li>
                    <li>✅ Office Locations & Contacts</li>
                    <li>✅ Fee & Processing Times</li>
                    <li>✅ Multi-language Support</li>
                </ul>
            </div>
            """)
            
            gr.HTML("""
            <div class="feature-card">
                <h4>🔗 Quick Links</h4>
                <ul>
                    <li><a href="https://aaplesarkar.mahaonline.gov.in/" target="_blank">Aaple Sarkar Portal</a></li>
                    <li><a href="https://edistrict.maharashtra.gov.in/" target="_blank">e-District Portal</a></li>
                    <li><a href="https://crsorgi.gov.in/" target="_blank">Birth Registration</a></li>
                </ul>
            </div>
            """)
    
    # Footer
    gr.HTML("""
    <div style="text-align: center; padding: 2rem; color: hsl(var(--muted-foreground)); border-top: 1px solid hsl(var(--border)); margin-top: 2rem;">
        <p style="margin: 0; font-size: 0.9rem;">
            <strong>⚠️ Disclaimer:</strong> This is an AI assistant for guidance only. 
            For official procedures, please visit government portals or contact offices directly.
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.7;">
            🔄 Auto-updated with latest government notifications • 
            🛡️ Secure & Privacy-focused • 
            🆓 Free for all citizens
        </p>
    </div>
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

# Launch app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7865,
        share=True,
        show_error=True,
        favicon_path=None,
        app_kwargs={"docs_url": None, "redoc_url": None}
    )