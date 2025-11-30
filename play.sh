#!/bin/bash

# Verifica se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "ERRO: Ambiente virtual não encontrado."
    echo "Por favor, rode o comando: bash setup.sh"
    exit 1
fi

# Ativa o ambiente
source .venv/bin/activate

# Roda o jogo
echo "Iniciando Shinobi Adventure..."
pgzrun game.py

# (Opcional) Desativa o ambiente ao fechar o jogo
deactivate