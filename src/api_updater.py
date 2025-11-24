#!/usr/bin/env python3
"""
API-based updater for government information
Uses official APIs and RSS feeds where available
"""

import requests
import json
import os
from datetime import datetime
import logging
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

class APIUpdater:
    def __init__(self):
        # Disable SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Government API endpoints and RSS feeds
        self.api_endpoints = {
            'maharashtra_gov': {
                'base_url': 'https://www.maharashtra.gov.in',
                'rss_feeds': [
                    '/rss/news.xml',
                    '/rss/notifications.xml',
                    '/rss/circulars.xml'
                ]
            },
            'aaple_sarkar': {
                'base_url': 'https://aaplesarkar.mahaonline.gov.in',
                'api_endpoints': [
                    '/api/services',
                    '/api/notifications'
                ]
            }
        }
        
        # Cache directory
        self.cache_dir = "cache/api_updates"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def fetch_with_fallback(self, url: str) -> Optional[str]:
        """Fetch content with multiple fallback methods"""
        methods = [
            # Method 1: Standard requests with SSL disabled
            lambda: requests.get(url, verify=False, timeout=10).text,
            
            # Method 2: Using different user agent
            lambda: requests.get(
                url, 
                verify=False, 
                timeout=10,
                headers={'User-Agent': 'GovGuideBot/1.0 (+https://github.com/govguidebot)'}
            ).text,
            
            # Method 3: Using curl-like headers
            lambda: requests.get(
                url,
                verify=False,
                timeout=10,
                headers={
                    'User-Agent': 'curl/7.68.0',
                    'Accept': '*/*'
                }
            ).text
        ]
        
        for i, method in enumerate(methods):
            try:
                content = method()
                logger.info(f"✓ Successfully fetched {url} using method {i+1}")
                return content
            except Exception as e:
                logger.warning(f"Method {i+1} failed for {url}: {e}")
                continue
        
        logger.error(f"All methods failed for {url}")
        return None
    
    def parse_rss_feed(self, rss_content: str) -> List[Dict]:
        """Parse RSS feed content"""
        try:
            root = ET.fromstring(rss_content)
            items = []
            
            for item in root.findall('.//item'):
                title = item.find('title')
                description = item.find('description')
                link = item.find('link')
                pub_date = item.find('pubDate')
                
                items.append({
                    'title': title.text if title is not None else '',
                    'description': description.text if description is not None else '',
                    'link': link.text if link is not None else '',
                    'date': pub_date.text if pub_date is not None else '',
                    'extracted_at': datetime.now().isoformat()
                })
            
            return items
        except Exception as e:
            logger.error(f"Error parsing RSS feed: {e}")
            return []
    
    def check_government_apis(self) -> Dict[str, List[Dict]]:
        """Check government APIs and RSS feeds for updates"""
        all_updates = {}
        
        for source_name, config in self.api_endpoints.items():
            logger.info(f"Checking {source_name}...")
            
            # Try RSS feeds first
            if 'rss_feeds' in config:
                for rss_path in config['rss_feeds']:
                    rss_url = config['base_url'] + rss_path
                    content = self.fetch_with_fallback(rss_url)
                    
                    if content:
                        items = self.parse_rss_feed(content)
                        if items:
                            source_key = f"{source_name}_rss"
                            if source_key not in all_updates:
                                all_updates[source_key] = []
                            all_updates[source_key].extend(items)
            
            # Try API endpoints
            if 'api_endpoints' in config:
                for api_path in config['api_endpoints']:
                    api_url = config['base_url'] + api_path
                    content = self.fetch_with_fallback(api_url)
                    
                    if content:
                        try:
                            data = json.loads(content)
                            source_key = f"{source_name}_api"
                            if source_key not in all_updates:
                                all_updates[source_key] = []
                            all_updates[source_key].append({
                                'data': data,
                                'source_url': api_url,
                                'extracted_at': datetime.now().isoformat()
                            })
                        except json.JSONDecodeError:
                            logger.warning(f"Invalid JSON from {api_url}")
        
        return all_updates
    
    def create_mock_updates(self) -> Dict[str, List[Dict]]:
        """Create mock updates for demonstration"""
        mock_updates = {
            'income_certificate': [{
                'title': 'Income Certificate Fee Revision',
                'description': 'Processing fee for Income Certificate revised to ₹30 effective from February 2025. Online applications now processed within 5 working days.',
                'date': '2025-01-20',
                'source': 'Maharashtra Revenue Department',
                'link': 'https://revenue.maharashtra.gov.in/notifications/income-cert-fee-2025',
                'extracted_at': datetime.now().isoformat()
            }],
            'caste_certificate': [{
                'title': 'Caste Validity Committee Schedule',
                'description': 'New schedule for Caste Validity Committee meetings announced. Monthly meetings on first Monday of each month.',
                'date': '2025-01-18',
                'source': 'Social Justice Department',
                'link': 'https://sjsa.maharashtra.gov.in/cvc-schedule-2025',
                'extracted_at': datetime.now().isoformat()
            }],
            'ncl_certificate': [{
                'title': 'NCL Income Limit Update',
                'description': 'Non-Creamy Layer income limit increased to ₹9,00,000 per annum for the year 2025-26.',
                'date': '2025-01-15',
                'source': 'Social Justice Department',
                'link': 'https://sjsa.maharashtra.gov.in/ncl-income-limit-2025',
                'extracted_at': datetime.now().isoformat()
            }]
        }
        
        # Save mock updates
        for cert_type, updates in mock_updates.items():
            cache_file = os.path.join(self.cache_dir, f"{cert_type}_updates.json")
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(updates, f, indent=2, ensure_ascii=False)
        
        logger.info("✓ Mock updates created successfully")
        return mock_updates
    
    def get_formatted_updates(self, certificate_type: str) -> str:
        """Get formatted updates for a certificate type"""
        cache_file = os.path.join(self.cache_dir, f"{certificate_type}_updates.json")
        
        if not os.path.exists(cache_file):
            return ""
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                updates = json.load(f)
            
            if not updates:
                return ""
            
            formatted_updates = "\n\n🔔 **RECENT GOVERNMENT UPDATES:**\n"
            
            for i, update in enumerate(updates[-2:], 1):  # Show last 2 updates
                formatted_updates += f"\n**Update {i}:**\n"
                formatted_updates += f"• {update.get('title', update.get('description', 'Government Update'))}\n"
                
                if update.get('description') and update.get('title'):
                    formatted_updates += f"• Details: {update['description'][:150]}{'...' if len(update['description']) > 150 else ''}\n"
                
                if update.get('date'):
                    formatted_updates += f"• Date: {update['date']}\n"
                
                if update.get('link'):
                    formatted_updates += f"• Link: {update['link']}\n"
                
                formatted_updates += f"• Source: {update.get('source', 'Government Website')}\n"
            
            formatted_updates += "\n⚠️ **Note:** Please verify latest information on official government portals.\n"
            
            return formatted_updates
            
        except Exception as e:
            logger.error(f"Error reading updates for {certificate_type}: {e}")
            return ""

# Singleton instance
api_updater = APIUpdater()

if __name__ == "__main__":
    # Test the API updater
    updater = APIUpdater()
    
    print("🚀 Testing API-based updates...")
    
    # Create mock updates for demonstration
    mock_updates = updater.create_mock_updates()
    
    print(f"✓ Created updates for {len(mock_updates)} certificate types")
    
    # Test formatting
    for cert_type in mock_updates.keys():
        formatted = updater.get_formatted_updates(cert_type)
        print(f"\n📋 {cert_type.replace('_', ' ').title()} Updates:")
        print(formatted)