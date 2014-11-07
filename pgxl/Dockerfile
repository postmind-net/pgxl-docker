FROM ubuntu:14.04
MAINTAINER Matthieu Lagacherie - Yannick Drant

USER root

### USER

RUN adduser pom --disabled-password --gecos "" --home /pom --shell /bin/bash
RUN adduser pom sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

### BASE PACKAGES

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y screen cmake vim
RUN apt-get install -y software-properties-common
RUN apt-get install -y curl flex bison zlib1g-dev libreadline6-dev gcc make supervisor git \
                    openssh-server openssh-client rsync
RUN apt-get install -y python-dev

### LOCALE

RUN apt-get install -y locales
        && localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8
RUN locale-gen fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

### PGXL

WORKDIR /root
RUN git clone git://git.code.sf.net/p/postgres-xl/postgres-xl pgxl --depth 1
WORKDIR /root/pgxl
RUN ./configure --with-python --prefix /opt/pgxl
RUN make -j 4
WORKDIR /root/pgxl/contrib
RUN make -j 4
WORKDIR /root/pgxl
RUN make install
WORKDIR /root/pgxl/contrib
RUN make install

ENV PATH /opt/pgxl/bin:$PATH
ENV PGDATA /pom/pgxc

### LD

RUN echo "/usr/local/lib" >> /etc/ld.so.conf
RUN echo "/opt/pgxl/lib" >> /etc/ld.so.conf
RUN ldconfig

### CONF

RUN mkdir -p /var/log/supervisor /pom/pgxc_ctl
COPY etc/supervisor/conf.d/supervisor.conf /etc/supervisor/conf.d/
COPY etc/supervisor/conf.d/pgxl.conf /etc/supervisor/conf.d/pgxl.conf
COPY etc/sysctl.conf /etc/sysctl.conf
COPY etc/pgxc_ctl.conf /pom/pgxc_ctl/pgxc_ctl.conf
COPY etc/environment /etc/environment

### SSH
RUN echo "   StrictHostKeyChecking no" >> /etc/ssh/ssh_config
RUN sudo /etc/init.d/ssh start && sudo /etc/init.d/ssh stop 

### USER

ADD . /app
RUN chown -R pom:pom /app /pom
USER pom
WORKDIR /pom
ENV HOME /pom

### SSH USER KEY FOR LOCAL SSH
RUN ssh-keygen -t rsa -C "pom@pgxl" -f /pom/.ssh/id_rsa -q -N ""
RUN cat /pom/.ssh/id_rsa.pub >> /pom/.ssh/authorized_keys

VOLUME ["/pom"]
ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 5432
CMD ["supervisor"]

