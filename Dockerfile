FROM python:3.9
COPY requirements.txt ./
RUN pip install -r requirements.txt; \
    mkdir /data
COPY . /code
VOLUME [ "/data" ]
CMD ["bash", "/code/docker/docker-entrypoint.sh"]
