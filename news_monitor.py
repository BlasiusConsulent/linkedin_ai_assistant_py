"""
News Monitor for IT/CyberSecurity Topics
RSS Feed Aggregator with Keyword Filtering
"""

import feedparser
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import config
from database import add_news_item

class NewsMonitor:
    def __init__(self):
        self.sources = config.news_sources
        self.keywords = config.keywords
    
    def fetch_feed(self, url: str) -> Optional[List[Dict[str, Any]]]:
        try:
            feed = feedparser.parse(url)
            entries = []
            
            for entry in feed.entries[:20]:
                item = {
                    'id': hashlib.md5(entry.link.encode()).hexdigest(),
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source': feed.feed.get('title', 'Unknown'),
                    'source_url': url,
                    'summary': entry.get('summary', entry.get('description', ''))[:1000],
                    'fetched_at': datetime.now().isoformat()
                }
                entries.append(item)
            
            return entries
            
        except Exception as e:
            print(f"Error fetching feed {url}: {e}")
            return None
    
    def filter_by_keywords(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered = []
        
        for item in items:
            text = f"{item['title']} {item['summary']}".lower()
            
            if any(keyword.lower() in text for keyword in self.keywords):
                score = sum(1 for keyword in self.keywords if keyword.lower() in text)
                item['relevance_score'] = score
                filtered.append(item)
        
        filtered.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return filtered
    
    def check_duplicates(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Usa una funzione helper per controllare se la news esiste
        from database import get_news
        existing_news = get_news()
        
        new_items = []
        for item in items:
            if item['id'] not in existing_news:
                new_items.append(item)
                add_news_item(item)
        
        return new_items
    
    def fetch_all(self) -> List[Dict[str, Any]]:
        all_items = []
        
        for source in self.sources:
            print(f"Fetching: {source[:50]}...")
            items = self.fetch_feed(source)
            if items:
                all_items.extend(items)
        
        filtered = self.filter_by_keywords(all_items)
        new_items = self.check_duplicates(filtered)
        
        print(f"Total: {len(all_items)}, Filtered: {len(filtered)}, New: {len(new_items)}")
        return new_items

    def search_news(self, query: str = "", date_filter: str = "") -> List[Dict[str, Any]]:
        """Ricerca notizie per titolo/data"""
        from database import get_news
        all_news = get_news()
        
        results = []
        for item in all_news.values():
            match = True
            
            # Filtro per titolo
            if query and query.lower() not in item.get('title', '').lower():
                match = False
            
            # Filtro per data (formato YYYY-MM-DD)
            if date_filter and date_filter not in item.get('published', ''):
                match = False
            
            if match:
                results.append(item)
        
        # Ordina per data decrescente
        results.sort(key=lambda x: x.get('published', ''), reverse=True)
        return results

news_monitor = NewsMonitor()
