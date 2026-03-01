"""
Alert System with Desktop Notifications
Now saves alerts in plain text files
"""

from plyer import notification
import winsound
from database import add_alert, get_alerts
from config import config

class AlertSystem:
    def __init__(self):
        self.app_name = "LinkedIn AI Assistant"

    def send_notification(self, title: str, message: str, alert_type: str = "info"):
        add_alert(alert_type, title, message)

        try:
            notification.notify(
                title=f"{self.app_name} - {title}",
                message=message,
                app_name=self.app_name,
                timeout=10
            )
        except Exception as e:
            print(f"Notification error: {e}")

        print(f"[ALERT] {title}: {message}")

    def alert_new_news(self, count: int):
        if count == 0:
            return
        self.send_notification(f"📰 {count} Nuove News IT", "Clicca per generare contenuti", "info")

    def alert_post_ready(self, post_title: str):
        self.send_notification("✍️ Post Pronto", f"{post_title[:50]}...", "info")

    def alert_ollama_offline(self):
        self.send_notification("⚠️ Ollama Non Rilevato", "Avvia Ollama per continuare", "urgent")

alert_system = AlertSystem()
