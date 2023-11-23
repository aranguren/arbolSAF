FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt update -y
RUN apt install -y gdal-bin python3-gdal libgdal-dev python3-pycurl
#RUN pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}') --global-option=build_ext --global-option="-I/usr/include/gdal"
RUN apt install -y wget
RUN apt install -y xfonts-base
RUN apt install -y xfonts-75dpi
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb
RUN dpkg -i wkhtmltox_0.12.5-1.buster_amd64.deb

RUN pip install -r requirements.txt
#COPY . /code
