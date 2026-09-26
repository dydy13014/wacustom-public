"""Historique des versions de Wacustom.

Numérotation propre au fork, indépendante de celle de WAStream (cf.
`WACUSTOM_VERSION` / `WASTREAM_BASE_VERSION` dans settings.py). Nouvelle entrée
en tête de liste à chaque version : c'est ce que la page /configure affiche
quand on clique sur le numéro de version.

Rédigé pour être lu par un utilisateur, pas par un développeur : dire ce que ça
change à l'usage, pas le détail d'implémentation.
"""

CHANGELOG = [
    {
        "version": "1.4.0",
        "date": "2026-09-26",
        "changes": [
            "AIOSources et Lumio ne remontaient plus aucun résultat depuis un moment, à cause d'un bug silencieux dans la transmission de l'identifiant IMDB aux sources — corrigé, ces deux sources fonctionnent de nouveau normalement",
            "Recherche plus précise sur les trackers à clé (Tr4ker, C411, Torr9, YggReborn, V3X) : la correspondance se fait désormais par identifiant exact (IMDB/TMDB/TheTVDB) plutôt que par simple recherche de mots-clés, ce qui réduit les faux résultats sur les titres ambigus — chaque tracker est sondé automatiquement pour savoir quel identifiant il accepte, sans réglage à faire",
            "Zilean : passage à son vrai système de recherche (identique à celui des autres trackers) — la taille des fichiers, qui s'affichait comme \"Inconnu\" sur tous les résultats, est désormais correcte, et la recherche se fait aussi par identifiant IMDB exact",
            "Nombre de sources (seeders) et de leechers désormais affiché sur les résultats torrent quand l'information est disponible (trackers à clé, Nyaa), utile pour choisir la source la plus rapide",
            "Nyaa : badges \"Trusted\" et \"Remake\" affichés sur les résultats, quand le tracker les signale comme tels",
            "Correction : les animes cherchés normalement dans Stremio (hors catalogue \"Anime\" dédié) ne recevaient jamais de résultats Nyaa — Nyaa ne cherchait que dans sa catégorie dramas/variétés pour ce type de recherche, jamais dans sa catégorie Anime",
            "Correction : le logo affiché par Stremio à l'installation de l'addon était encore celui de WAStream (projet d'origine) au lieu du logo Wacustom",
            "Correction : la description de l'addon (visible à l'installation dans Stremio) ne mentionnait que le DDL, alors que Wacustom gère aussi les torrents",
        ],
    },
    {
        "version": "1.3.0",
        "date": "2026-09-16",
        "changes": [
            "Nouvelle source disponible : AIOSources (agrégateur communautaire C411/Tr4ker/TsukiHime/Nostradamus/TheOldSchool, projet tiers maintenu par Théo [TB]) — réglée une seule fois par l'hébergeur, comme Zilean ou Nyaa : aucune clé à renseigner pour en profiter",
        ],
    },
    {
        "version": "1.2.0",
        "date": "2026-09-09",
        "changes": [
            "Nouvelle identité visuelle : dégradé cyan/indigo et nouveau logo, sur la page de configuration, la connexion admin et le tableau de bord (merci à razeN pour le logo !)",
            "Wacustom repart de la base WAStream 3.9.1 (le fork suivait jusqu'ici la 3.8.2)",
            "Fiabilité Idrix : délai entre les requêtes allongé pour réduire les erreurs, meilleure détection des vraies pages de contenu",
            "Meilleure compatibilité des sources : repli automatique www/non-www lors de la synchronisation des domaines, en-têtes de requête plus cohérents",
            "AllDebrid : sélection plus fiable du lien à débrider quand plusieurs choix sont proposés, et distinction entre un lien réellement mort et une simple erreur temporaire du service",
        ],
    },
    {
        "version": "1.1.0",
        "date": "2026-08-21",
        "changes": [
            "Nouvelle option Réglages : prioriser les résultats en VF/Multi (doublage français) avant les résultats VOSTFR, parmi les résultats français",
        ],
    },
    {
        "version": "1.0.0",
        "date": "2026-08-16",
        "changes": [
            "Wacustom repart de la base WAStream 3.8.2 (le fork suivait jusqu'ici la 3.6.3)",
            "Wacustom a désormais sa propre identité : logo, numéro de version distinct de celui de WAStream, et liens vers Wacustom, WAStream et le Discord",
            "Interface revue : navigation par onglets, palette unifiée entre la page de configuration, la connexion et le tableau de bord",
            "Cliquer sur le numéro de version affiche les nouveautés (ce changelog)",
            "Nouvel onglet Réglages : les sources et leurs clés API se configurent depuis le tableau de bord, sans éditer de fichier",
            "Clés API des trackers (Tr4ker, C411, Torr9, YggReborn, V3X, Gemini, Generation-Free) configurables depuis l'interface, stockées chiffrées",
            "Onglet Sauvegarde : export et import complets des données",
            "Nouveau tracker disponible : V3X, comme les autres il ne s'active qu'en renseignant sa propre clé",
            "Nouvelle source Lumio : chacun peut renseigner son propre manifest Lumio (torrents déjà vérifiés en cache debrid), au même titre qu'une clé de tracker",
            "Nouvelles options disponibles, désactivées par défaut : source Zone-Telechargement, collecteur Idrix, et suivi automatique des changements de domaine des sites sources",
            "Animés : un fichier nommé « S3 - 07 » n'est plus pris pour la saison 3 entière, il ne correspond plus qu'à l'épisode 7 (les mauvais épisodes n'apparaissent plus dans la liste)",
            "Animés : les lots d'épisodes (« 1017-1024 ») sont désormais reconnus sur toute leur plage, et une année ou un codec dans le nom ne passe plus pour un numéro d'épisode",
            "Fiabilité : un hébergeur AllDebrid renvoyant des informations incomplètes ne fait plus disparaître le statut des autres (moins de sources marquées indisponibles à tort)",
        ],
    },
]
