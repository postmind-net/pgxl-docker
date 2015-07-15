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
RUN apt-get install -y pgxnclient

### LOCALE

RUN apt-get install -y locales && localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8
RUN locale-gen fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

### PGXL

WORKDIR /root
RUN git clone https://github.com/postmind-net/postgres-xl.git pgxl --depth 1
WORKDIR /root/pgxl
RUN ./configure --with-python --prefix /opt/pgxl
# ./configure --enable-cassert --enable-debug CFLAGS="-ggdb -Og -fno-omit-frame-pointer" --with-python --prefix /opt/pgxl
RUN make -j 4
WORKDIR /root/pgxl/contrib
RUN make -j 4
WORKDIR /root/pgxl
RUN make install
WORKDIR /root/pgxl/contrib
RUN make install

ENV PATH /opt/pgxl/bin:$PATH
ENV PGDATA /pom/pgxc

### PG EXTENSIONS

RUN pgxnclient install json_enhancements

RUN sudo apt-get install -y haproxy

### LD

RUN echo "/usr/local/lib" >> /etc/ld.so.conf
RUN echo "/opt/pgxl/lib" >> /etc/ld.so.conf
RUN ldconfig

### CONF

RUN mkdir -p /var/log/supervisor
COPY etc/supervisor/conf.d/supervisor.conf /etc/supervisor/conf.d/
COPY etc/sysctl.conf /etc/sysctl.conf
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

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 5432

CMD ["supervisor"]

