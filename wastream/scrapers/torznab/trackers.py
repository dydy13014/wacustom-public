"""Trackers prives — VERSION INSTANCE PUBLIQUE.

Difference fondamentale avec Wacustom self-host : la cle API vient de la
config de l'UTILISATEUR (`get_tracker_api_key`), jamais du .env de
l'hebergeur. Un utilisateur qui n'a pas renseigne un tracker ne le voit
simplement pas dans ses resultats — aucune cle ne lui est pretee. Preter
celle de l'hebergeur ferait porter par un seul compte le trafic de tous les
utilisateurs, ce qui le ferait bannir en quelques jours.

L'URL du tracker, elle, reste cote hebergeur (settings) : elle est la meme
pour tout le monde, seule la cle distingue les comptes.
"""
from typing import List, Dict, Optional

from wastream.config.settings import settings
from wastream.scrapers.torznab.base import BaseTorznab
from wastream.scrapers.unit3d.base import BaseUnit3d
from wastream.utils.helpers import get_tracker_api_key


class _UserKeyTracker:
    """Fabrique commune a tous les trackers a cle utilisateur : seuls le nom,
    la classe de scraper et ses arguments changent d'une sous-classe a l'autre.

    `url_setting` est explicite plutot que deduit de `tracker_id` : les noms
    de reglages historiques ne suivent pas tous la meme convention, mieux vaut
    les nommer que reposer sur une regle qui a des exceptions.
    """

    tracker_id: str = ""
    display_name: str = ""
    url_setting: str = ""
    scraper_class = BaseTorznab
    scraper_kwargs: Dict = {}

    async def search(self, title: str, year: Optional[str] = None, metadata: Optional[Dict] = None,
                     season: Optional[str] = None, episode: Optional[str] = None,
                     config: Optional[Dict] = None) -> List[Dict]:
        url = getattr(settings, self.url_setting, None)
        api_key = get_tracker_api_key(config, self.tracker_id)
        if not api_key or not url:
            return []
        scraper = self.scraper_class(self.display_name, url, api_key, **self.scraper_kwargs)
        return await scraper.search(title, year, metadata, season, episode, config)


# ===========================
# Trackers Torznab
# ===========================
class YggRebornScraper(_UserKeyTracker):
    tracker_id = "yggreborn"
    display_name = "YggReborn"
    url_setting = "YGGREBORN_URL"
    scraper_kwargs = {"auth_type": "query"}


class Tr4kerScraper(_UserKeyTracker):
    tracker_id = "tr4ker"
    display_name = "Tr4ker"
    url_setting = "TR4KER_URL"
    scraper_kwargs = {"auth_type": "query"}


class Torr9Scraper(_UserKeyTracker):
    tracker_id = "torr9"
    display_name = "Torr9"
    url_setting = "TORR9_URL"
    scraper_kwargs = {"auth_type": "query"}


class V3XScraper(_UserKeyTracker):
    tracker_id = "v3x"
    display_name = "V3X"
    url_setting = "V3X_URL"
    scraper_kwargs = {"auth_type": "query"}


class C411Scraper(_UserKeyTracker):
    tracker_id = "c411"
    display_name = "C411"
    url_setting = "C411_URL"
    scraper_kwargs = {"auth_type": "query"}


yggreborn_scraper = YggRebornScraper()
tr4ker_scraper = Tr4kerScraper()
torr9_scraper = Torr9Scraper()
v3x_scraper = V3XScraper()
c411_scraper = C411Scraper()


# ===========================
# Trackers UNIT3D (API JSON native, pas Torznab)
# ===========================
class GeminiScraper(_UserKeyTracker):
    tracker_id = "gemini"
    display_name = "Gemini"
    url_setting = "GEMINI_URL"
    scraper_class = BaseUnit3d


class GenerationFreeScraper(_UserKeyTracker):
    tracker_id = "generationfree"
    display_name = "Generation-Free"
    url_setting = "GENERATIONFREE_URL"
    scraper_class = BaseUnit3d


gemini_scraper = GeminiScraper()
generationfree_scraper = GenerationFreeScraper()
