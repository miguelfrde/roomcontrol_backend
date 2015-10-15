FROM resin/rpi-raspbian

MAINTAINER Miguel Flores Ruiz de Eguino (@miguelfrde) <miguel.frde@gmail.com>

# Define working directory
WORKDIR /roomcontrol

# Install dependencies
RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    python-pip \
    python-virtualenv \
    libffi-dev \
    libspotify-dev \
    libspotify12 \
    portaudio19-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# RabbitMQ
RUN echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list
RUN wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
RUN apt-key add rabbitmq-signing-key-public.asc
RUN apt-get install -y rabbitmq-server

# Install python packages
RUN pip install -e '.[dev]' --allow-unverified=pyaudio

# Define default command
CMD ["roomcontrol run"]
