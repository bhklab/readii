FROM python:3.11-slim as base

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
RUN pip install --no-cache-dir readii

# Create a new image with just the bare minimum required to use the python package

FROM python:3.11-slim as final

COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Check that the package is installed
RUN readii --help
RUN imgtools --help

# On run, open a bash shell
CMD ["/bin/bash"]