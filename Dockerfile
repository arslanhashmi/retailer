FROM python:3.7

ENV PYTHONUNBUFFERED 1

# Set apps home directory.
ENV APP_DIR /rtailer
RUN mkdir ${APP_DIR}

# Adds the application code to the image
ADD . ${APP_DIR}

# Define current working directory.
WORKDIR ${APP_DIR}

# Cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --disable-pip-version-check --exists-action w -r requirements.txt

EXPOSE 8080
