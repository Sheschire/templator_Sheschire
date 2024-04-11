import os
import copier
import click
import requests
import sys
import subprocess
import yaml
from datetime import datetime

requests.packages.urllib3.disable_warnings()

TOKEN = "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"
ORG_NAME = "Sheschire"
SOURCE_BRANCH = "master"
COPIER_TEMPLATE = "https://github.com/ugieiris/template-robotframework.git"
timestamp = (str(round(datetime.now().timestamp())))


def check_template_version(repository, branch):
    # Vérifier si la branche existe
    branch_url = f'https://api.github.com/repos/{ORG_NAME}/{repository}/branches/{branch}'
    headers = {'Authorization': f'token {TOKEN}'}

    branch_response = requests.get(branch_url, headers=headers, verify=False)

    if branch_response.status_code != 200:
        return False

    # Lire le contenu du fichier YAML
    file_url = f'https://raw.githubusercontent.com/{ORG_NAME}/{repository}/{branch}/.copier-answers.yml'
    headers = {'Authorization': f'token {TOKEN}'}
    file_response = requests.get(file_url, headers=headers, verify=False)

    if file_response.status_code == 200:
        yaml_content = file_response.text
        data = yaml.safe_load(yaml_content)
        branch_version = data.get('_commit')
        if branch_version == VERSION:
            return True

    return False


def process_repository(repository, clone_url):
    branch_url = f"https://api.github.com/repos/{ORG_NAME}/{repository}/git/refs/heads/{SOURCE_BRANCH}"
    headers = {"Authorization": f"token {TOKEN}"}

    # Créer une nouvelle branche à partir de la branche source
    response = requests.get(branch_url, headers=headers, verify=False)
    template_branch_sha = response.json()["object"]["sha"]
    new_branch_data = {
        "ref": f"refs/heads/{TARGET_BRANCH}",
        "sha": template_branch_sha
    }
    response = requests.post(f"https://api.github.com/repos/{ORG_NAME}/{repository}/git/refs", json=new_branch_data, headers=headers, verify=False)

    # Clone du repository dans le répertoire temporaire
    temp_dir = f"{WORK_DIR}/{timestamp}/{repository}"
    os.makedirs(temp_dir, exist_ok=True)
    os.system(f"git clone {clone_url} {temp_dir}")
    os.chdir(temp_dir)
    os.system(f"git checkout {TARGET_BRANCH}")
    current_branch = subprocess.run("git branch --show-current", capture_output=True, shell=True, encoding="utf-8").stdout.rstrip()

    if current_branch != TARGET_BRANCH:
        sys.exit(f"La branche courante {current_branch} n'est pas la branche souhaitée : {TARGET_BRANCH}")

    # Utiliser Copier pour effectuer le "copy update"
    copier.run_update(
        src_path=COPIER_TEMPLATE,
        dst_path=temp_dir,
        unsafe=True,
        defaults=True,
        overwrite=True,
        vcs_ref=VERSION
    )

    # Commit et pousser les changements
    os.system("git add .")
    os.system("git commit -m \"Update_from_template\"")
    os.system("git push")

    # Créer une pull request
    pull_request_data = {
        "title": f"feature/sync-with-template-{VERSION}",
        "head": TARGET_BRANCH,
        "body": f"Synchronisation avec le template {COPIER_TEMPLATE} en version {VERSION}",
        "base": "master"
    }
    headers = {
        "Authorization": f"token {TOKEN}"
    }
    response = requests.post(f"https://api.github.com/repos/{ORG_NAME}/{repository}/pulls", json=pull_request_data, headers=headers, verify=False)
    print(f"Pull request created for repository: {repository}")


def update_template(project):
    url = f"https://api.github.com/repos/{project}"
    headers = {"Authorization": f"token {TOKEN}"}
    repository = requests.get(url, headers=headers, verify=False).json()["name"]
    clone_url = requests.get(url, headers=headers, verify=False).json()["clone_url"]

    master_on_good_version = check_template_version(repository, SOURCE_BRANCH)
    version_branch_created = check_template_version(repository, TARGET_BRANCH)

    if not master_on_good_version and not version_branch_created:
        process_repository(repository, clone_url)
        return


@click.option("--projects", help="Liste des projets sur lesquels diffuser le template", required=True)
@click.option("--version", help="Version à appliquer sur le copier-answers.yml de chaque projet", required=True)
def main(projects, version):
    global VERSION
    global TARGET_BRANCH
    VERSION = version
    TARGET_BRANCH = f"feature/sync-with-template-{VERSION}"

    for project in projects:
        update_template(project)


if __name__ == "__main__":
    main(["Sheschire/templator_Sheschire"], "v14.1.2")