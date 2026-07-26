#!/bin/bash

# Script de teste simples - apenas abre navegador e faz login

echo "================================================================================"
echo "TESTE SIMPLES — GRAVAÇÃO AUTOMATIZADA"
echo "================================================================================"
echo ""
echo "Abrindo navegador em 5 segundos..."
sleep 5

echo ""
echo "🎬 Abrindo navegador..."
google-chrome --new-window "http://localhost:5173" &
sleep 5

# Maximizar janela
xdotool search --name "Chrome" windowactivate windowsize 100% 100%
sleep 2

echo "✓ Navegador aberto"
echo ""
echo "Aguardando 3 segundos para página carregar..."
sleep 3

echo ""
echo "Clicando em 'Advogado'..."
xdotool mousemove 530 433
sleep 1
xdotool click 1
sleep 1

echo "✓ Clicou em Advogado"
echo ""
echo "Aguardando 2 segundos..."
sleep 2

echo "Clicando em 'Entrar'..."
xdotool mousemove 529 364
sleep 1
xdotool click 1
sleep 1

echo "✓ Clicou em Entrar"
echo ""
echo "Aguardando 5 segundos para dashboard carregar..."
sleep 5

echo ""
echo "✅ TESTE CONCLUÍDO!"
echo "Se você viu o login acontecer, a automação está funcionando!"
echo ""
