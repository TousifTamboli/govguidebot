# app.py
import os
import ssl
import certifi

# Fix SSL certificate issue on Windows
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['CURL_CA_BUNDLE'] = certifi.where()
ssl._create_default_https_context = ssl._create_unverified_context

import gradio as gr
import google.generativeai as genai
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

chat_sessions = []

def chat_interface(message, history, language, session_index):
    """Gradio chat interface"""
    
    if not message.strip():
        return history, "", gr.update(), session_index
    
    # Get response
    response = bot.chat(message, language=language)
    
    # Update history (Gradio 6 uses dict format with 'role' and 'content')
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response['answer']})
    
    if session_index is None or session_index == "":
        title = message[:30] + "..." if len(message) > 30 else message
        chat_sessions.append({"title": title, "history": history.copy()})
        session_index = len(chat_sessions) - 1
    else:
        chat_sessions[int(session_index)]["history"] = history.copy()
        
    choices = [(s["title"], i) for i, s in enumerate(chat_sessions)]
    
    return history, "", gr.update(choices=choices, value=session_index), session_index

def reset_chat():
    """Reset conversation"""
    bot.reset_conversation()
    return [], "Conversation reset!", gr.update(value=None), None

def load_chat(session_index):
    """Load a previous chat session"""
    if session_index is None or session_index == "":
        return [], None
    bot.reset_conversation()
    history = chat_sessions[int(session_index)]["history"]
    return history.copy(), session_index

def process_audio(audio_path):
    """Transcribe audio using Gemini"""
    if not audio_path:
        return ""
    try:
        audio_file = genai.upload_file(audio_path)
        prompt = "Transcribe exactly what is spoken in this audio. The language might be English, Hindi, or Marathi. Do not answer questions, just return the transcription."
        response = bot.model.generate_content([prompt, audio_file])
        try:
            genai.delete_file(audio_file.name)
        except:
            pass
        return response.text.strip()
    except Exception as e:
        print(f"Error processing audio: {e}")
        return "Error transcribing audio. Please try typing instead."

# Create Gradio interface
with gr.Blocks(title="GovGuideBot - Maharashtra Government Documents Assistant") as demo:
    
    gr.Markdown("""
    # 🏛️ GovGuideBot
    ### AI Assistant for Maharashtra Government Documents
    
    Get help with:
    - Income Certificate (उत्पन्न प्रमाणपत्र)
    - Caste Certificate (जात प्रमाणपत्र)
    - Domicile Certificate (अधिवास प्रमाणपत्र)
    - And more...
    
    **Languages supported:** English, Hindi (हिंदी), Marathi (मराठी)
    """)
    
    session_state = gr.State(None)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🕒 Chat History")
            history_radio = gr.Radio(
                choices=[],
                label="Past Sessions",
                interactive=True
            )
            new_chat_btn = gr.Button("➕ New Chat", variant="secondary")

        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                height=500,
                label="Chat with GovGuideBot"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ask me about government documents... Select language above for consistent responses",
                    label="Your Message",
                    scale=4
                )
                voice_in = gr.Audio(
                    sources=["microphone"], 
                    type="filepath", 
                    label="Voice Input 🎤", 
                    scale=1
                )
                language_selector = gr.Dropdown(
                    choices=[
                        ("Auto-detect", "auto"),
                        ("English Only", "en"),
                        ("Hindi Only (हिंदी)", "hi"),
                        ("Marathi Only (मराठी)", "mr")
                    ],
                    value="auto",
                    label="Response Language",
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
            """)
    
    # Event handlers
    submit_btn.click(
        chat_interface,
        inputs=[msg, chatbot, language_selector, session_state],
        outputs=[chatbot, msg, history_radio, session_state]
    )
    
    msg.submit(
        chat_interface,
        inputs=[msg, chatbot, language_selector, session_state],
        outputs=[chatbot, msg, history_radio, session_state]
    )
    
    clear_btn.click(
        reset_chat,
        outputs=[chatbot, msg, history_radio, session_state]
    )

    new_chat_btn.click(
        reset_chat,
        outputs=[chatbot, msg, history_radio, session_state]
    )

    history_radio.change(
        load_chat,
        inputs=[history_radio],
        outputs=[chatbot, session_state]
    )

    voice_in.change(
        process_audio,
        inputs=[voice_in],
        outputs=[msg]
    )
    
    gr.Markdown("""
    ---
    **Note:** This is an AI assistant. For official information, please visit government portals or contact offices directly.
    
    **Free Tier Limits:** 15 requests per minute, 1500 requests per day
    """)

# Launch app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=True,  # Creates public URL
        theme=gr.themes.Soft()
    )