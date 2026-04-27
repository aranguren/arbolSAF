FROM ghcr.io/osgeo/gdal:ubuntu-small-3.6.4
ENV PYTHONUNBUFFERED=1
WORKDIR /code

RUN apt update -y && apt install -y python3-pip python3-dev
RUN pip3 install --upgrade pip

COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
