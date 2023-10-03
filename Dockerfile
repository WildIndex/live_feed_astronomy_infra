FROM python:3.9-slim

ADD . /app

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      wget \
      python3-tk && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install --no-cache --no-cache-dir --upgrade -r requirements.txt

# Minimize image size 
RUN (apt-get autoremove -y; \
     apt-get autoclean -y)

EXPOSE 5000

COPY . .

CMD [ "python", "app.py" ]
