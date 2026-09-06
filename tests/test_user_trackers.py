"""Tests du modele « instance publique » : les cles de trackers viennent de
l'utilisateur, jamais de l'hebergeur.

Le test le plus important de ce fichier est
`test_scraper_ne_retombe_JAMAIS_sur_la_cle_de_l_hebergeur` : c'est la garantie
qui distingue ce fork de Wacustom self-host. Si elle saute, l'hebergeur se
retrouve a porter le trafic de tous les utilisateurs sur son propre compte
tracker — et se fait bannir.
"""
import json
from base64 import b64encode

import pytest

from wastream.config.settings import settings
from wastream.utils.helpers import get_tracker_api_key
from wastream.utils.validators import validate_config
from wastream.scrapers.torznab.trackers import c411_scraper, tr4ker_scraper


def _encode(config: dict) -> str:
    return b64encode(json.dumps(config).encode("utf-8")).decode("utf-8")


def _base_config(**overrides):
    config = {
        "tmdb_api_token": "abc123",
        "debrid_services": [{"service": "alldebrid", "api_key": "key123"}],
    }
    config.update(overrides)
    return config


# ===========================
# get_tracker_api_key
# ===========================
def test_renvoie_la_cle_de_l_utilisateur():
    config = {"trackers": [{"tracker": "c411", "api_key": "cle-utilisateur"}]}
    assert get_tracker_api_key(config, "c411") == "cle-utilisateur"


def test_renvoie_vide_si_tracker_non_configure():
    config = {"trackers": [{"tracker": "c411", "api_key": "cle"}]}
    assert get_tracker_api_key(config, "tr4ker") == ""


def test_renvoie_vide_si_aucun_tracker():
    assert get_tracker_api_key({}, "c411") == ""
    assert get_tracker_api_key({"trackers": []}, "c411") == ""


def test_renvoie_vide_si_config_absente():
    # Cas reel : certains chemins d'appel passent config=None.
    assert get_tracker_api_key(None, "c411") == ""


def test_distingue_bien_plusieurs_trackers():
    config = {"trackers": [
        {"tracker": "c411", "api_key": "cle-c411"},
        {"tracker": "tr4ker", "api_key": "cle-tr4ker"},
    ]}
    assert get_tracker_api_key(config, "c411") == "cle-c411"
    assert get_tracker_api_key(config, "tr4ker") == "cle-tr4ker"


# ===========================
# Validation de la config utilisateur
# ===========================
def test_config_valide_avec_trackers():
    config = _base_config(trackers=[{"tracker": "c411", "api_key": "cle"}])
    result = validate_config(_encode(config))
    assert result is not None
    assert result["trackers"][0]["tracker"] == "c411"


def test_trackers_absent_est_accepte():
    # Un utilisateur sans compte tracker doit pouvoir utiliser l'addon : il
    # n'aura que les sources sans cle (Wawacity, Movix, Nyaa, Zilean...).
    result = validate_config(_encode(_base_config()))
    assert result is not None
    assert result["trackers"] == []


def test_tracker_inconnu_rejete():
    config = _base_config(trackers=[{"tracker": "tracker-bidon", "api_key": "cle"}])
    assert validate_config(_encode(config)) is None


def test_cle_vide_rejetee():
    config = _base_config(trackers=[{"tracker": "c411", "api_key": ""}])
    assert validate_config(_encode(config)) is None


def test_tous_les_trackers_declares_sont_acceptes():
    for name in settings.USER_TRACKERS:
        config = _base_config(trackers=[{"tracker": name, "api_key": "cle"}])
        assert validate_config(_encode(config)) is not None, f"{name} devrait etre accepte"


# ===========================
# Garantie centrale du fork
# ===========================
async def test_scraper_ne_retombe_JAMAIS_sur_la_cle_de_l_hebergeur(monkeypatch):
    """Meme si l'hebergeur a laisse une cle dans son .env (par exemple parce
    qu'il vient d'un deploiement self-host), un utilisateur qui n'a pas fourni
    la sienne ne doit PAS en beneficier."""
    monkeypatch.setattr(settings, "C411_URL", "https://c411.example", raising=False)
    # Le reglage n'existe plus du tout dans cette version (pydantic refuse
    # meme de le poser) : on force l'attribut en contournant le modele pour
    # simuler une cle residuelle, et on verifie qu'elle n'est jamais lue.
    assert "C411_API_KEY" not in type(settings).model_fields
    object.__setattr__(settings, "C411_API_KEY", "cle-de-l-hebergeur")
    try:
        config_sans_tracker = {"trackers": []}
        resultats = await c411_scraper.search("Un film", "2026", {}, config=config_sans_tracker)
        assert resultats == []
    finally:
        settings.__dict__.pop("C411_API_KEY", None)


async def test_scraper_inactif_si_url_hebergeur_absente(monkeypatch):
    """Symetrique : l'utilisateur a beau fournir sa cle, sans URL cote
    hebergeur le tracker ne peut pas etre interroge."""
    monkeypatch.setattr(settings, "TR4KER_URL", None, raising=False)

    config = {"trackers": [{"tracker": "tr4ker", "api_key": "cle-utilisateur"}]}
    resultats = await tr4ker_scraper.search("Un film", "2026", {}, config=config)
    assert resultats == []
