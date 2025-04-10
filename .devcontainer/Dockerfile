FROM mcr.microsoft.com/devcontainers/python:3.13-bullseye

# Instalar Miniconda
RUN curl -sSLo miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x miniconda.sh && ./miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh

# Crear entorno conda e instalar dependencias
COPY .devcontainer/requirements.txt /tmp/requirements.txt
RUN /opt/conda/bin/conda create -n azurebeach python=3.13 -y && \
    /opt/conda/bin/conda run -n azurebeach pip install --upgrade pip && \
    /opt/conda/bin/conda run -n azurebeach pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

ENV PATH="/opt/conda/envs/azurebeach/bin:/opt/conda/bin:$PATH"
ENV CONDA_DEFAULT_ENV=azurebeach
ENV ENVIRONMENT=container

# Establecer bash como shell por defecto
SHELL ["/bin/bash", "-c"]
