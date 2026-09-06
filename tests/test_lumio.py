"""Tests du manifest Lumio personnel (instance publique) : meme garantie que
les trackers prives — aucun repli sur un identifiant partage par
l'hebergeur, chaque utilisateur apporte le sien ou la source est ignoree
pour lui."""
from wastream.utils.helpers import get_lumio_manifest_id
from wastream.utils.validators import UserConfig


# ===========================
# get_lumio_manifest_id
# ===========================
def test_renvoie_l_identifiant_brut():
    config = {"lumio_manifest_id": "ExempleLumio"}
    assert get_lumio_manifest_id(config) == "ExempleLumio"


def test_extrait_l_identifiant_d_une_url_complete():
    config = {"lumio_manifest_id": "https://mylumio.tv/ExempleLumio/manifest.json"}
    assert get_lumio_manifest_id(config) == "ExempleLumio"


def test_extrait_l_identifiant_d_une_url_sans_manifest_json():
    config = {"lumio_manifest_id": "https://mylumio.tv/ExempleLumio/"}
    assert get_lumio_manifest_id(config) == "ExempleLumio"


def test_renvoie_vide_si_non_configure():
    assert get_lumio_manifest_id({}) == ""
    assert get_lumio_manifest_id({"lumio_manifest_id": ""}) == ""


def test_renvoie_vide_si_config_absente():
    assert get_lumio_manifest_id(None) == ""


def test_ignore_les_espaces():
    config = {"lumio_manifest_id": "  ExempleLumio  "}
    assert get_lumio_manifest_id(config) == "ExempleLumio"


# ===========================
# UserConfig.lumio_manifest_id
# ===========================
def test_userconfig_accepte_lumio_manifest_id():
    config = UserConfig(
        tmdb_api_token="abc123",
        debrid_services=[{"service": "alldebrid", "api_key": "key123"}],
        lumio_manifest_id="ExempleLumio",
    )
    assert config.lumio_manifest_id == "ExempleLumio"


def test_userconfig_lumio_manifest_id_optionnel():
    config = UserConfig(
        tmdb_api_token="abc123",
        debrid_services=[{"service": "alldebrid", "api_key": "key123"}],
    )
    assert config.lumio_manifest_id is None
