FROM ubuntu:22.04

ARG USERNAME=dev_user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user and configure sudo
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && chown -R $USER_UID:$USER_GID /home/$USERNAME

# Install and configure packages required from ubuntu repository
RUN apt-get update \
    && DEBIAN_FRONTEND="noninteractive" \
    apt-get install -y curl gnupg build-essential bash-completion nano \
    python3 python3-dev python3-pip git git-lfs ca-certificates curl wget \
    default-jre-headless graphviz python3-venv python-is-python3 gtkwave \
    python3-tk libssl-dev libffi-dev gettext

# Upgrade pip to latest version and install required packages from PyPI
RUN pip install --upgrade pip

USER $USERNAME

ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

# Installs poetry and Azure CLI
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.5.1 \
    && curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash - \
    && poetry config virtualenvs.in-project true

USER root

# enables command completion on bash
RUN poetry completions bash > /etc/bash_completion.d/poetry
