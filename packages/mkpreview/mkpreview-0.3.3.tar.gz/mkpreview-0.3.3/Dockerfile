FROM ubuntu:latest
MAINTAINER Colin Bitterfield <cbitterfield@gmail.com>
USER root

LABEL Description="Production Container for creating preview Images and Database."
LABEL License="GNU Public License 3.0"
LABEL Usage="docker run -d  -v [DOCUMENT ROOT]:/data  cbitterfield/mkpreview"
LABEL Version="1.0"
LABEL maintainer="Colin Bitterfield <colin@bitterfield.com>"
LABEL Author="Colin Bitterfield <colin@bitterfield.com>"

ARG DATE_TIMEZONE=UTC
ARG DEBIAN_FRONTEND=noninteractive

# Set up environment
RUN apt-get update && apt-get install -y \
	python \
	python-dev \
	python-pip \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Update the operating system when we start and again at the end.
RUN apt-get update
RUN apt-get upgrade -y

# Add Basic Utilities needed
RUN apt-get install -y zip unzip
RUN apt install debconf-utils sudo -y
RUN apt-get install git nano tree vim curl ftp ssh  -y


# TODO: update this libraries
RUN pip install wheel==0.32.1 \
	watchdog==0.9.0

ADD . /mkpreview
WORKDIR /mkpreview
VOLUME /data

# Install app dependencies
RUN make install

ENTRYPOINT ["mkpreview"]
