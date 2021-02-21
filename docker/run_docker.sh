#!/bin/bash
# Declarando o nome da pasta
export PKG_DIR="$1"
# removendo a pasta e criando outra (-p) mesmo que o diretório pai 
# não exista
# E executando o container removendo automaticamente caso ele exista
# (--rm) e montando o volume (-v)
rm -rf ${PKG_DIR} && mkdir -p ${PKG_DIR}
docker run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.8 \
pip3 install -r requirements.txt -t ${PKG_DIR}