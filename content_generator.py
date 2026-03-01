"""
Content Generator for HTML News Articles
Uses Ollama for AI-powered HTML content creation
"""

from typing import Optional, List, Dict, Any
from ollama_client import ollama
from news_monitor import news_monitor
from database import get_news, add_post
from alert_system import alert_system

class ContentGenerator:
    def __init__(self):
        self.ollama = ollama
        self.alerts = alert_system

    def check_ollama_status(self) -> bool:
        return self.ollama.check_connection()

    def generate_html_from_news(self, news_item: Dict[str, Any]) -> Optional[str]:
        if not self.check_ollama_status():
            self.alerts.alert_ollama_offline()
            return None

        html_content = self.ollama.generate_linkedin_post(news_item)

        if html_content:
            # Salva l'articolo HTML
            filepath = self.ollama.save_html_article(html_content, news_item, "linkedin")
            
            # Crea un post che punti all'HTML
            post_content = f"Nuovo articolo pubblicato: {news_item.get('title', 'Articolo')}\n\nLeggi l'analisi completa qui: {filepath}\n\nFonte: {news_item.get('link', 'N/A')}"
            add_post(post_content, news_item['id'])
            
            self.alerts.alert_post_ready(news_item.get('title', 'Nuovo Articolo'))
            return filepath

        return None

    def generate_daily_html_content(self) -> List[str]:
        if not self.check_ollama_status():
            return []

        all_news = get_news()
        unprocessed = [item for item in all_news.values() if not item.get('processed', False)]

        generated_files = []
        for item in unprocessed[:5]:
            filepath = self.generate_html_from_news(item)
            if filepath:
                item['processed'] = True
                all_news[item['id']] = item
                from database import save_news
                save_news(all_news)
                generated_files.append(filepath)

        return generated_files

content_generator = ContentGenerator()