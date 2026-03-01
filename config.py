import json
import os
from pathlib import Path
from typing import Dict, Any, List

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.config_path = Path("config.json")
        self.config: Dict[str, Any] = {}
        self._ensure_directories()
        self._load_config()
        self._initialized = True

    def _ensure_directories(self):
        directories = ["data", "logs", "cache"]
        for dir_name in directories:
            Path(dir_name).mkdir(exist_ok=True)

    def _load_config(self):
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self._get_default_config()
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "ollama": {"base_url": "http://localhost:11434", "model": "llama3", "timeout": 300},
            "news_sources": ["https://feeds.feedburner.com/TheHackersNews"],
            "keywords": ["cybersecurity", "AI", "IT", "job"],
            "alerts": {"enabled": True, "check_interval_minutes": 30},
            "linkedin": {"post_frequency_days": 3, "max_post_length": 2600},
            "user_profile": {"name": "Biagio Apostolico", "role": "Senior ICT Consultant"}
        }

    def save_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key: str, value: Any):
        """
        Imposta un valore nella configurazione e salva su file
        Usa la notazione punto (es: 'ollama.model')
        """
        keys = key.split('.')
        config = self.config
        
        # Scorri fino al penultimo livello
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Imposta il valore all'ultima chiave
        config[keys[-1]] = value
        
        # Salva la configurazione aggiornata
        self.save_config()

    @property
    def ollama_url(self) -> str:
        return self.get('ollama.base_url', 'http://localhost:11434')

    @property
    def ollama_model(self) -> str:
        return self.get('ollama.model', 'llama3')

    @property
    def news_sources(self) -> List[str]:
        return self.get('news_sources', [])

    @property
    def keywords(self) -> List[str]:
        return self.get('keywords', [])

    @property
    def user_profile(self) -> Dict[str, Any]:
        return self.get('user_profile', {})

config = Config()
