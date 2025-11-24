#!/usr/bin/env python3
"""
Update Scheduler for GovGuideBot
Automatically checks for government updates and refreshes knowledge base
"""

import schedule
import time
import threading
import logging
from datetime import datetime
from src.web_scraper import web_scraper
from src.data_loader import DocumentLoader
import json
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UpdateScheduler:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.is_running = False
        self.scheduler_thread = None
        self.last_update_check = None
        
        # Create cache directory
        os.makedirs("cache", exist_ok=True)
        
    def check_for_updates(self):
        """Check for government updates and refresh knowledge base"""
        try:
            logger.info("🔍 Checking for government updates...")
            
            # Scrape for new updates
            new_updates = web_scraper.scrape_government_updates()
            
            if new_updates:
                logger.info(f"📢 Found updates for: {list(new_updates.keys())}")
                
                # Save update summary
                self.save_update_summary(new_updates)
                
                # Trigger knowledge base refresh (if needed)
                self.refresh_knowledge_base()
                
            else:
                logger.info("✅ No new updates found")
            
            self.last_update_check = datetime.now()
            
        except Exception as e:
            logger.error(f"❌ Error during update check: {e}")
    
    def save_update_summary(self, updates: dict):
        """Save summary of latest updates"""
        summary = {
            'last_checked': datetime.now().isoformat(),
            'updates_found': len(updates),
            'certificates_updated': list(updates.keys()),
            'summary': {}
        }
        
        for cert_type, cert_updates in updates.items():
            summary['summary'][cert_type] = {
                'count': len(cert_updates),
                'latest_update': cert_updates[0]['text'][:100] if cert_updates else None
            }
        
        with open('cache/latest_updates.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    
    def refresh_knowledge_base(self):
        """Refresh the knowledge base with updated information"""
        try:
            # This would trigger a reload of the chatbot's knowledge base
            # For now, we'll just log that a refresh is needed
            logger.info("🔄 Knowledge base refresh triggered")
            
            # In a production system, you might:
            # 1. Reload the DocumentLoader
            # 2. Recreate text chunks
            # 3. Update the chatbot's knowledge base
            # 4. Send notification to running chatbot instances
            
        except Exception as e:
            logger.error(f"❌ Error refreshing knowledge base: {e}")
    
    def get_update_status(self) -> dict:
        """Get current update status"""
        try:
            if os.path.exists('cache/latest_updates.json'):
                with open('cache/latest_updates.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'last_checked': None,
            'updates_found': 0,
            'certificates_updated': [],
            'summary': {}
        }
    
    def start_scheduler(self):
        """Start the update scheduler"""
        if self.is_running:
            logger.warning("⚠️ Scheduler is already running")
            return
        
        # Schedule updates
        schedule.every(6).hours.do(self.check_for_updates)  # Every 6 hours
        schedule.every().day.at("09:00").do(self.check_for_updates)  # Daily at 9 AM
        schedule.every().monday.at("08:00").do(self.check_for_updates)  # Weekly on Monday
        
        self.is_running = True
        
        def run_scheduler():
            logger.info("🚀 Update scheduler started")
            logger.info("📅 Schedule: Every 6 hours, Daily at 9 AM, Weekly on Monday")
            
            # Run initial check
            self.check_for_updates()
            
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop the update scheduler"""
        self.is_running = False
        schedule.clear()
        logger.info("🛑 Update scheduler stopped")
    
    def force_update_check(self):
        """Force an immediate update check"""
        logger.info("🔄 Forcing immediate update check...")
        self.check_for_updates()

# Singleton instance
update_scheduler = UpdateScheduler()

if __name__ == "__main__":
    # Test the scheduler
    scheduler = UpdateScheduler()
    
    print("Testing update scheduler...")
    scheduler.force_update_check()
    
    print("\nUpdate status:")
    status = scheduler.get_update_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))