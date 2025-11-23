FROM ubuntu:noble
WORKDIR /root

# Expose postgresql port
EXPOSE 5432

# Install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y
#  Postgresql Dependencies
RUN apt install wget gcc g++ pkg-config libicu-dev bison flex libreadline-dev zlib1g-dev make perl -y 
# Stap Dependencies
RUN apt install git libelf-dev libdw-dev elfutils libboost-all-dev python3-setuptools gettext linux-headers-$(uname -r) vim -y 

# Stap installation
RUN git clone git://sourceware.org/git/systemtap.git
WORKDIR /root/systemtap
RUN ./configure && make
RUN make install; exit 0

# Get postgresql source
WORKDIR /root
RUN wget https://ftp.postgresql.org/pub/source/v18.0/postgresql-18.0.tar.gz
RUN tar -xvzf postgresql-18.0.tar.gz 
WORKDIR ./postgresql-18.0
# Run setup
RUN ./configure --enable-dtrace
RUN make
RUN su
RUN make install
# Create user as postgres will not run on root
RUN /sbin/useradd postgres
RUN mkdir -p /home/postgres/
RUN mkdir -p /usr/local/pgsql/data
RUN chown postgres /usr/local/pgsql/data
RUN chown postgres /home/postgres/
USER postgres
WORKDIR /home/postgres/
RUN /usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data

# Copy in config files
COPY ./configs/pga_hba.conf /usr/local/pgsql/data/pg_hba.conf
COPY ./configs/postgresql.conf /usr/local/pgsql/data/postgresql.conf
# Copy startup script
COPY ./start_postgres.sh /home/postgres/


CMD ["/home/postgres/start_postgres.sh"]

# CMD ["/usr/local/pgsql/bin/pg_ctl", "-D", "/usr/local/pgsql/data", "-l", "logfile", "start", "&&", "sleep", "infinity"]
# CMD ["sleep", "infinity"]
# CMD ["echo", "hey"]
