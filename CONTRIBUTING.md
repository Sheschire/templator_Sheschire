# Contribuer à ce projet

Ce document couvre les process visant à guider:

- l'auteur d'un changement (= un collaborateur souhaitant apporter sa contribution)
- un mainteneur (= un reviewer de code)

## Guide pour l'auteur d'un changement

### Bootstraper un environnement de développement

2 cas d'usage seront présentés ci-dessous:

- développement sur un hôte physique (par exemple, un laptop Windows 10)
- développement dans un devcontainer

#### Développer sur un hôte physique

##### Installer et configurer l'outillage requis

###### Python

Il est nécessaire d'installer un version Python supportée par de projet. Pour se faire, se référer à la section `[tool.poetry.dependencies]` du fichier [pyproject.toml](pyproject.toml). Chercher la clé `python` et choisir une version satisfaisant l'intervalle de versions.

Se référer ensuite à la documentation [Installer Python sur une machine de développement](https://confluence.systeme-u.com/pages/viewpage.action?pageId=11437773).

###### Poetry

[Poetry](https://python-poetry.org/) nécessite d'être installé. Pour ce faire, se référer à la documentation [Installer Poetry sur une machine de développement](https://confluence.systeme-u.com/pages/viewpage.action?pageId=11437809).

Afin d'installer des packages PyPi avec Poetry, une authentification à [Artifactory] est requise. Pour se faire, exécuter la commande suivante en remplaçant `<ARTIFACTORY_USERNAME>` pour votre nom de connexion:

```bash
poetry config http-basic.py-releases <ARTIFACTORY_USERNAME>
```



###### Éditeur de code

Ce projet est pré-configuré pour être utilisé avec [Visual Studio Code](https://code.visualstudio.com/) sur un système Windows. De petites modifications sont requises pour un système non-Windows.

##### Lancer le projet

Avant d'ouvrir un éditeur de code, il est nécessaire d'installer les dépendances requises pour ce projet:

```bash
poetry install
poetry run poe install
```

Si des problématiques de connexions sont rencontrées avec la seconde commande, lancer à la place:

- Sous PowerShell: `$env:NODE_TLS_REJECT_UNAUTHORIZED=0; poetry run poe install`
- Sous un shell Linux: `NODE_TLS_REJECT_UNAUTHORIZED=0 poetry run poe install`

Poetry se chargera de créer lui-même un environnement virtuel Python.

###### Cas particulier pour les utilisateurs qui utilisent Visual Studio Code

Si vous n'êtes pas sous une workstation Windows, les fichiers `workspace.code-workspace` et `.vscode/settings.json` devront être configurés selon votre environnement. En particulier, il faudra éditer les chemins qui référencent le répertoire `.venv`.

Par la suite, le projet pourra être ouvert de plusieurs façon:

- en exécutant le script PowerShell [`launch.ps1`](launch.ps1) (clique droit sur le fichier puis *Exécuter avec PowerShell*)
- en double-cliquant sur le fichier [`workspace.code-workspace`](workspace.code-workspace)

La première méthode est à privilégier car elle permettra de lancer l'éditeur Robot Framework en mode interactif.

Une fois au sein de VSCode, l'installation des extensions requises au développement Robot Framework pourraient être nécessaire. Si tel est le cas, la notification suivante apparaîtra:

![extension_recommendations](https://i.stack.imgur.com/DrPIB.png)

Installer toutes les extensions recommandées. Si la popup n'apparaît pas, les extensions pourront être manuellement installées en inspectant le fichier `.vscode/extensions.json`.

###### Cas particulier pour les utilisateurs n'utilisant pas Visual Studio Code

Si votre éditeur de code supporte les environnements virtuels Python, il faudra manuellement le configurer pour utiliser l'interpréteur Python résidant sous le dossier `.venv`.

Si vous n'êtes pas en mesure d'activer votre environnement virtuel, le faire avec la commande suivante:

```bash
poetry shell
```

#### Développer dans un devcontainer

##### Installer et configurer l'outillage requis

En prérequis à l'usage d'un devcontainer, suivre les modes d'emploi suivants:

- [Configurer une machine de développement pour utiliser un devcontainer](https://confluence.systeme-u.com/pages/viewpage.action?pageId=14517948)
- [Installer le serveur VcXsrv sur une machine de développement](https://confluence.systeme-u.com/pages/viewpage.action?pageId=14516688)

Les variables d'environnements ci-dessous devront être positionnées sur l'hôte physique:

| Nom | description |
|---|---|
| USER_CI | Nom d'utilisateur pour s'authentifier à Artifactory |
| PASSWORD_CI | Mot de passe pour s'authentifier à Artifactory |

##### Lancer le projet

Veiller à ce que Docker soit bien en cours d'exécution.

Lancer le serveur VcXsrv en double-cliquant sur le fichier [`config.xlaunch`](config.xlaunch).

Pour lancer le devcontainer, ouvrir VSCode à la racine du projet. Une fois dans VSCode, accéder à la palette de commande (CTRL+SHIT+P) et taper `Remote-Containers: Reopen in Container`.

Une fois au sein de la nouvelle instance VSCode, l'installation des extensions requises au développement Robot Framework pourraient être nécessaire. Si tel est le cas, la notification suivante apparaîtra:

![extension_recommendations](https://i.stack.imgur.com/DrPIB.png)

Installer toutes les extensions recommandées. Si la popup n'apparaît pas, les extensions pourront être manuellement installées en inspectant le fichier `.vscode/extensions.json`.

### Développer

Se référer à la documentation [Développer dans un projet Robot Framework](https://confluence.systeme-u.com/pages/viewpage.action?pageId=6393956).

### Soumettre une contribution

Se référer à la documentation [Soumettre une contribution sur un projet Robot Framework](https://confluence.systeme-u.com/display/ECIQDDI/RF-Soumettre+une+contribution+sur+un+projet+Robot+Framework)

## Guide du mainteneur

### Accepter de nouvelles contributions

Se référer à la documentation [Accepter de nouvelles contributions sur un projet Robot Framework](https://confluence.systeme-u.com/display/ECIQDDI/RF-Accepter+de+nouvelles+contributions+sur+un+projet+Robot+Framework).

### Créer de nouvelles releases

Se référer à la documentation [Créer une nouvelle release pour un projet Robot Framework](https://confluence.systeme-u.com/pages/viewpage.action?pageId=6393658).

[Style Guide Robot Framework d'U IRIS]: https://confluence.systeme-u.com/display/ECIQDDI/RF-Style+Guide
[Conventional Commits]: https://www.conventionalcommits.org/
[Artifactory]: https://artifactory-iris.groupement.systeme-u.fr
