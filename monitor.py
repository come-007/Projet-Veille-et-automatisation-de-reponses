import logging
import time
from duckduckgo_search import DDGS
from db import save_alert

# Configuration du logging pour anticiper les erreurs en prod
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scan_web_for_keywords(keywords: list[str]) -> dict:
    """
    Scanne les actualités web pour une liste de mots-clés et sauvegarde les résultats.
    Retourne un dictionnaire avec le détail (trouvés, nouveaux, erreurs).
    """
    summary = {"found": 0, "new": 0, "errors": []}
    
    with DDGS() as ddgs:
        for keyword in keywords:
            logging.info(f"Scan en cours pour le mot-clé : {keyword}")
            try:
                # Récupère les 5 dernières actualités pour le mot-clé
                results = ddgs.news(keyword, max_results=5)
                
                if results:
                    summary["found"] += len(results)
                    for article in results:
                        title = article.get('title', 'Titre inconnu')
                        url = article.get('url', '#')
                        source = article.get('source', 'Source inconnue')
                        date = article.get('date', 'Date inconnue')
                        
                        # Tente de sauvegarder en base (ignorera les doublons grâce à l'UNIQUE constraint)
                        if save_alert(keyword, title, url, source, date):
                            summary["new"] += 1
                            
            except Exception as e:
                logging.error(f"Erreur lors du scan pour '{keyword}': {str(e)}")
                # On stocke l'erreur pour l'afficher sur l'interface
                summary["errors"].append(f"{keyword}: {str(e)}")
                
            # Pause de 2 secondes pour éviter le blocage (RateLimit) anti-robot de DuckDuckGo
            time.sleep(2)

    return summary