FROM fedora:41

RUN dnf -y check-update; \
    dnf -y upgrade && \
    dnf -y install python3.12 libglvnd-glx texlive-latex python-tox && \
    python3.12 -m ensurepip --user --altinstall && \
    python3.12 -m pip install --user tox 
