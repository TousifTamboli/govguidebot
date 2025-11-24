#!/usr/bin/env python3
"""
Admin Panel for GovGuideBot
Manage updates, view status, and control the update scheduler
"""

import gradio as gr
import json
import os
from datetime import datetime
from src.update_scheduler import update_scheduler
from src.web_scraper import web_scraper

def get_update_status():
    """Get current update status"""
    status = update_scheduler.get_update_status()
    
    if status['last_checked']:
        last_checked = datetime.fromisoformat(status['last_checked']).strftime("%Y-%m-%d %H:%M:%S")
    else:
        last_checked = "Never"
    
    status_text = f"""
📊 **Update Status**

🕐 Last Checked: {last_checked}
📢 Updates Found: {status['updates_found']}
📋 Certificates Updated: {', '.join(status['certificates_updated']) if status['certificates_updated'] else 'None'}

📝 **Summary:**
"""
    
    for cert_type, summary in status.get('summary', {}).items():
        status_text += f"\n• **{cert_type.replace('_', ' ').title()}**: {summary['count']} updates"
        if summary.get('latest_update'):
            status_text += f"\n  Latest: {summary['latest_update']}..."
    
    return status_text

def force_update():
    """Force an immediate update check"""
    try:
        update_scheduler.force_update_check()
        return "✅ Update check completed! Check status above for results."
    except Exception as e:
        return f"❌ Error during update: {str(e)}"

def view_recent_updates(certificate_type):
    """View recent updates for a certificate type"""
    try:
        updates = web_scraper.get_recent_updates(certificate_type, days=30)
        
        if not updates:
            return f"No recent updates found for {certificate_type.replace('_', ' ').title()}"
        
        updates_text = f"📋 **Recent Updates for {certificate_type.replace('_', ' ').title()}**\n\n"
        
        for i, update in enumerate(updates[-5:], 1):  # Show last 5 updates
            updates_text += f"**Update {i}:**\n"
            updates_text += f"📝 {update['text'][:300]}{'...' if len(update['text']) > 300 else ''}\n"
            
            if update.get('date'):
                updates_text += f"📅 Date: {update['date']}\n"
            
            if update.get('links'):
                for link in update['links'][:2]:
                    updates_text += f"🔗 Link: {link['url']}\n"
            
            updates_text += f"🌐 Source: {update.get('site', 'Government Website')}\n"
            updates_text += f"⏰ Extracted: {update.get('extracted_at', 'Unknown')}\n\n"
            updates_text += "─" * 50 + "\n\n"
        
        return updates_text
        
    except Exception as e:
        return f"❌ Error retrieving updates: {str(e)}"

def clear_cache():
    """Clear update cache"""
    try:
        cache_dir = "cache/updates"
        if os.path.exists(cache_dir):
            for file in os.listdir(cache_dir):
                os.remove(os.path.join(cache_dir, file))
        
        if os.path.exists("cache/latest_updates.json"):
            os.remove("cache/latest_updates.json")
        
        return "✅ Cache cleared successfully!"
    except Exception as e:
        return f"❌ Error clearing cache: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="GovGuideBot Admin Panel", theme=gr.themes.Soft()) as admin_demo:
    
    gr.Markdown("""
    # 🔧 GovGuideBot Admin Panel
    ### Manage Government Updates & Monitor System Status
    """)
    
    with gr.Tab("📊 Status Dashboard"):
        gr.Markdown("## Current Update Status")
        
        status_display = gr.Markdown(get_update_status())
        
        with gr.Row():
            refresh_btn = gr.Button("🔄 Refresh Status", variant="secondary")
            force_update_btn = gr.Button("⚡ Force Update Check", variant="primary")
        
        update_result = gr.Markdown("")
        
        refresh_btn.click(
            fn=get_update_status,
            outputs=status_display
        )
        
        force_update_btn.click(
            fn=force_update,
            outputs=update_result
        )
    
    with gr.Tab("📋 View Updates"):
        gr.Markdown("## Recent Government Updates by Certificate Type")
        
        certificate_dropdown = gr.Dropdown(
            choices=[
                ("Income Certificate", "income_certificate"),
                ("Caste Certificate", "caste_certificate"),
                ("Domicile Certificate", "domicile_certificate"),
                ("Birth Certificate", "birth_certificate"),
                ("Non-Creamy Layer Certificate", "non_creamy_certificate")
            ],
            label="Select Certificate Type",
            value="income_certificate"
        )
        
        view_updates_btn = gr.Button("📖 View Recent Updates", variant="primary")
        
        updates_display = gr.Markdown("")
        
        view_updates_btn.click(
            fn=view_recent_updates,
            inputs=certificate_dropdown,
            outputs=updates_display
        )
    
    with gr.Tab("🛠️ System Management"):
        gr.Markdown("## System Management Tools")
        
        with gr.Row():
            clear_cache_btn = gr.Button("🗑️ Clear Update Cache", variant="secondary")
        
        management_result = gr.Markdown("")
        
        clear_cache_btn.click(
            fn=clear_cache,
            outputs=management_result
        )
        
        gr.Markdown("""
        ### 📝 System Information
        
        **Update Schedule:**
        - Every 6 hours
        - Daily at 9:00 AM
        - Weekly on Monday at 8:00 AM
        
        **Monitored Websites:**
        - Aaple Sarkar Portal
        - Social Justice Department
        - Revenue Department
        - Mantralaya
        - CRS Portal
        
        **Cache Location:** `cache/updates/`
        """)

if __name__ == "__main__":
    admin_demo.launch(
        server_name="0.0.0.0",
        server_port=7863,
        share=False,
        auth=("admin", "govguide123")  # Simple authentication
    )