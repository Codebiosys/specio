FROM selenium/standalone-chrome-debug:3.14
# ARG VNC_PASSWORD

# Do not buffer Python output
ENV PYTHONUNBUFFERED=1

RUN sudo apt-get update && sudo apt-get install -y \
  tmux \
  ffmpeg \
  python3 \
  python3-pip \
  gunicorn3

# Override the supervisor config.
COPY flask.conf /etc/supervisor/conf.d/

# Copy in a custom version of the XVFB start script.
COPY start-xvfb.sh \
      start-flask-server.sh \
      /opt/bin/

# Setup the flask app
RUN pip3 install flask
COPY server.py /opt/bin/server.py
