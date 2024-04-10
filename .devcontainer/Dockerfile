FROM docker-registry-iris.groupement.systeme-u.fr/iris-mw/playwright-browser:1.39.0-node18-jammy

ARG POETRY_VERSION=1.2.0

ARG USER_UID=1000

ARG USER_GID=1000

ENV PIP_NO_CACHE_DIR=1

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

ENV POETRY_NO_INTERACTION=1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# hadolint ignore=DL3008
RUN apt-get install --yes --no-install-recommends --no-install-suggests \
        # Needed for installing Poetry.
        curl \
        # Needed for building Python dependencies.
        build-essential \
        # Needed to install dependencies from VCS platforms.
        git &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" &&\
    USER=$(id -un $USER_UID) &&\
    mkdir /commandhistory &&\
    touch /commandhistory/.bash_history &&\
    chown --recursive "$USER" /commandhistory &&\
    echo $SNIPPET >> "/home/$USER/.bashrc"

USER $USER_UID

RUN python3 -m pip install --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org poetry==$POETRY_VERSION &&\
    # @hack Temporary disabling SSL until the installation can be performed
    # without, when installing through Artifactory.
    npm config set strict-ssl=false

ENTRYPOINT [ "/bin/bash" ]
