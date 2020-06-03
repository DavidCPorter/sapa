#
#  Author: david porter
#  Date: Mon Feb  3 15:30:24 CST 2020

FROM ubuntu:latest

LABEL Description="local ubuntu server for janus local experiments"


RUN bash -c ' \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
                       curl \
                       dnsutils \
                       dstat \
                       ethtool \
                       git \
                       golang \
                       htop \
                       lsof \
                       make \
                       maven \
                       netcat \
                       nmap \
                       net-tools \
                       openssh-server \
                       procps \
                       python-dev \
                       python-pip \
                       python-setuptools \
                       ruby \
                       ruby-dev \
                       socat \
                       scala \
					   strace \
                       sysstat \
                       systemd \
					   sudo \
					   telnet \
                       tcpdump \
                       unzip \
                       vim \
                       wget \
                       zip && \
    apt-get update && \
    apt-get clean && \
	useradd -m -p $(openssl passwd -1 "password") -s /bin/bash -G sudo janususer'

EXPOSE 22 8983 9200

CMD service ssh start; sleep 99999

