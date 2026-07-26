#!/bin/bash

# Script de Gravação Automatizada — Legal AI Copilot
# Executa as 14 cenas conforme o shot list usando xdotool

set -e

echo "================================================================================"
echo "GRAVAÇÃO AUTOMATIZADA — LEGAL AI COPILOT"
echo "================================================================================"
echo ""
echo "⚠️  INSTRUÇÕES:"
echo "1. Inicie a gravação de tela AGORA (OBS, ScreenFlow, etc)"
echo "2. Aguarde 10 segundos para sincronização"
echo "3. O script controlará o navegador automaticamente"
echo ""
echo "================================================================================"
echo ""

# Aguardar 10 segundos para o usuário iniciar a gravação
echo "Aguardando 10 segundos para sincronização..."
for i in {10..1}; do
    echo -ne "  $i...\r"
    sleep 1
done

echo ""
echo "🎬 Iniciando gravação!"
echo ""

# ============================================================================
# ABRIR NAVEGADOR
# ============================================================================
echo "Abrindo navegador..."
# Abrir Chrome/Chromium em modo fullscreen
google-chrome --new-window "http://localhost:5173" &
CHROME_PID=$!
sleep 5

# Maximizar janela
xdotool search --name "Chrome" windowactivate windowsize 100% 100%
sleep 2

echo "✓ Navegador aberto em http://localhost:5173"
wait_for_page 5

# Função para mover mouse com delay
move_mouse() {
    local x=$1
    local y=$2
    local duration=${3:-0.5}
    xdotool mousemove --sync $x $y
    sleep $duration
}

# Função para clicar com delay
click_mouse() {
    local delay=${1:-0.3}
    sleep $delay
    xdotool click 1
    sleep 0.3
}

# Função para digitar com delay
type_text() {
    local text="$1"
    local delay=${2:-0.05}
    xdotool type --delay $delay "$text"
}

# Função para scroll
scroll_mouse() {
    local direction=$1
    local amount=$2
    if [ "$direction" = "down" ]; then
        for i in $(seq 1 $amount); do
            xdotool key Page_Down
            sleep 0.3
        done
    else
        for i in $(seq 1 $amount); do
            xdotool key Page_Up
            sleep 0.3
        done
    fi
}

# Função para aguardar carregamento
wait_for_page() {
    local seconds=${1:-3}
    echo "   ⏳ Aguardando carregamento ($seconds segundos)..."
    sleep $seconds
}

# ============================================================================
# CENA 01-03: TÍTULO, PROBLEMA E ARQUITETURA (1:45)
# ============================================================================
echo "================================================================================"
echo "CENA 01-03: TÍTULO, PROBLEMA E ARQUITETURA (1:45)"
echo "================================================================================"

echo ""
echo "[CENA 01] Título / Abertura..."
sleep 3

move_mouse 960 300 2
sleep 2

move_mouse 960 350 1
sleep 3

move_mouse 960 540 2
sleep 2

move_mouse 960 680 2
sleep 3

move_mouse 960 540 1.5
sleep 2

echo "✓ CENA 01 concluída"

echo ""
echo "[CENA 02] Problema e Contexto..."
sleep 5

move_mouse 960 430 2
sleep 3

move_mouse 960 510 1
sleep 3

move_mouse 960 580 1
sleep 3

move_mouse 960 540 1.5
sleep 5

move_mouse 1700 950 2
sleep 2

echo "✓ CENA 02 concluída"

echo ""
echo "[CENA 03] Arquitetura..."
sleep 3

move_mouse 960 680 2
sleep 3

move_mouse 960 740 1
sleep 3

move_mouse 960 540 2
sleep 5

move_mouse 960 580 1
sleep 2

echo "✓ CENA 03 concluída"

# ============================================================================
# CENA 04: LOGIN (0:30)
# ============================================================================
echo ""
echo "================================================================================"
echo "CENA 04: LOGIN (0:30)"
echo "================================================================================"

echo ""
echo "[CENA 04] Login com credenciais..."
wait_for_page 2

# Clicar em "Advogado"
move_mouse 530 433 1.5
click_mouse 0.5
echo "✓ Clicou em 'Advogado'"
wait_for_page 1.5

# Clicar em "Entrar"
move_mouse 529 364 1.5
click_mouse 0.5
echo "✓ Clicou em 'Entrar'"
wait_for_page 4

# Aguardar dashboard carregar
move_mouse 960 540 1
wait_for_page 2

echo "✓ CENA 04 concluída"

# ============================================================================
# CENA 05: DASHBOARD (0:30)
# ============================================================================
echo ""
echo "================================================================================"
echo "CENA 05: DASHBOARD (0:30)"
echo "================================================================================"

echo ""
echo "[CENA 05] Dashboard e navegação..."
wait_for_page 1

# Mostrar navbar items com hover
move_mouse 200 32 0.8
wait_for_page 0.3
move_mouse 310 32 0.8
wait_for_page 0.3
move_mouse 400 32 0.8
wait_for_page 0.3
move_mouse 480 32 0.8
wait_for_page 0.3
move_mouse 570 32 0.8
wait_for_page 0.3
move_mouse 660 32 0.8
wait_for_page 0.3
move_mouse 770 32 0.8
wait_for_page 0.3
move_mouse 870 32 0.8
wait_for_page 0.3
move_mouse 970 32 0.8
wait_for_page 0.5

# Mover para canto inferior direito
move_mouse 1750 32 2
wait_for_page 1

# Explorar dashboard
move_mouse 300 300 2
wait_for_page 1.5

# Clicar em "Upload PDF"
move_mouse 1650 120 2
click_mouse 0.5
echo "✓ Clicou em 'Upload PDF'"
wait_for_page 2

echo "✓ CENA 05 concluída"

# ============================================================================
# CENA 06: UPLOAD DE CONTRATO (1:00)
# ============================================================================
echo ""
echo "================================================================================"
echo "CENA 06: UPLOAD DE CONTRATO (1:00)"
echo "================================================================================"

echo ""
echo "[CENA 06] Upload com processamento..."
wait_for_page 1

# Clicar no campo de título
move_mouse 960 300 1
click_mouse 0.3
wait_for_page 0.5

# Digitar nome do contrato
type_text "Contrato de Prestacao de Servicos - Demo" 0.03
wait_for_page 0.8

# Clicar na área de upload
move_mouse 960 450 1.5
click_mouse 0.3
echo "✓ Clicou em área de upload"
wait_for_page 2

# Aguardar seleção de arquivo
wait_for_page 2

# Clicar em "Fazer Upload"
move_mouse 960 650 1.5
click_mouse 0.3
echo "✓ Clicou em 'Fazer Upload'"
wait_for_page 5

# Aguardar processamento
wait_for_page 3

# Explorar página
move_mouse 960 540 1.5
wait_for_page 2

echo "✓ CENA 06 concluída"

# ============================================================================
# CENA 07: ANÁLISE (1:30)
# ============================================================================
echo ""
echo "================================================================================"
echo "CENA 07: ANÁLISE (1:30)"
echo "================================================================================"

echo ""
echo "[CENA 07] Análise - Resumo e Extração..."

# Clicar em "Análise"
move_mouse 480 32 2
click_mouse 0.3
echo "✓ Clicou em 'Análise'"
wait_for_page 4

# Explorar análise
move_mouse 1700 950 1
wait_for_page 2

move_mouse 960 250 2
wait_for_page 2

move_mouse 1500 250 1.5
wait_for_page 1

# Scroll para ver mais conteúdo
scroll_mouse down 3
wait_for_page 1.5

# Explorar diferentes áreas
move_mouse 400 500 2
wait_for_page 2

move_mouse 1400 500 2
wait_for_page 2

move_mouse 400 800 2
wait_for_page 2

move_mouse 1400 800 2
wait_for_page 2

# Voltar ao topo
scroll_mouse up 3
wait_for_page 1

echo "✓ CENA 07 concluída"

# ============================================================================
# CENA 08: CHAT COM AGENT ROUTER (1:30)
# ============================================================================
echo ""
echo "================================================================================"
echo "CENA 08: CHAT COM AGENT ROUTER (1:30)"
echo "================================================================================"

echo ""
echo "[CENA 08] Chat com roteamento..."

# Clicar em "Iniciar Chat"
move_mouse 1500 250 1.5
click_mouse 0.3
echo "✓ Clicou em 'Iniciar Chat'"
wait_for_page 3

# Explorar chat
move_mouse 960 540 1.5
wait_for_page 1.5

# Mostrar sidebar
move_mouse 150 120 2
wait_for_page 1.5

move_mouse 150 200 1
wait_for_page 1.5

# Clicar no campo de mensagem
move_mouse 960 950 2
click_mouse 0.3
wait_for_page 0.5

# Digitar pergunta
type_text "Quais sao os riscos deste contrato?" 0.03
wait_for_page 0.8

# Clicar em Send
move_mouse 1750 950 1
click_mouse 0.3
echo "✓ Clicou em Send"
wait_for_page 1

# Aguardar resposta do agente
move_mouse 1700 950 1
wait_for_page 5

# Aguardar processamento
wait_for_page 2

# Explorar resposta
move_mouse 800 600 2
wait_for_page 2

move_mouse 800 800 1.5
wait_for_page 2

# Scroll para ver mais
scroll_mouse down 2
wait_for_page 1

move_mouse 800 900 1
wait_for_page 2

# Voltar ao topo
move_mouse 1700 950 1.5
wait_for_page 1.5

echo "✓ CENA 08 concluída"

# ============================================================================
# CENA 09: ANÁLISE DE RISCOS (1:30)
# ============================================================================
echo ""
echo "================================================================================"
echo "CENA 09: ANÁLISE DE RISCOS (1:30)"
echo "================================================================================"

echo ""
echo "[CENA 09] Análise de Riscos..."

# Clicar em "Riscos"
move_mouse 570 32 2
click_mouse 0.3
echo "✓ Clicou em 'Riscos'"
wait_for_page 3

# Explorar página
move_mouse 960 300 1.5
wait_for_page 1.5

# Clicar em "Analyze Risks"
move_mouse 960 400 1.5
click_mouse 0.3
echo "✓ Clicou em 'Analyze Risks'"
wait_for_page 5

# Aguardar análise
move_mouse 1700 950 1
wait_for_page 3

# Explorar resultados
move_mouse 960 300 2
wait_for_page 2

move_mouse 960 500 1.5
wait_for_page 2

# Clicar em "Sources"
move_mouse 1100 600 1
click_mouse 0.3
echo "✓ Clicou em 'Sources'"
wait_for_page 2

# Explorar sources
move_mouse 960 700 1
wait_for_page 2

# Scroll para ver mais
scroll_mouse down 3
wait_for_page 1.5

# Explorar mais
move_mouse 960 900 2
wait_for_page 2

# Voltar ao topo
move_mouse 1700 950 1.5
wait_for_page 1.5

echo "✓ CENA 09 concluída"

# ============================================================================
# CENA 10-14: AUTOMAÇÕES, REVISÕES, MÉTRICAS, COMPARAÇÃO E CONCLUSÃO
# ============================================================================
echo ""
echo "================================================================================"
echo "CENA 10-14: AUTOMAÇÕES, REVISÕES, MÉTRICAS, COMPARAÇÃO E CONCLUSÃO"
echo "================================================================================"

echo ""
echo "[CENA 10] Automações..."
# Clicar em "Automações"
move_mouse 660 32 2
click_mouse 0.3
wait_for_page 3

# Explorar automações
move_mouse 960 300 1.5
wait_for_page 2

move_mouse 300 300 1.5
wait_for_page 1.5

move_mouse 600 350 1.5
wait_for_page 1.5

move_mouse 1400 350 2
wait_for_page 1.5

# Scroll para ver mais
scroll_mouse down 3
wait_for_page 1.5

# Voltar ao topo
move_mouse 1700 950 2
wait_for_page 1

echo "✓ CENA 10 concluída"

echo ""
echo "[CENA 11] Revisão Humana..."
# Clicar em "Revisão Humana"
move_mouse 770 32 2
click_mouse 0.3
wait_for_page 3

# Explorar página
move_mouse 960 400 1.5
wait_for_page 1.5

# Mostrar filtros
move_mouse 300 120 2
wait_for_page 1

move_mouse 450 120 1
wait_for_page 1

# Clicar em item
move_mouse 250 250 2
wait_for_page 1.5

click_mouse 0.3
wait_for_page 1.5

# Explorar detalhes
move_mouse 1700 950 1.5
wait_for_page 2

move_mouse 1200 400 2
wait_for_page 2

move_mouse 1200 800 2
wait_for_page 1

click_mouse 0.3
wait_for_page 1.5

# Voltar
move_mouse 1700 950 1.5
wait_for_page 2

echo "✓ CENA 11 concluída"

echo ""
echo "[CENA 12] Métricas de Impacto..."
# Clicar em "Métricas"
move_mouse 870 32 2
click_mouse 0.3
wait_for_page 3

# Explorar página
move_mouse 960 300 1.5
wait_for_page 1.5

move_mouse 400 300 1.5
wait_for_page 2

move_mouse 1400 300 2
wait_for_page 2

move_mouse 400 600 2
wait_for_page 2

move_mouse 1400 600 2
wait_for_page 2

# Scroll para ver mais
scroll_mouse down 3
wait_for_page 1.5

# Explorar mais
move_mouse 960 800 2
wait_for_page 2

# Voltar ao topo
move_mouse 1700 950 2
wait_for_page 1.5

echo "✓ CENA 12 concluída"

echo ""
echo "[CENA 13] Comparação de Contratos..."
# Clicar em "Comparação"
move_mouse 970 32 2
click_mouse 0.3
wait_for_page 3

# Explorar página
move_mouse 960 300 1.5
wait_for_page 1.5

# Selecionar contratos para comparar
move_mouse 400 120 1.5
click_mouse 0.3
wait_for_page 0.5

move_mouse 400 180 1
click_mouse 0.3
wait_for_page 0.5

move_mouse 1400 120 2
click_mouse 0.3
wait_for_page 0.5

move_mouse 1400 180 1
click_mouse 0.3
wait_for_page 0.5

# Clicar em "Comparar"
move_mouse 960 250 1.5
click_mouse 0.3
wait_for_page 5

# Explorar resultados
move_mouse 1700 950 1.5
wait_for_page 2

move_mouse 960 400 2
wait_for_page 2

# Scroll para ver comparação
scroll_mouse down 4
wait_for_page 1.5

# Explorar mais
move_mouse 960 700 2
wait_for_page 2

# Voltar ao topo
move_mouse 1700 950 2
wait_for_page 1.5

echo "✓ CENA 13 concluída"

echo ""
echo "[CENA 14] Conclusão / Encerramento..."
# Clicar em "Home"
move_mouse 200 32 2
click_mouse 0.3
wait_for_page 2

# Explorar dashboard final
move_mouse 960 540 1.5
wait_for_page 2

# Mover para canto superior direito
move_mouse 1750 32 2
wait_for_page 1.5

# Clicar em menu de usuário
move_mouse 1750 80 1
wait_for_page 1

click_mouse 0.3
wait_for_page 1.5

# Explorar menu
move_mouse 960 540 1.5
wait_for_page 2

echo "✓ CENA 14 concluída"

# ============================================================================
# CONCLUSÃO
# ============================================================================
echo ""
echo "================================================================================"
echo "✅ GRAVAÇÃO CONCLUÍDA COM SUCESSO!"
echo "================================================================================"
echo ""
echo "Duração total: ~12 minutos"
echo "Todas as 14 cenas foram executadas"
echo ""
echo "Próximas etapas:"
echo "1. Parar a gravação de tela"
echo "2. Exportar vídeo em 1080p"
echo "3. Sincronizar áudio com narração"
echo "4. Revisar qualidade e transições"
echo ""
echo "================================================================================"
