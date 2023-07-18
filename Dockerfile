FROM python:3-alpine

# upgrade pip
RUN pip install --upgrade pip

# permissions and flask user for tightened security
RUN adduser -D flask
RUN mkdir /app && chown -R flask:flask /app
RUN mkdir -p /var/log/flask && touch /var/log/flask/flask.err.log && touch /var/log/flask/flask.out.log
RUN chown -R flask:flask /var/log/flask
WORKDIR /app
USER flask

# copy all the files to the container
COPY --chown=flask:flask requirements.txt /app/
COPY --chown=flask:flask airgradient.py /app/

# venv
ENV VIRTUAL_ENV=/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP="airgradient.py"
RUN pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 5909

ENTRYPOINT [ "flask" ]
CMD ["run", "--port=5909", "--host=0.0.0.0"]