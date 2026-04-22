import sqlite3
import os
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), 'alerts.db')

def get_connection():
    """Initialise et retourne la connexion SQLite."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crée les tables nécessaires si elles n'existent pas."""
    conn = get_connection()
    cursor = conn.cursor()
    # Table pour stocker les mots-clés surveillés
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE NOT NULL
        )
    ''')
    # Table pour stocker les alertes remontées
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            source TEXT,
            date TEXT,
            UNIQUE(url)
        )
    ''')
    conn.commit()
    conn.close()

def add_keyword(word: str) -> bool:
    """Ajoute un mot-clé à surveiller."""
    conn = get_connection()
    try:
        conn.execute('INSERT INTO keywords (word) VALUES (?)', (word.strip(),))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_keywords() -> List[str]:
    """Récupère la liste des mots-clés."""
    conn = get_connection()
    cursor = conn.execute('SELECT word FROM keywords')
    words = [row['word'] for row in cursor.fetchall()]
    conn.close()
    return words

def delete_keyword(word: str) -> bool:
    """Supprime un mot-clé de la base de données."""
    conn = get_connection()
    try:
        conn.execute('DELETE FROM keywords WHERE word = ?', (word,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def save_alert(keyword: str, title: str, url: str, source: str, date: str) -> bool:
    """Sauvegarde une nouvelle alerte si elle n'existe pas déjà (basé sur l'URL)."""
    conn = get_connection()
    try:
        conn.execute(
            'INSERT INTO alerts (keyword, title, url, source, date) VALUES (?, ?, ?, ?, ?)',
            (keyword, title, url, source, date)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # L'alerte existe déjà
    finally:
        conn.close()

def get_recent_alerts(limit: int = 50) -> List[Dict[str, Any]]:
    """Récupère les alertes les plus récentes."""
    conn = get_connection()
    cursor = conn.execute('SELECT * FROM alerts ORDER BY id DESC LIMIT ?', (limit,))
    alerts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return alerts