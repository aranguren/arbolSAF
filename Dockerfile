FROM ghcr.io/osgeo/gdal:ubuntu-small-3.6.4
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /code

# System deps + wkhtmltopdf (required for PDF generation via django-wkhtmltopdf)
# Using Ubuntu 22.04 (Jammy) apt package — the old buster .deb does not install on Ubuntu
RUN apt update -y && apt install -y \
    python3-pip \
    python3-dev \
    xfonts-base \
    xfonts-75dpi \
    libfontconfig1 \
    libxrender1 \
    wkhtmltopdf \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
