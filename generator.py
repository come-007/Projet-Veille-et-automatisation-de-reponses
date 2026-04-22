class CrisisAgent:
    def __init__(self):
        # Le prompt systémique tel que demandé par la composante 4
        self.system_prompt = """
        Tu es l'agent de communication de crise de "Lexia Avocats" (ou du cabinet concerné).
        Ton objectif est de rédiger des communications en cas d'alerte e-réputation ou de crise (ex: fuite de données, hallucination IA).
        
        Règles strictes :
        1. Ton de la communication : Professionnel, rassurant, transparent et juridiquement prudent.
        2. Format : Fournir 3 déclinaisons de la réponse :
           - [CLIENTS] : Un email direct, empathique, détaillant les actions prises.
           - [PRESSE] : Un communiqué concis, factuel, limitant les spéculations.
           - [LINKEDIN] : Un post institutionnel, orienté résolution de problème et transparence.
        3. Contraintes : Ne jamais admettre une responsabilité pénale de manière prématurée. Toujours insister sur l'investigation en cours.
        """

    def generate_responses(self, alert: dict) -> dict:
        """
        Pour la DÉMO : Génère des réponses basées sur des templates métier ultra-réalistes.
        En production, c'est ici que l'on injecterait le `self.system_prompt` vers une API (Ollama/OpenAI).
        """
        title = alert.get('title', 'Titre inconnu')
        source = alert.get('source', 'Source inconnue')
        keyword = alert.get('keyword', 'Mot-clé')
        url = alert.get('url', '#')
        
        # Création de réponses 100% dynamiques et adaptées à l'alerte sélectionnée
        clients_text = f"Objet : Information importante concernant Lexia Avocats - Veille '{keyword}'\n\nChère/Cher client(e),\n\nNous avons pris connaissance d'une information récente parue dans {source} intitulée « {title} ».\n\nLa sécurité, la confidentialité de vos dossiers et notre réputation sont nos priorités absolues. Nos équipes sont actuellement mobilisées pour analyser cette situation. Aucun impact direct n'est confirmé à ce stade.\n\nNous vous tiendrons informés sous 24h de l'évolution de la situation."
        
        presse_text = f"COMMUNIQUÉ DE PRESSE\n\nParis, le [DATE].\n\nLe cabinet Lexia Avocats prend acte de la publication récente dans {source} concernant : « {title} ».\n\nUne analyse interne indépendante a été immédiatement déclenchée pour établir les faits avec précision. Le cabinet continue d'opérer normalement et communiquera de manière transparente dès que les conclusions seront connues.\n\nAucun autre commentaire ne sera fait à ce stade."
        
        linkedin_text = f"Transparence et rigueur sont les piliers de notre profession.\n\nFace à la récente publication de {source} (« {title} »), nous tenons à rassurer nos partenaires : une investigation rigoureuse est en cours au sein de Lexia Avocats. Nous avons activé notre cellule de veille et de crise.\n\nLien vers l'article concerné pour contexte : {url}\n\nNous restons engagés à maintenir les plus hauts standards. #LexiaAvocats #Communication #Veille"

        return {
            "prompt_systemique_utilise": self.system_prompt,
            "clients": clients_text,
            "presse": presse_text,
            "linkedin": linkedin_text
        }