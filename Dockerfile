FROM ghcr.io/osgeo/gdal:ubuntu-small-3.6.4
ENV PYTHONUNBUFFERED=1
WORKDIR /code

# System deps + wkhtmltopdf (required for PDF generation via django-wkhtmltopdf)
RUN apt update -y && apt install -y \
    python3-pip \
    python3-dev \
    wget \
    xfonts-base \
    xfonts-75dpi \
    libfontconfig1 \
    libxrender1 \
 && wget -q https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb \
 && (dpkg -i wkhtmltox_0.12.5-1.buster_amd64.deb || apt-get install -f -y) \
 && rm wkhtmltox_0.12.5-1.buster_amd64.deb \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
