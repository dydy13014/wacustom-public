# Wacustom Public

> **Version « instance publique » de [Wacustom](https://github.com/dydy13014/wacustom)**, lui-même fork de [WAStream](https://gitlab.com/10ho/wastream) (10ho / spel, MIT).
> Même moteur, mêmes sources, une différence de fond : **chaque utilisateur apporte ses propres clés**. L'hébergeur fournit l'infrastructure, jamais ses comptes.

Si vous voulez un addon pour vous seul, sur votre propre serveur, c'est [Wacustom](https://github.com/dydy13014/wacustom) qu'il vous faut. Ce dépôt sert à héberger une instance ouverte à plusieurs personnes.

## En quoi c'est différent de Wacustom

| | Wacustom (self-host) | Wacustom Public |
|---|---|---|
| Clés des trackers privés (YggReborn, Tr4ker, Torr9, C411, V3X, Gemini, Generation-Free) | dans le `.env` de l'hébergeur, partagées par tous les utilisateurs de l'instance | **saisies par chaque utilisateur** dans `/configure`, chiffrées dans sa configuration |
| Manifest Lumio | dans le `.env` de l'hébergeur | **saisi par chaque utilisateur** |
| Réglage `*_API_KEY` côté serveur | oui | **n'existe pas** : ni dans le `.env`, ni dans le tableau de bord admin. Une clé posée là ne serait lue nulle part |
| Sources sans clé (Wawacity, Free-Telecharger, Movix, Zone-Telechargement, Nyaa, Zilean…) | configurées par l'hébergeur | configurées par l'hébergeur, partagées par tous |
| Validation des configurations utilisateur | contrôle de présence du débrideur | validation complète à la création **et** à la mise à jour (tracker inconnu ou clé vide refusés) |
| Pause anti-quota Lumio | globale | **par identifiant** : le quota d'un utilisateur ne bloque pas les autres |

Le reste (débrideurs, filtres, lecture résiliente, tableau de bord, sondes de santé, cache mutualisé) est identique à Wacustom. La liste complète des fonctionnalités est dans [son README](https://github.com/dydy13014/wacustom#readme).

## Côté utilisateur

1. Ouvrez `/configure` sur l'instance.
2. Renseignez votre débrideur et votre token TMDB, comme d'habitude.
3. Dans **« Vos trackers privés »**, collez la clé API de chaque tracker où vous avez un compte. Laissez vides les autres : ils sont simplement ignorés pour vous, aucune clé ne vous est prêtée.
4. Dans **« Votre manifest Lumio »**, collez l'identifiant de votre manifest personnel si vous avez un compte Lumio.
5. Générez votre lien et ajoutez-le à Stremio.

> ⚠️ **Conservez votre UUID** (il est dans l'URL de votre manifest). Sans lui, votre configuration est définitivement perdue : le mot de passe seul ne permet aucune récupération, et l'hébergeur ne peut rien retrouver pour vous.

Vos clés sont chiffrées avec votre mot de passe. L'hébergeur ne les voit pas en clair, mais **elles sont utilisées depuis son serveur** (voir ci-dessous).

## Côté hébergeur

### Installation

```bash
curl -O https://raw.githubusercontent.com/dydy13014/wacustom-public/main/.env.example
cp .env.example wacustom-public.env
# Renseignez SECRET_KEY, ADMIN_PASSWORD, et les URLs des sources que vous proposez
```

```yaml
services:
  wacustom-public:
    image: ghcr.io/dydy13014/wacustom-public:latest
    container_name: wacustom-public
    env_file:
      - wacustom-public.env
    volumes:
      - wacustom-public-data:/app/data
    ports:
      - "127.0.0.1:7000:7000"
    restart: unless-stopped

volumes:
  wacustom-public-data:
```

```bash
docker compose up -d
```

Exposez ensuite le port derrière un reverse proxy HTTPS (Traefik, Caddy, nginx). Le `docker-compose.yml` du dépôt utilise `build: .` pour builder l'image localement.

### Ce que vous configurez

- Les **URLs** des trackers (`YGGREBORN_URL`, `TR4KER_URL`, `C411_URL`, `V3X_URL`…) : identiques pour tout le monde, c'est vous qui décidez quels trackers l'instance sait interroger. Un tracker sans URL est indisponible pour tous.
- Les **sources sans clé** (Wawacity, Free-Telecharger, Movix, Zone-Telechargement, Nyaa, Zilean) : scrapées depuis l'IP de votre serveur pour tous les utilisateurs.
- Aucune clé de tracker : il n'y a pas de variable pour ça.

### ⚠️ À lire avant d'ouvrir une instance

- **Le scraping part de l'IP de votre serveur.** La lecture vidéo, elle, part de l'IP du spectateur. Conséquence : les clés de **tous** vos utilisateurs sont utilisées depuis **une seule IP**, ce que beaucoup de trackers privés assimilent à du partage de compte. Risque de bannissement pour les comptes de vos utilisateurs **et** pour votre IP. Vérifiez les règles des trackers concernés, et prévenez vos utilisateurs.
- Un `PROXY_URL` (WARP par exemple) protège votre IP vis-à-vis des sites scrapés, mais ne change rien au point précédent.
- Le cache est mutualisé : cent personnes demandant le même film ne déclenchent qu'un seul scrape. La charge suit le nombre de contenus distincts, pas le nombre d'utilisateurs.
- Pensez à un mot de passe d'accès (`ADDON_PASSWORD`) si l'instance n'est pas destinée à être totalement ouverte.

## Tests

```bash
pip install -e ".[test]"
pytest
```

Les tests propres à cette version sont dans `tests/test_user_trackers.py` et `tests/test_lumio.py`. Le plus important vérifie qu'un scraper **ne retombe jamais** sur une clé de l'hébergeur.

## Licence

MIT, comme WAStream et Wacustom. Voir [LICENSE](LICENSE).

## Clause de non-responsabilité

Ce logiciel est fourni à des fins éducatives. L'hébergeur d'une instance et ses utilisateurs sont seuls responsables de l'usage qu'ils en font et du respect des lois et des conditions d'utilisation des services interrogés.
