FROM python:3.11-slim

LABEL maintainer="Katy Scott"
LABEL description="This is a Dockerfile for the readii package."
LABEL license="MIT"
LABEL usage="docker run -it --rm <image_name> readii --help"
LABEL org.opencontainers.image.source="github.com/bhklab/readii"


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        && rm -rf /var/lib/apt/lists/*

# install readii
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir numpy==1.26.4
RUN pip install readii

RUN readii --help

# On run, open a bash shell
CMD ["/bin/bash"]