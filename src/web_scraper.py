#!/usr/bin/env python3
"""
Web Scraper for Government Updates
Monitors Maharashtra government websites for GRs, notifications, and updates
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Optional
import hashlib
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GovWebScraper:
    def __init__(self):
        # Fix SSL certificate issues
        import ssl
        import certifi
        import urllib3
        
        # Set SSL certificate path
        os.environ['SSL_CERT_FILE'] = certifi.where()
        os.environ['CURL_CA_BUNDLE'] = certifi.where()
        
        # Create session with proper SSL handling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Disable SSL verification for government sites (they often have certificate issues)
        self.session.verify = False
        
        # Suppress SSL warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Alternative: Use system certificates
        try:
            self.session.verify = certifi.where()
        except:
            self.session.verify = False
        
        # Government websites to monitor
        self.gov_websites = {
            'aaple_sarkar': 'https://aaplesarkar.mahaonline.gov.in',
            'social_justice': 'https://sjsa.maharashtra.gov.in',
            'revenue_dept': 'https://revenue.maharashtra.gov.in',
            'mantralaya': 'https://www.maharashtra.gov.in',
            'crsorgi': 'https://crsorgi.gov.in'
        }
        
        # Keywords to monitor for each certificate type
        self.certificate_keywords = {
            'income_certificate': [
                'income certificate', 'उत्पन्न प्रमाणपत्र', 'income limit', 'processing fee',
                'RTS timeline', 'income proof', 'salary certificate'
            ],
            'caste_certificate': [
                'caste certificate', 'जात प्रमाणपत्र', 'OBC', 'SC', 'ST', 'VJNT', 'SBC',
                'caste validity', 'scrutiny committee', 'CVC'
            ],
            'domicile_certificate': [
                'domicile certificate', 'अधिवास प्रमाणपत्र', '15 year residence',
                'domicile proof', 'residence certificate'
            ],
            'birth_certificate': [
                'birth certificate', 'जन्म प्रमाणपत्र', 'birth registration',
                'CRS portal', 'delayed registration'
            ],
            'non_creamy_certificate': [
                'non creamy layer', 'NCL', 'गैर क्रीमी स्तर', 'income limit 8 lakh',
                'creamy layer', 'OBC reservation'
            ]
        }
        
        # Cache directory for storing updates
        self.cache_dir = "cache/updates"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def fetch_page_content(self, url: str) -> Optional[str]:
        """Fetch content from a webpage with retry logic"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Try with different SSL configurations
                ssl_configs = [
                    {'verify': False},  # No SSL verification
                    {'verify': True},   # Default SSL verification
                ]
                
                for config in ssl_configs:
                    try:
                        response = self.session.get(
                            url, 
                            timeout=15,
                            **config
                        )
                        response.raise_for_status()
                        logger.info(f"✓ Successfully fetched {url}")
                        return response.text
                    except requests.exceptions.SSLError:
                        continue
                    except Exception as e:
                        if attempt == max_retries - 1:
                            logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                        continue
                
                # If all SSL configs fail, try with requests without session
                try:
                    import urllib3
                    urllib3.disable_warnings()
                    
                    response = requests.get(
                        url, 
                        timeout=15, 
                        verify=False,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    )
                    response.raise_for_status()
                    logger.info(f"✓ Successfully fetched {url} (fallback method)")
                    return response.text
                except:
                    pass
                    
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed to fetch {url} after {max_retries} attempts: {e}")
                else:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    def extract_notifications(self, html_content: str, base_url: str) -> List[Dict]:
        """Extract notifications and updates from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        notifications = []
        
        # Common selectors for notifications
        selectors = [
            '.notification', '.news', '.update', '.circular',
            '.gr-list', '.announcement', '.latest-news',
            '[class*="notification"]', '[class*="news"]',
            '[class*="update"]', '[class*="circular"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                notification = self.parse_notification_element(element, base_url)
                if notification:
                    notifications.append(notification)
        
        return notifications
    
    def parse_notification_element(self, element, base_url: str) -> Optional[Dict]:
        """Parse individual notification element"""
        try:
            # Extract text content
            text = element.get_text(strip=True)
            if len(text) < 10:  # Skip very short texts
                return None
            
            # Extract links
            links = []
            for link in element.find_all('a', href=True):
                href = link['href']
                if href.startswith('/'):
                    href = base_url + href
                links.append({
                    'text': link.get_text(strip=True),
                    'url': href
                })
            
            # Extract date if available
            date_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', text)
            date_str = date_match.group(1) if date_match else None
            
            return {
                'text': text,
                'links': links,
                'date': date_str,
                'source_url': base_url,
                'extracted_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error parsing notification element: {e}")
            return None
    
    def check_relevance(self, notification: Dict, certificate_type: str) -> bool:
        """Check if notification is relevant to a certificate type"""
        keywords = self.certificate_keywords.get(certificate_type, [])
        text_lower = notification['text'].lower()
        
        # Check if any keyword matches
        for keyword in keywords:
            if keyword.lower() in text_lower:
                return True
        
        return False
    
    def get_content_hash(self, content: str) -> str:
        """Generate hash for content to detect changes"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def save_update(self, certificate_type: str, update_data: Dict):
        """Save update to cache file"""
        cache_file = os.path.join(self.cache_dir, f"{certificate_type}_updates.json")
        
        # Load existing updates
        updates = []
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    updates = json.load(f)
            except:
                updates = []
        
        # Add new update
        update_data['id'] = self.get_content_hash(update_data['text'])
        
        # Check if update already exists
        existing_ids = [u.get('id') for u in updates]
        if update_data['id'] not in existing_ids:
            updates.append(update_data)
            
            # Keep only last 50 updates
            updates = updates[-50:]
            
            # Save updates
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(updates, f, indent=2, ensure_ascii=False)
            
            logger.info(f"New update saved for {certificate_type}")
            return True
        
        return False
    
    def scrape_government_updates(self) -> Dict[str, List[Dict]]:
        """Main method to scrape all government websites for updates"""
        all_updates = {}
        
        for site_name, base_url in self.gov_websites.items():
            logger.info(f"Scraping {site_name}: {base_url}")
            
            # Try different common paths for notifications
            paths_to_check = [
                '/',
                '/notifications',
                '/news',
                '/updates',
                '/circulars',
                '/gr',
                '/en/notifications',
                '/en/news'
            ]
            
            for path in paths_to_check:
                url = base_url + path
                content = self.fetch_page_content(url)
                
                if content:
                    notifications = self.extract_notifications(content, base_url)
                    
                    # Categorize notifications by certificate type
                    for notification in notifications:
                        for cert_type in self.certificate_keywords.keys():
                            if self.check_relevance(notification, cert_type):
                                notification['site'] = site_name
                                notification['certificate_type'] = cert_type
                                
                                # Save if new
                                if self.save_update(cert_type, notification):
                                    if cert_type not in all_updates:
                                        all_updates[cert_type] = []
                                    all_updates[cert_type].append(notification)
                
                # Be respectful to servers
                time.sleep(1)
        
        return all_updates
    
    def get_recent_updates(self, certificate_type: str, days: int = 30) -> List[Dict]:
        """Get recent updates for a certificate type"""
        cache_file = os.path.join(self.cache_dir, f"{certificate_type}_updates.json")
        
        if not os.path.exists(cache_file):
            return []
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                updates = json.load(f)
            
            # Filter by date
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_updates = []
            
            for update in updates:
                try:
                    update_date = datetime.fromisoformat(update['extracted_at'])
                    if update_date >= cutoff_date:
                        recent_updates.append(update)
                except:
                    # Include updates without valid dates
                    recent_updates.append(update)
            
            return recent_updates[-10:]  # Return last 10 updates
            
        except Exception as e:
            logger.error(f"Error reading updates for {certificate_type}: {e}")
            return []
    
    def format_updates_for_chatbot(self, certificate_type: str) -> str:
        """Format recent updates for inclusion in chatbot responses"""
        updates = self.get_recent_updates(certificate_type, days=30)
        
        if not updates:
            return ""
        
        formatted_updates = "\n\n🔔 **RECENT GOVERNMENT UPDATES:**\n"
        
        for i, update in enumerate(updates[-3:], 1):  # Show last 3 updates
            formatted_updates += f"\n**Update {i}:**\n"
            formatted_updates += f"• {update['text'][:200]}{'...' if len(update['text']) > 200 else ''}\n"
            
            if update.get('date'):
                formatted_updates += f"• Date: {update['date']}\n"
            
            if update.get('links'):
                for link in update['links'][:2]:  # Show max 2 links
                    formatted_updates += f"• Link: {link['url']}\n"
            
            formatted_updates += f"• Source: {update.get('site', 'Government Website')}\n"
        
        formatted_updates += "\n⚠️ **Note:** Please verify latest information on official government portals.\n"
        
        return formatted_updates

# Singleton instance
web_scraper = GovWebScraper()

if __name__ == "__main__":
    # Test the scraper
    scraper = GovWebScraper()
    updates = scraper.scrape_government_updates()
    
    for cert_type, cert_updates in updates.items():
        print(f"\n{cert_type.upper()}: {len(cert_updates)} new updates")
        for update in cert_updates[:2]:  # Show first 2
            print(f"  - {update['text'][:100]}...")