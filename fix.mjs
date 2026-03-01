#!/usr/bin/env node

/**
 * 🛠️ FIX AUTOMATICO per metodo mancante
 * Aggiorna content_generator.py per usare il nuovo metodo corretto
 */

import { readFile, writeFile, access, constants } from 'fs/promises';
import { join } from 'path';

const PROJECT_DIR = process.cwd();
const FILE_PATH = join(PROJECT_DIR, 'content_generator.py');

async function main() {
  console.log("🔧 FIX AUTOMATICO - Correzione metodo mancante...");
  console.log("");

  try {
    // Leggi il contenuto
    const content = await readFile(FILE_PATH, 'utf-8');
    
    // Aggiorna il metodo mancante
    const updatedContent = content.replace(
      /html_content = self\.ollama\.generate_html_news_article\(news_item\)/g,
      'html_content = self.ollama.generate_linkedin_post(news_item)'
    ).replace(
      /filepath = self\.ollama\.save_html_article\(html_content, news_item\)/g,
      'filepath = self.ollama.save_html_article(html_content, news_item, "linkedin")'
    );

    // Salva il file aggiornato
    await writeFile(FILE_PATH, updatedContent, 'utf-8');
    
    console.log('✅ METODO CORRETTO!');
    console.log(`   File aggiornato: ${FILE_PATH}`);
    console.log(`   → Metodo corretto: generate_linkedin_post al posto di generate_html_news_article`);
    console.log(`   → Parametro aggiunto: "linkedin" per save_html_article`);
    console.log('');
    console.log('👉 Ora i post dovrebbero generarsi correttamente.');
    console.log('   Riavvia l\'applicazione: py main.py');
    
  } catch (error) {
    if (error.code === 'ENOENT') {
      console.error('❌ File non trovato:', FILE_PATH);
      console.error('   Assicurati di essere nella cartella giusta');
    } else {
      console.error('❌ Errore durante la correzione:', error.message);
    }
  }
}

// Esegui
main().catch(console.error);