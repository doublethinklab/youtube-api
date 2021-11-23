#syntax=docker/dockerfile:experimental
FROM python:3.9.5

# need this to install dependencies using our ssh key from github
RUN apt install openssh-client
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN --mount=type=ssh,id=github pip install -r requirements.txt
RUN rm requirements.txt
