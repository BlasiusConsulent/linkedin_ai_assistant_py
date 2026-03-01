"""
LinkedIn AI Assistant - Main Application
Windows Desktop GUI with Tkinter
Now generates HTML articles
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from datetime import datetime
import threading
import time
import webbrowser

from config import config
from ollama_client import ollama
from news_monitor import news_monitor
from content_generator import content_generator
from alert_system import alert_system
from database import get_news, get_posts, get_unread_alerts, save_news

class LinkedInAIAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 LinkedIn AI Assistant Pro - HTML Generator")
        self.root.geometry("1200x800")
        
        self.running = False
        
        self._setup_styles()
        self._create_menu_bar()
        self._create_ui()
        self._check_ollama_status()
        self._load_available_models()
        self._load_news_table()  # Carica le notizie nella tabella
    
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#0066CC')
        style.configure('Success.TLabel', foreground='#28A745')
        style.configure('Error.TLabel', foreground='#DC3545')
    
    def _create_menu_bar(self):
        """Crea la barra del menu con selezione modello e gestione notizie"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Modello
        model_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modello", menu=model_menu)
        
        self.model_var = tk.StringVar(value="Caricamento...")
        self.model_dropdown = tk.Menu(model_menu, tearoff=0)
        
        model_menu.add_cascade(label="Seleziona Modello", menu=self.model_dropdown)
        model_menu.add_separator()
        model_menu.add_command(label="Aggiorna Lista", command=self._load_available_models)
        
        # Menu Notizie
        news_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Notizie", menu=news_menu)
        
        news_menu.add_command(label="Visualizza Notizie", command=self._open_news_window)
        news_menu.add_command(label="Aggiorna Notizie", command=self._refresh_news)
        news_menu.add_command(label="Cerca Notizie...", command=self._search_news_dialog)
        
        # Menu HTML
        html_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="HTML", menu=html_menu)
        html_menu.add_command(label="Genera Articolo HTML", command=self._generate_html_post)
        html_menu.add_command(label="Apri Cartella HTML", command=self._open_html_folder)
    
    def _load_available_models(self):
        """Carica i modelli disponibili da Ollama e popola la tendina"""
        if not ollama.check_connection():
            messagebox.showwarning("Attenzione", "Ollama non è in esecuzione. Avvia Ollama per caricare i modelli.")
            return
        
        self._log("🔄 Caricamento modelli Ollama...", 'info')
        
        def load_models_internal():
            models = ollama.list_models()
            self.root.after(0, lambda: self._update_model_menu(models))
        
        threading.Thread(target=load_models_internal, daemon=True).start()
    
    def _update_model_menu(self, models):
        """Aggiorna la tendina con i modelli disponibili"""
        self.model_dropdown.delete(0, 'end')
        
        if not models:
            self.model_dropdown.add_command(label="Nessun modello trovato", state='disabled')
            self._log("⚠️ Nessun modello trovato in Ollama", 'warning')
            return
        
        for model in models:
            self.model_dropdown.add_command(
                label=model,
                command=lambda m=model: self._select_model(m)
            )
        
        current_model = ollama.model
        self.model_var.set(current_model)
        self._log(f"✅ {len(models)} modelli caricati. Corrente: {current_model}", 'success')
    
    def _select_model(self, model_name):
        """Seleziona un modello dall'interfaccia"""
        old_model = ollama.model
        ollama.set_model(model_name)
        
        self.model_var.set(model_name)
        self._log(f"🔄 Modello cambiato da '{old_model}' a '{model_name}'", 'info')
    
    def _create_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(header_frame, text="🚀 LinkedIn AI Assistant Pro - HTML Generator", style='Title.TLabel').pack(side='left')
        
        model_frame = ttk.Frame(header_frame)
        model_frame.pack(side='right')
        ttk.Label(model_frame, text="Modello: ").pack(side='left')
        self.model_label = ttk.Label(model_frame, textvariable=self.model_var)
        self.model_label.pack(side='left')
        
        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Stato", padding="10")
        status_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.ollama_status = ttk.Label(status_frame, text="⚪ Verifica...")
        self.ollama_status.grid(row=0, column=0)
        
        # Controls
        control_frame = ttk.LabelFrame(main_frame, text="Controlli", padding="10")
        control_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        
        ttk.Button(control_frame, text="🔄 Aggiorna News", command=self._refresh_news).pack(pady=5)
        ttk.Button(control_frame, text="🔍 Visualizza News", command=self._open_news_window).pack(pady=5)
        ttk.Button(control_frame, text="📝 Genera HTML", command=self._generate_html_post).pack(pady=5)
        
        # Log
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15)
        self.log_text.grid(row=3, column=0, sticky="nsew")
        
        self._log("🚀 Assistant avviato - Modalità HTML", 'success')
    
    def _load_news_table(self):
        """Carica le notizie per la visualizzazione"""
        all_news = get_news()
        self._log(f"📊 Caricate {len(all_news)} notizie dal database", 'info')
    
    def _open_news_window(self):
        """Apre la finestra con tutte le notizie"""
        news_win = tk.Toplevel(self.root)
        news_win.title("📰 Notizie Disponibili")
        news_win.geometry("1000x600")
        
        # Frame per ricerca
        search_frame = ttk.Frame(news_win)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(search_frame, text="Cerca:").pack(side='left', padx=(0, 5))
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=(0, 5))
        
        def search_news_internal():
            query = search_entry.get()
            results = news_monitor.search_news(query=query)
            _update_news_display_internal(results)
        
        ttk.Button(search_frame, text="Cerca", command=search_news_internal).pack(side='left')
        ttk.Button(search_frame, text="Tutte", command=lambda: _update_news_display_internal(get_news().values())).pack(side='left', padx=(5, 0))
        
        # Treeview per le notizie
        tree_frame = ttk.Frame(news_win)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('Titolo', 'Fonte', 'Data', 'Link')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('Titolo', text='Titolo')
        tree.heading('Fonte', text='Fonte')
        tree.heading('Data', text='Data')
        tree.heading('Link', text='Link')
        
        tree.column('Titolo', width=400)
        tree.column('Fonte', width=150)
        tree.column('Data', width=120)
        tree.column('Link', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        def _update_news_display_internal(news_list):
            # Pulisci la tabella
            for item in tree.get_children():
                tree.delete(item)
            
            # Aggiungi le notizie
            for news in news_list:
                title = news.get('title', '')[:60] + '...' if len(news.get('title', '')) > 60 else news.get('title', '')
                source = news.get('source', 'N/A')
                date = news.get('published', 'N/A')[:10]  # Solo data, non ora
                link = news.get('link', 'N/A')
                
                tree.insert('', 'end', values=(title, source, date, link), tags=(news['id'],))
        
        # Carica tutte le notizie
        _update_news_display_internal(get_news().values())
        
        # Doppio click per vedere dettagli
        def on_double_click_internal(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                news_id = item['tags'][0] if item['tags'] else None
                
                if news_id:
                    all_news = get_news()
                    if news_id in all_news:
                        news_detail = all_news[news_id]
                        detail_text = f"""
Titolo: {news_detail.get('title', 'N/A')}
Fonte: {news_detail.get('source', 'N/A')}
Link: {news_detail.get('link', 'N/A')}
Data: {news_detail.get('published', 'N/A')}
Riassunto: {news_detail.get('summary', 'N/A')}

Vuoi generare un articolo HTML da questa notizia?
"""
                        result = messagebox.askyesno("Dettagli Notizia", detail_text)
                        if result:
                            # Chiedi conferma per generare articolo HTML
                            confirm = messagebox.askyesno("Conferma", f"Vuoi generare un articolo HTML da questa notizia?\n\n{news_detail.get('title', 'N/A')[:50]}...")
                            if confirm:
                                self._generate_html_from_news(news_detail)
        
        tree.bind('<Double-1>', on_double_click_internal)
    
    def _search_news_dialog(self):
        """Dialog per ricerca avanzata notizie"""
        query = simpledialog.askstring("Cerca Notizie", "Inserisci parole chiave:")
        if query:
            results = news_monitor.search_news(query=query)
            messagebox.showinfo("Risultati Ricerca", f"Trovate {len(results)} notizie corrispondenti.")
    
    def _generate_html_from_news(self, news_item):
        """Genera articolo HTML da una specifica notizia"""
        if not ollama.check_connection():
            messagebox.showwarning("Attenzione", "Ollama non è connesso")
            return
        
        def generate_internal():
            filepath = content_generator.generate_html_from_news(news_item)
            if filepath:
                self.root.after(0, lambda: self._log(f"✅ Articolo HTML generato: {filepath}", 'success'))
            else:
                self.root.after(0, lambda: self._log("⚠️ Nessun articolo HTML generato", 'warning'))
        
        threading.Thread(target=generate_internal, daemon=True).start()
    
    def _generate_html_post(self):
        if not ollama.check_connection():
            messagebox.showwarning("Attenzione", "Ollama non è connesso")
            return
        
        self._log("📝 Generazione articolo HTML...", 'info')
        
        def generate_internal():
            files = content_generator.generate_daily_html_content()
            if files:
                self.root.after(0, lambda: self._log(f"✅ {len(files)} articoli HTML generati", 'success'))
                self.root.after(0, lambda: self._log(f"File: {', '.join([f.split('/')[-1] for f in files])}", 'info'))
            else:
                self.root.after(0, lambda: self._log("⚠️ Nessun contenuto HTML generato", 'warning'))
        
        threading.Thread(target=generate_internal, daemon=True).start()
    
    def _open_html_folder(self):
        """Apre la cartella degli articoli HTML"""
        import os
        html_dir = "data/html_articles"
        os.makedirs(html_dir, exist_ok=True)
        webbrowser.open(f"file://{os.path.abspath(html_dir)}")
    
    def _check_ollama_status(self):
        if ollama.check_connection():
            self.ollama_status.configure(text="🟢 Connesso", style='Success.TLabel')
        else:
            self.ollama_status.configure(text="🔴 Non Connesso", style='Error.TLabel')
            self._log("⚠️ Ollama non rilevato", 'error')
    
    def _refresh_news(self):
        self._log("📰 Aggiornamento news...", 'info')
        
        def fetch_internal():
            items = news_monitor.fetch_all()
            self.root.after(0, lambda: self._log(f"✅ {len(items)} news trovate", 'success'))
            # Ricarica la tabella delle notizie
            self.root.after(0, self._load_news_table)
        
        threading.Thread(target=fetch_internal, daemon=True).start()
    
    def _log(self, message: str, level: str = 'info'):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LinkedInAIAssistant()
    app.run()