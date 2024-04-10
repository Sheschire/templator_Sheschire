# templator

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![release-please](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-release--please-e10079.svg)](https://github.com/googleapis/release-please)
[![github-flow](https://img.shields.io/badge/git%20workflow-GitHub%20flow-brightgreen)](https://guides.github.com/introduction/flow/)
[![Robot Framework Style Guide](https://img.shields.io/badge/code_style-u%20iris-brightgreen.svg)](https://github.com/ugieiris/sandbox-test-rf/tree/master/styleguide-robot-framework)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

test diffusion template

## Installation

### Avec Artifactory

```bash
poetry add u-iris.robotframework-templator
```

### Avec Git

```bash
poetry add git+https://github.com/Sheschire/templator-test-rf.git
```

## Utilisation

Dans votre projet Robot Framework, charger les fichiers ressources avec la syntaxe suivante:

```robotframework
Library    ImportResource    resources=u_iris.templator
```

## Contribuer à ce projet

Se référer à la documentation du fichier [CONTRIBUTING.md](CONTRIBUTING.md).
