# 🛡️ CrisisWatch : Dashboard de Veille & Aide à la Réponse

Projet réalisé dans le cadre du projet Legal Innovation Area de l'EFREI.
L'objectif est de démontrer qu'on peut automatiser la gestion de crise avec des outils simples, souverains et efficaces.

## 🚀 Le Concept
Ce dashboard permet aux cabinets (ex: Lexia Avocats) de surveiller leur e-réputation et de réagir en quelques secondes face à un incident (fuite de données, hallucination IA, etc.).

## ✨ Fonctionnalités
* **Veille Automatisée** : Scan en temps réel du web via DuckDuckGo News (pas besoin de clés API payantes).
* **Gestion des Alertes** : Système CRUD pour ajouter/supprimer des mots-clés stratégiques.
* **Agent IA de Crise** : Génération instantanée de plans de communication multicanaux (Emails clients, Communiqués de presse, Posts LinkedIn).
* **Souveraineté des données** : 
    * Base de données **SQLite** locale.
    * **Zéro Google Workspace** (pas de Sheets/Drive).
    * Interface ultra-rapide via **Streamlit**.

## 🛠️ Stack Technique
* **Langage** : Python 3.x
* **Interface** : Streamlit
* **Recherche** : DuckDuckGo Search API (Libre)
* **Base de données** : SQLite3

## 📦 Installation & Lancement

1. **Cloner le repo** :
   ```bash
   git clone [https://github.com/ton-username/crisis-watch.git](https://github.com/ton-username/crisis-watch.git)
   cd crisis-watch
