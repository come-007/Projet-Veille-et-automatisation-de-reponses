import streamlit as st
import pandas as pd
from db import init_db, add_keyword, get_keywords, get_recent_alerts, delete_keyword
from monitor import scan_web_for_keywords
from generator import CrisisAgent

# Configuration de la page
st.set_page_config(page_title="Dashboard Crise & Veille", layout="wide")

# Initialisation de la BDD au démarrage
init_db()

# --- SIDEBAR : Paramétrage ---
st.sidebar.title("⚙️ Configuration Veille")
st.sidebar.markdown("Gérez vos mots-clés d'alerte (ex: *Lexia Avocats*, *fuite données*).")

new_keyword = st.sidebar.text_input("Ajouter un mot-clé :")
if st.sidebar.button("Ajouter"):
    if new_keyword:
        if add_keyword(new_keyword):
            st.sidebar.success(f"'{new_keyword}' ajouté !")
        else:
            st.sidebar.warning("Ce mot-clé existe déjà.")

st.sidebar.markdown("### Mots-clés actifs")
active_keywords = get_keywords()
for kw in active_keywords:
    col1, col2 = st.sidebar.columns([4, 1])
    col1.markdown(f"- **{kw}**")
    if col2.button("❌", key=f"del_{kw}", help="Supprimer ce mot-clé"):
        delete_keyword(kw)
        st.rerun() # Rafraîchit l'interface pour faire disparaître le mot-clé

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Lancer un Scan Manuel du Web", type="primary"):
    with st.spinner("Recherche d'actualités en cours (DuckDuckGo)..."):
        if active_keywords:
            summary = scan_web_for_keywords(active_keywords)
            
            # Affichage des erreurs s'il y en a
            if summary["errors"]:
                for err in summary["errors"]:
                    st.sidebar.error(f"Erreur DDG : {err}")
                    
            st.sidebar.success(f"Scan terminé : {summary['found']} article(s) trouvé(s) dont {summary['new']} nouveau(x).")
        else:
            st.sidebar.error("Ajoutez d'abord des mots-clés.")

# --- MAIN CONTENT : Dashboard ---
st.title("🛡️ Dashboard Veille & E-Réputation")
st.markdown("Outil automatisé de communication de crise - **Composante 4**")

alerts = get_recent_alerts()

if not alerts:
    st.info("Aucune alerte pour le moment. Lancez un scan manuel depuis le menu de gauche.")
else:
    # Transformation en DataFrame Pandas pour un affichage propre
    df = pd.DataFrame(alerts)
    # Affichage d'un tableau simplifié
    st.dataframe(
        df[['date', 'keyword', 'source', 'title', 'url']], 
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.subheader("🤖 Agent IA : Générateur de Réponse de Crise")
    
    # Sélection d'une alerte pour générer une réponse
    alert_options = {f"[{a['keyword']}] {a['title']}": a for a in alerts}
    selected_alert_title = st.selectbox("Sélectionnez une alerte à traiter :", options=list(alert_options.keys()))
    
    if st.button("⚡ Générer le plan de communication"):
        selected_alert = alert_options[selected_alert_title]
        agent = CrisisAgent()
        
        with st.spinner("Génération des réponses adaptées par l'Agent IA..."):
            responses = agent.generate_responses(selected_alert)
            
            with st.expander("👁️ Voir le Prompt Systémique utilisé (Back-office)"):
                st.code(responses["prompt_systemique_utilise"], language="text")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("📧 Communication CLIENTS")
                st.write(responses["clients"])
                
            with col2:
                st.warning("📰 Communication PRESSE")
                st.write(responses["presse"])
                
            with col3:
                st.success("💼 Communication LINKEDIN")
                st.write(responses["linkedin"])