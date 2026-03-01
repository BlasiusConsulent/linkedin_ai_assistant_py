# 🚀 LinkedIn AI Assistant Pro - HTML Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/AI-Ollama%20Local-green.svg)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Privacy](https://img.shields.io/badge/Privacy-GDPR%20Compliant-brightgreen.svg)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/Version-1.0.0 Pro-orange.svg)]()

**LinkedIn AI Assistant Pro - HTML Generator** è un'applicazione desktop enterprise-grade progettata per automatizzare la creazione di contenuti professionali per social media (LinkedIn, Instagram, Facebook, YouTube) basandosi su notizie IT e Cybersecurity in tempo reale.

Utilizzando **AI Locale (Ollama)**, garantisce la massima privacy dei dati, conformità GDPR e assenza di costi API esterni, mantenendo standard elevati di qualità professionale, legale e tecnica.

---

## 📋 Indice

1. [Panoramica Esecutiva](#-panoramica-esecutiva)
2. [Funzionalità Principali](#-funzionalità-principali)
3. [Sicurezza e Privacy (GDPR)](#-sicurezza-e-privacy-gdpr)
4. [Requisiti di Sistema](#-requisiti-di-sistema)
5. [Installazione e Configurazione](#-installazione-e-configurazione)
6. [Utilizzo Operativo](#-utilizzo-operativo)
7. [Struttura del Progetto](#-struttura-del-progetto)
8. [API e Moduli](#-api-e-moduli)
9. [Note Legali e Disclaimer](#-note-legali-e-disclaimer)
10. [Autore e Contatti](#-autore-e-contatti)

---

## 🌐 Panoramica Esecutiva

Questo strumento è stato sviluppato per **Consulenti ICT, Recruiter e Professionisti del Lavoro** che necessitano di mantenere una presenza digitale autorevole senza compromettere la privacy dei dati o incorrere in costi di abbonamento API.

Il sistema aggrega feed RSS, filtra le notizie per rilevanza (keyword-based), e utilizza modelli di linguaggio locale (LLM) per generare contenuti strutturati, salvando gli output in formati editabili (HTML, DOCX, JSON).

### 🔑 Punti di Forza

| Caratteristica | Descrizione |
| :--- | :--- |
| **🔒 Privacy-First** | Tutte le elaborazioni AI avvengono in locale tramite Ollama |
| **📰 News Aggregation** | Feed RSS multipli con filtraggio intelligente per parole chiave |
| **✍️ Multi-Platform** | Generazione contenuti ottimizzati per LinkedIn, Instagram, Facebook, YouTube |
| **📄 Export Documentale** | Generazione automatica di report Word (.docx) e articoli HTML |
| **🖥️ GUI Nativa** | Interfaccia desktop Tkinter leggera e responsiva |
| **💾 Storage Locale** | Database JSON trasparente e ispezionabile |

---

## ✨ Funzionalità Principali

### 🤖 Intelligenza Artificiale Locale

- **Privacy-First:** Nessun dato viene inviato a server cloud esterni per l'elaborazione AI
- **Modelli Supportati:** Compatibile con tutti i modelli Ollama (Llama3, Mistral, ecc.)
- **Prompt Engineering:** Template specifici per ciascuna piattaforma social
- **Multi-Lingua:** Output in italiano professionale con controllo grammaticale

### 📰 Monitoraggio News Intelligente

- **Aggregazione RSS:** Fonti preconfigurate (The Hacker News, BleepingComputer, Krebs)
- **Filtro Semantico:** Selezione automatica basata su parole chiave personalizzabili
- **Deduplicazione:** Controllo hash per evitare notizie ripetute
- **Relevance Scoring:** Classificazione notizie per pertinenza

### 📄 Documentazione e Export

- **Generazione HTML:** Articoli completi salvati localmente in `data/html_articles/`
- **Report Word:** Aggregazione automatica dei post generati in `linkedin_posts.docx`
- **Storage JSON:** Database locale trasparente e ispezionabile
- **Logging:** Tracciamento operazioni per audit interno

### 🖥️ Interfaccia GUI Professionale

- **Tkinter:** Interfaccia desktop nativa, leggera e responsiva
- **Menu Dinamici:** Selezione modelli AI e gestione notizie
- **Log in Tempo Reale:** Visualizzazione operazioni in corso
- **Notifiche Desktop:** Alert visivi e sonori (Windows) per eventi critici

---

## 🔒 Sicurezza e Privacy (GDPR)

Questo progetto è architetto secondo i principi di **Privacy by Design** e **Privacy by Default**:

### 1. Data Sovereignty
Tutti i dati (news, profili, post generati) risiedono esclusivamente sul disco locale dell'utente nella cartella `/data`.

### 2. No External AI API
L'elaborazione del linguaggio naturale avviene tramite **Ollama in locale**. Non vi è trasferimento di dati personali verso provider AI terzi.

### 3. Trasparenza
Il codice è open-source e ispezionabile. Non sono presenti tracker o telemetria nascosta.

### 4. Controllo Utente
L'utente agisce come **Titolare del Trattamento** (Data Controller) per i dati inseriti nel profilo e nei log.

### 5. Sicurezza del Codice
Utilizzo di librerie validate (`requests`, `feedparser`) e gestione sicura dei path (`pathlib`).

> **⚠️ Nota per il DPO:** In ottica GDPR, si raccomanda di cifrare il disco su cui risiede la cartella `data/` se vengono trattati dati personali sensibili nei profili utente.

### Compliance Checklist

- [x] Elaborazione dati in locale (no cloud)
- [x] Consenso utente per generazione contenuti
- [x] Diritto di accesso ai dati (file JSON ispezionabili)
- [x] Diritto alla cancellazione (eliminazione file locale)
- [x] Minimizzazione dati (solo informazioni necessarie)
- [x] Sicurezza tecnica (path sanitization, error handling)

---

## 🛠️ Requisiti di Sistema

Prima di procedere, verificare i seguenti prerequisiti tecnici:

| Componente | Versione Minima | Note |
| :--- | :--- | :--- |
| **Python** | 3.8+ | Ambiente 64-bit consigliato |
| **Ollama** | Latest | Deve essere in esecuzione in background |
| **Modello AI** | N/A | Scaricare tramite `ollama pull llama3` |
| **Sistema Operativo** | Windows 10/11 | Ottimizzato per notifiche Windows |
| **Node.js** | 18+ | Opzionale, solo per script utility |
| **RAM** | 8GB+ | Consigliato per modelli AI locali |
| **Storage** | 2GB+ | Per modelli Ollama e dati locali |

---

## 📥 Installazione e Configurazione

### 1. Clonazione del Repository

```bash
git clone https://github.com/tuo-username/blasiusconsulent-linkedin_ai_assistant_py.git
cd blasiusconsulent-linkedin_ai_assistant_py
```

### 2. Ambiente Virtuale (Best Practice)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Installazione Dipendenze

```bash
pip install -r requirements.txt
```

> **⚠️ Importante:** Il modulo `database.py` richiede `python-docx` per la generazione dei report Word. Installarlo manualmente:
>
> ```bash
> pip install python-docx
> ```

### 4. Configurazione Ollama

Assicurarsi che Ollama sia installato e attivo. Scaricare un modello consigliato:

```bash
# Avvia il servizio Ollama
ollama serve

# In un altro terminale, scarica il modello
ollama pull llama3.2:latest
```

### 5. Configurazione Applicazione

Il file `config.json` viene generato automaticamente al primo avvio. Per personalizzarlo:

```json
{
  "ollama": {
    "base_url": "http://localhost:11434",
    "model": "llama3.2:latest",
    "timeout": 300
  },
  "news_sources": [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/"
  ],
  "keywords": [
    "cybersecurity", "AI", "IT", "job", "recruiter",
    "Campania", "Napoli", "Salerno"
  ],
  "user_profile": {
    "name": "Biagio Apostolico",
    "role": "Senior ICT Consultant",
    "location": "Campania, Italia",
    "specializations": ["CyberSecurity", "Infrastructure", "AI", "HelpDesk L3"]
  }
}
```

---

## 🚀 Utilizzo Operativo

### 1. Avvio Applicazione

```bash
python main.py
```

### 2. Verifica Connessione

Controllare che l'indicatore di stato in GUI mostri **🟢 Connesso**.

### 3. Aggiornamento News

Cliccare su **🔄 Aggiorna News** per scaricare i feed RSS.

### 4. Generazione Contenuti

1. Selezionare una notizia dalla lista
2. Cliccare su **📝 Genera HTML** per creare l'articolo
3. Il post verrà salvato in `data/html_articles/` e aggiunto al report Word

### 5. Gestione Modelli

Usare il menu **Modello** per switchare tra diversi LLM locali senza riavviare l'app.

### 6. Export Documentale

I post generati vengono automaticamente aggregati in:
- `data/linkedin_posts.docx` - Report Word
- `data/html_articles/*.html` - Articoli HTML
- `data/*.txt` - Database JSON locale

---

## 📂 Struttura del Progetto

```
blasiusconsulent-linkedin_ai_assistant_py/
├── main.py                 # Entry point GUI (Tkinter)
├── config.py               # Gestione configurazione (Singleton Pattern)
├── config.json             # Configurazione utente
├── ollama_client.py        # Wrapper API per Ollama Locale
├── news_monitor.py         # Logica RSS Feed e Filtraggio
├── content_generator.py    # Prompt Engineering e Generazione Contenuti
├── database.py             # Persistenza JSON e Export DOCX
├── alert_system.py         # Notifiche Desktop (Windows)
├── requirements.txt        # Dipendenze Python
├── fix.mjs                 # Utility script per correzioni codice
├── generate-readme.mjs     # Script autogenerazione README
└── data/                   # Directory dati (GitIgnored)
    ├── html_articles/      # Output articoli HTML
    ├── linkedin_posts.docx # Report aggregato
    └── *.txt               # Database locale (News, Posts, Alerts)
```

---

## 🔌 API e Moduli

### Moduli Principali

| Modulo | Responsabilità | Dipendenze |
| :--- | :--- | :--- |
| **`main.py`** | GUI Tkinter, gestione eventi | tkinter, threading |
| **`config.py`** | Configurazione Singleton | json, pathlib |
| **`ollama_client.py`** | API Ollama, generazione contenuti | requests |
| **`news_monitor.py`** | RSS Feed, filtraggio keyword | feedparser |
| **`content_generator.py`** | Prompt engineering, export | ollama_client |
| **`database.py`** | Storage JSON, export DOCX | json, python-docx |
| **`alert_system.py`** | Notifiche desktop | plyer, winsound |

### Endpoint Ollama Utilizzati

| Endpoint | Metodo | Scopo |
| :--- | :--- | :--- |
| `/api/tags` | GET | Lista modelli disponibili |
| `/api/generate` | POST | Generazione contenuti AI |

### Funzioni Core

```python
# Generazione post LinkedIn
ollama.generate_linkedin_post(news_item)

# Generazione caption Instagram
ollama.generate_instagram_caption(news_item)

# Generazione post Facebook
ollama.generate_facebook_post(news_item)

# Generazione descrizione YouTube
ollama.generate_youtube_description(news_item)

# Salvataggio articolo HTML
ollama.save_html_article(html_content, news_item, platform)
```

---

## ⚖️ Note Legali e Disclaimer

### 1. Accuratezza dei Contenuti (AI Hallucination)

Sebbene i prompt siano ingegnerizzati per verificare i fatti, i modelli di linguaggio (LLM) possono commettere errori. **È responsabilità esclusiva dell'utente verificare ogni dato, numero o affermazione prima della pubblicazione.** L'autore del software non si assume responsabilità per danni derivanti da informazioni inesatte generate dall'AI.

### 2. Diritto d'Autore e News

Le notizie sono aggregate da feed RSS pubblici. L'utente deve rispettare i termini di servizio delle fonti originali e citare sempre la provenienza quando si condividono i contenuti generati. Questo strumento facilita la sintesi, non la redistribuzione integrale di contenuti protetti.

### 3. Utilizzo Professionale

Questo software è uno strumento di supporto alla decisione e alla creazione di bozze. Non sostituisce il parere di un consulente del lavoro, un avvocato o un esperto di cybersecurity umano.

### 4. Licenza

Il codice è distribuito sotto licenza **MIT**. Vedi il file [LICENSE](LICENSE) per i dettagli. L'utente è libero di modificare e distribuire il codice, mantenendo l'attribuzione originale.

### 5. Responsabilità Limitata

IL SOFTWARE È FORNITO "COSÌ COM'È", SENZA GARANZIE DI ALCUN TIPO, ESPLICITE O IMPLICITE. GLI AUTORI NON SONO RESPONSABILI PER DANNI DIRETTI, INDIRETTI, INCIDENTALI O CONSEGUENTI DERIVANTI DALL'USO DEL SOFTWARE.

---

## 🤝 Autore e Contatti

Sviluppato con standard di eccellenza professionale da:

### **Biagio Apostolico**
*Senior ICT Consultant | CyberSecurity & AI Specialist*

| Contatto | Dettaglio |
| :--- | :--- |
| **📍 Location** | Campania, Italia |
| **📧 Email** | b.apostolico@libero.it |
| **💼 LinkedIn** | [Profilo LinkedIn](https://www.linkedin.com/in/biagio-apostolico/) |

---

## 🐛 Troubleshooting

| Problema | Soluzione |
| :--- | :--- |
| **Ollama Non Connesso** | Verificare che il servizio `ollama serve` sia attivo. Controllare il firewall. |
| **Errore Word (DOCX)** | Eseguire `pip install python-docx`. Riavviare l'app. |
| **Notifiche Non Funzionano** | `alert_system.py` usa `winsound`. Funziona nativamente su Windows. Su Linux/Mac richiede librerie aggiuntive. |
| **Metodi Obsoleti** | Eseguire `node fix.mjs` se si riscontrano errori di chiamata nei generatori di contenuto. |
| **Modelli Non Visibili** | Eseguire `ollama pull llama3.2:latest` per scaricare un modello. |
| **Errori di Encoding** | Verificare che tutti i file siano salvati in UTF-8. |

---

## 📄 Licenza

Questo progetto è distribuito sotto licenza **MIT**.

```
Copyright (c) 2026 Biagio Apostolico

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Ringraziamenti

- **Ollama Team** - Per la piattaforma AI locale open-source
- **Python Community** - Per le librerie utilizzate
- **Fonti News** - The Hacker News, BleepingComputer, Krebs on Security

---

*Ultimo aggiornamento: 2026-03-01*  
*Versione: 1.0.0 Pro*  
*Compliance: GDPR Ready / Local AI / Secure Coding*

---

> **💡 Suggerimento:** Per aggiornamenti futuri del README, eseguire:
> ```bash
> node generate-readme.mjs
> ```
