#!/bin/bash

echo "--- 1. Atualizando listas de pacotes... ---"
# Tenta usar sudo, se não tiver (como no Termux), roda direto
if command -v sudo &> /dev/null; then
    sudo apt update
    echo "--- 2. Instalando Python3 e Venv... ---"
    sudo apt install -y python3 python3-pip python3-venv
else
    apt update
    echo "--- 2. Instalando Python3 e Venv (sem sudo)... ---"
    apt install -y python3 python3-pip python3-venv
fi

echo "--- 3. Criando Ambiente Virtual (venv)... ---"
# Cria uma pasta oculta .venv para guardar as bibliotecas
python3 -m venv .venv

echo "--- 4. Ativando ambiente e instalando PgZero... ---"
# Ativa o ambiente temporariamente para instalar
source .venv/bin/activate

# Atualiza o pip para evitar avisos
pip install --upgrade pip

# Instala a biblioteca do jogo
pip install pgzero

echo ""
echo "=== INSTALAÇÃO CONCLUÍDA COM SUCESSO! ==="
echo "Para jogar, execute: ./play.sh"