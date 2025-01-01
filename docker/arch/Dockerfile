FROM archlinux:latest

RUN \
  pacman-key --init && \
  pacman -Syu --noconfirm --noprogressbar && \
  pacman -S --noconfirm --noprogressbar \
    git \
    libglvnd \
    python \
    python-build \
    python-pip \
    python-pipx \
    python-tox \
    python-virtualenv \
    texlive-bin

