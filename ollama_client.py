"""
Ollama Client for Local AI Processing
Now supports platform-specific prompts for social media
"""

import requests
import json
from typing import Optional, Dict, Any
from config import config
import os
from datetime import datetime

class OllamaClient:
    def __init__(self):
        self.base_url = config.ollama_url
        self.model = config.ollama_model
        self.timeout = config.get('ollama.timeout', 300)
        self.current_platform = 'linkedin'  # Default
    
    def check_connection(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Ollama connection error: {e}")
            return False
    
    def list_models(self) -> list:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                model_names = [model.get('name', '') for model in models if model.get('name')]
                return model_names
            return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def set_model(self, model_name: str):
        self.model = model_name
        from config import config as cfg
        cfg.set('ollama.model', model_name)
    
    def set_platform(self, platform: str):
        """Imposta la piattaforma per i prompt successivi"""
        self.current_platform = platform.lower()
    
    def generate(self, prompt: str) -> Optional[str]:
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "top_p": 0.9, "num_predict": 2048}
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return data.get('response', '').strip()
                except json.JSONDecodeError:
                    return response.text.strip()
            else:
                print(f"Ollama error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Generation error: {e}")
            return None
    
    def get_platform_prompt(self, platform: str = None) -> str:
        """Restituisce il prompt specifico per la piattaforma"""
        if platform is None:
            platform = self.current_platform
        
        profile = config.user_profile
        sector = ', '.join(profile.get('specializations', ['IT']))
        
        prompts = {
            'linkedin': f"""Sei un redattore professionista specializzato in LinkedIn.
Il tuo compito è tradurre fedelmente contenuti forniti dall'utente e trasformarli in post LinkedIn autorevoli e accurati.

Regole fondamentali:
- NON inventare dati, numeri, dichiarazioni o contesto non presenti nel testo originale.
- NON aggiungere opinioni personali se non richiesto.
- NON alterare il significato del testo originale.
- Se un'informazione non è chiara, riformulala in modo neutro senza speculare.
- Mantieni precisione terminologica.
- Scrivi in italiano professionale, chiaro, credibile.
- Evita tono sensazionalistico o clickbait.

Struttura obbligatoria del post:
1) Hook iniziale professionale (1-2 frasi)
2) Sintesi fedele della notizia
3) 3 punti chiave chiari e concreti
4) Chiusura con riflessione neutra o implicazione per il settore
5) 3 hashtag pertinenti massimo

Il post deve sembrare scritto da un esperto del settore, non da un generatore automatico.

Se il testo contiene dati numerici, riportali esattamente come nel testo originale.
Se un dato non è presente, NON inserirlo.
Se una parte non è verificabile dal testo fornito, omettila.
Non utilizzare espressioni come:
- "secondo gli esperti"
- "è probabile che"
- "questo potrebbe significare"
a meno che siano nel testo originale.

Esigo controllo ortografico e traduzione 15 volte e applica la correzione.

SETTORE: {sector}""",
            
            'instagram': f"""Sei un copywriter esperto di Instagram e social media marketing.
Il tuo compito è creare caption coinvolgenti e visivamente accattivanti per Instagram.

Regole fondamentali:
- Usa linguaggio informale ma professionale
- Massimo 2000 caratteri per caption
- Inizia con un hook che catturi l'attenzione
- Usa emojis strategicamente (massimo 5-7)
- Crea un flusso narrativo che porti all'azione
- Includi una call-to-action chiara
- Usa 15-20 hashtag rilevanti ma non spammy
- Mantieni coerenza con il brand
- Usa linguaggio visivo e descrittivo

Struttura obbligatoria del post:
1) Hook iniziale accattivante (emoji + frase)
2) Corpo del messaggio con valore aggiunto
3) Call-to-action finale
4) Hashtag rilevanti

Evita:
- Linguaggio troppo formale
- Frasi troppo lunghe
- Mancanza di call-to-action
- Hashtag non rilevanti

Esigo controllo ortografico e traduzione 15 volte e applica la correzione.

SETTORE: {sector}""",
            
            'facebook': f"""Sei un esperto di Facebook e social media management.
Il tuo compito è creare post coinvolgenti e ottimizzati per Facebook.

Regole fondamentali:
- Linguaggio chiaro e diretto
- Ottimizzato per algoritmo Facebook
- Include elementi che incoraggiano l'interazione
- Usa un tono adatto al pubblico target
- Incorpora domande per stimolare discussioni
- Usa formati adatti a Facebook (testuali, immagini, video)
- Bilancia informazione e intrattenimento
- Include link quando rilevante
- Usa call-to-action appropriate

Struttura obbligatoria del post:
1) Titolo o frase iniziale accattivante
2) Contenuto principale con valore
3) Elemento interattivo (domanda, invito a commentare)
4) Call-to-action finale

Esigo controllo ortografico e traduzione 15 volte e applica la correzione.

SETTORE: {sector}""",
            
            'youtube': f"""Sei un esperto di YouTube e content creator.
Il tuo compito è creare descrizioni, titoli e testi per video YouTube coinvolgenti e SEO-friendly.

Regole fondamentali:
- Titolo accattivante e SEO-optimized (massimo 60 caratteri)
- Descrizione dettagliata ma scannabile
- Include timestamp quando rilevante
- Ottimizzato per ricerca YouTube
- Linguaggio coinvolgente e diretto
- Include CTA per iscrizione e like
- Usa parole chiave rilevanti
- Include link esterni quando appropriato
- Formatta per massima leggibilità

Struttura obbligatoria del post:
1) Titolo SEO-friendly accattivante
2) Descrizione dettagliata con valore
3) Timestamp (se applicabile)
4) Call-to-action per coinvolgimento

Esigo controllo ortografico e traduzione 15 volte e applica la correzione.

SETTORE: {sector}"""
        }
        
        return prompts.get(platform.lower(), prompts['linkedin'])
    
    def generate_linkedin_post(self, news_item: Dict[str, Any]) -> Optional[str]:
        platform_prompt = self.get_platform_prompt('linkedin')
        
        news_link = news_item.get('link', 'N/A')
        news_title = news_item.get('title', 'N/A')
        news_source = news_item.get('source', 'N/A')
        news_summary = news_item.get('summary', 'N/A')[:500]
        news_published = news_item.get('published', 'N/A')
        
        full_prompt = f"""{platform_prompt}

NOTIZIA ORIGINALE:
- Titolo: {news_title}
- Fonte: {news_source}
- Data pubblicazione: {news_published}
- Link: {news_link}
- Riassunto: {news_summary}

COMPITO:
Crea un post LinkedIn professionale seguendo esattamente lo stile e la struttura indicati nel prompt precedente.
Il post deve essere in italiano perfetto, senza errori grammaticali o di traduzione.
Massimo 2600 caratteri.

FORMATO OUTPUT:
Solo il testo del post, niente spiegazioni aggiuntive."""
        
        return self.generate(full_prompt)
    
    def generate_instagram_caption(self, news_item: Dict[str, Any]) -> Optional[str]:
        platform_prompt = self.get_platform_prompt('instagram')
        
        news_link = news_item.get('link', 'N/A')
        news_title = news_item.get('title', 'N/A')
        news_source = news_item.get('source', 'N/A')
        news_summary = news_item.get('summary', 'N/A')[:300]  # Più corto per IG
        news_published = news_item.get('published', 'N/A')
        
        full_prompt = f"""{platform_prompt}

NOTIZIA ORIGINALE:
- Titolo: {news_title}
- Fonte: {news_source}
- Data pubblicazione: {news_published}
- Link: {news_link}
- Riassunto: {news_summary}

COMPITO:
Crea una caption Instagram coinvolgente seguendo esattamente lo stile e la struttura indicati nel prompt precedente.
La caption deve essere in italiano perfetto, senza errori grammaticali o di traduzione.
Massimo 2000 caratteri.

FORMATO OUTPUT:
Solo il testo della caption, niente spiegazioni aggiuntive."""
        
        return self.generate(full_prompt)
    
    def generate_facebook_post(self, news_item: Dict[str, Any]) -> Optional[str]:
        platform_prompt = self.get_platform_prompt('facebook')
        
        news_link = news_item.get('link', 'N/A')
        news_title = news_item.get('title', 'N/A')
        news_source = news_item.get('source', 'N/A')
        news_summary = news_item.get('summary', 'N/A')[:500]
        news_published = news_item.get('published', 'N/A')
        
        full_prompt = f"""{platform_prompt}

NOTIZIA ORIGINALE:
- Titolo: {news_title}
- Fonte: {news_source}
- Data pubblicazione: {news_published}
- Link: {news_link}
- Riassunto: {news_summary}

COMPITO:
Crea un post Facebook coinvolgente seguendo esattamente lo stile e la struttura indicati nel prompt precedente.
Il post deve essere in italiano perfetto, senza errori grammaticali o di traduzione.
Massimo 2600 caratteri.

FORMATO OUTPUT:
Solo il testo del post, niente spiegazioni aggiuntive."""
        
        return self.generate(full_prompt)
    
    def generate_youtube_description(self, news_item: Dict[str, Any]) -> Optional[str]:
        platform_prompt = self.get_platform_prompt('youtube')
        
        news_link = news_item.get('link', 'N/A')
        news_title = news_item.get('title', 'N/A')
        news_source = news_item.get('source', 'N/A')
        news_summary = news_item.get('summary', 'N/A')[:800]  # Più lungo per YT
        news_published = news_item.get('published', 'N/A')
        
        full_prompt = f"""{platform_prompt}

NOTIZIA ORIGINALE:
- Titolo: {news_title}
- Fonte: {news_source}
- Data pubblicazione: {news_published}
- Link: {news_link}
- Riassunto: {news_summary}

COMPITO:
Crea una descrizione YouTube completa seguendo esattamente lo stile e la struttura indicati nel prompt precedente.
La descrizione deve essere in italiano perfetto, senza errori grammaticali o di traduzione.
Massimo 5000 caratteri.

FORMATO OUTPUT:
Solo il testo della descrizione, niente spiegazioni aggiuntive."""
        
        return self.generate(full_prompt)

    def save_html_article(self, html_content: str, news_item: Dict[str, Any], platform: str = 'linkedin'):
        """Salva l'articolo HTML in un file con nome che indica la piattaforma"""
        # Crea cartella HTML se non esiste
        html_dir = "data/html_articles"
        os.makedirs(html_dir, exist_ok=True)
        
        # Genera nome file sicuro con piattaforma
        safe_title = "".join(c for c in news_item.get('title', 'articolo') if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:50]  # Limita lunghezza
        filename = f"{safe_title}_{platform}_{int(datetime.now().timestamp())}.html"
        filepath = os.path.join(html_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📝 Articolo HTML per {platform} salvato: {filepath}")
        return filepath

# Singletone
ollama = OllamaClient()
