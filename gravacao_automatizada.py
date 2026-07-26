#!/usr/bin/env python3
"""
Script de Gravação Automatizada — Legal AI Copilot
Executa as 14 cenas conforme o shot list
"""

import time
import subprocess
import sys

def instalar_pyautogui():
    """Instala pyautogui se não estiver disponível"""
    try:
        import pyautogui
        return pyautogui
    except ImportError:
        print("Instalando pyautogui...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyautogui", "-q"], check=True)
        import pyautogui
        return pyautogui

def main():
    print("=" * 80)
    print("GRAVAÇÃO AUTOMATIZADA — LEGAL AI COPILOT")
    print("=" * 80)
    print("\n⚠️  INSTRUÇÕES:")
    print("1. Inicie a gravação de tela AGORA (OBS, ScreenFlow, etc)")
    print("2. Aguarde 10 segundos para sincronização")
    print("3. O script controlará o navegador automaticamente")
    print("\n" + "=" * 80)
    
    # Aguardar 10 segundos para o usuário iniciar a gravação
    print("\nAguardando 10 segundos para sincronização...")
    for i in range(10, 0, -1):
        print(f"  {i}...", end="\r")
        time.sleep(1)
    
    print("\n🎬 Iniciando gravação!\n")
    
    # Instalar pyautogui
    pyautogui = instalar_pyautogui()
    
    # Configurar velocidade do mouse
    pyautogui.PAUSE = 0.1
    pyautogui.FAILSAFE = True
    
    try:
        # ====================================================================
        # CENA 01-03: TÍTULO, PROBLEMA E ARQUITETURA (1:45)
        # ====================================================================
        print("=" * 80)
        print("CENA 01-03: TÍTULO, PROBLEMA E ARQUITETURA (1:45)")
        print("=" * 80)
        
        # CENA 01: Tela estática com movimentos de cursor
        print("\n[CENA 01] Título / Abertura...")
        time.sleep(3)  # Tela estática
        
        # Mover cursor para logo
        pyautogui.moveTo(960, 300, duration=2)
        time.sleep(2)
        
        # Mover para título
        pyautogui.moveTo(960, 350, duration=1)
        time.sleep(3)
        
        # Voltar ao centro
        pyautogui.moveTo(960, 540, duration=2)
        time.sleep(2)
        
        # Para credenciais
        pyautogui.moveTo(960, 680, duration=2)
        time.sleep(3)
        
        # Voltar ao centro
        pyautogui.moveTo(960, 540, duration=1.5)
        time.sleep(2)
        
        print("✓ CENA 01 concluída")
        
        # CENA 02: Problema e contexto
        print("\n[CENA 02] Problema e Contexto...")
        time.sleep(5)
        
        pyautogui.moveTo(960, 430, duration=2)
        time.sleep(3)
        
        pyautogui.moveTo(960, 510, duration=1)
        time.sleep(3)
        
        pyautogui.moveTo(960, 580, duration=1)
        time.sleep(3)
        
        pyautogui.moveTo(960, 540, duration=1.5)
        time.sleep(5)
        
        pyautogui.moveTo(1700, 950, duration=2)
        time.sleep(2)
        
        print("✓ CENA 02 concluída")
        
        # CENA 03: Arquitetura
        print("\n[CENA 03] Arquitetura...")
        time.sleep(3)
        
        pyautogui.moveTo(960, 680, duration=2)
        time.sleep(3)
        
        pyautogui.moveTo(960, 740, duration=1)
        time.sleep(3)
        
        pyautogui.moveTo(960, 540, duration=2)
        time.sleep(5)
        
        pyautogui.moveTo(960, 580, duration=1)
        time.sleep(2)
        
        print("✓ CENA 03 concluída")
        
        # ====================================================================
        # CENA 04: LOGIN (0:30)
        # ====================================================================
        print("\n" + "=" * 80)
        print("CENA 04: LOGIN (0:30)")
        print("=" * 80)
        
        print("\n[CENA 04] Login com credenciais...")
        time.sleep(1)
        
        # Clicar em "Advogado"
        pyautogui.moveTo(960, 680, duration=1.5)
        time.sleep(0.5)
        pyautogui.click()
        print("✓ Clicou em 'Advogado'")
        time.sleep(1.5)
        
        # Clicar em "Entrar"
        pyautogui.moveTo(960, 580, duration=1.5)
        time.sleep(0.5)
        pyautogui.click()
        print("✓ Clicou em 'Entrar'")
        time.sleep(3)
        
        # Aguardar dashboard
        pyautogui.moveTo(960, 540, duration=0)
        time.sleep(3)
        
        print("✓ CENA 04 concluída")
        
        # ====================================================================
        # CENA 05: DASHBOARD (0:30)
        # ====================================================================
        print("\n" + "=" * 80)
        print("CENA 05: DASHBOARD (0:30)")
        print("=" * 80)
        
        print("\n[CENA 05] Dashboard e navegação...")
        time.sleep(2)
        
        # Percorrer navbar
        navbar_items = [
            (200, 32, "Dashboard"),
            (310, 32, "Upload"),
            (400, 32, "Chat"),
            (480, 32, "Análise"),
            (570, 32, "Riscos"),
            (660, 32, "Automações"),
            (770, 32, "Revisões"),
            (870, 32, "Métricas"),
            (970, 32, "Comparação"),
        ]
        
        for x, y, name in navbar_items:
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.3)
        
        # Para nome/role
        pyautogui.moveTo(1750, 32, duration=2)
        time.sleep(2)
        
        # Para primeiro card
        pyautogui.moveTo(300, 300, duration=2)
        time.sleep(2)
        
        # Para botão Upload
        pyautogui.moveTo(1650, 120, duration=2)
        time.sleep(0.5)
        pyautogui.click()
        print("✓ Clicou em 'Upload PDF'")
        time.sleep(2)
        
        print("✓ CENA 05 concluída")
        
        # ====================================================================
        # CENA 06: UPLOAD DE CONTRATO (1:00)
        # ====================================================================
        print("\n" + "=" * 80)
        print("CENA 06: UPLOAD DE CONTRATO (1:00)")
        print("=" * 80)
        
        print("\n[CENA 06] Upload com processamento...")
        time.sleep(2)
        
        # Campo de título
        pyautogui.moveTo(960, 300, duration=1)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        
        # Digitar título
        pyautogui.typewrite("Contrato de Prestacao de Servicos - Demo", interval=0.05)
        time.sleep(0.5)
        
        # Área de upload
        pyautogui.moveTo(960, 450, duration=1)
        time.sleep(0.5)
        pyautogui.click()
        print("✓ Clicou em área de upload")
        time.sleep(1)
        
        # Aguardar seleção de arquivo (simulado)
        time.sleep(2)
        
        # Botão fazer upload
        pyautogui.moveTo(960, 650, duration=1.5)
        time.sleep(0.5)
        pyautogui.click()
        print("✓ Clicou em 'Fazer Upload'")
        time.sleep(5)  # Aguardar processamento
        
        # Tela de sucesso
        time.sleep(3)
        
        # Redirect para dashboard
        pyautogui.moveTo(960, 540, duration=0)
        time.sleep(3)
        
        print("✓ CENA 06 concluída")
        
        # ====================================================================
        # CENA 07: ANÁLISE (1:30)
        # ====================================================================
        print("\n" + "=" * 80)
        print("CENA 07: ANÁLISE (1:30)")
        print("=" * 80)
        
        print("\n[CENA 07] Análise - Resumo e Extração...")
        
        # Para Análise
        pyautogui.moveTo(480, 32, duration=2)
        time.sleep(0.5)
        pyautogui.click()
        print("✓ Clicou em 'Análise'")
        time.sleep(3)
        
        # Aguardar análise
        pyautogui.moveTo(1700, 950, duration=0)
        time.sleep(3)
        
        # Para resumo
        pyautogui.moveTo(960, 250, duration=2)
        time.sleep(3)
        
        # Para botão chat
        pyautogui.moveTo(1500, 250, duration=1.5)
        time.sleep(1)
        
        # Scroll para baixo
        pyautogui.scroll(-5, x=960, y=500)
        time.sleep(2)
        
        # Cards de extração
        cards = [(400, 500), (1400, 500), (400, 800), (1400, 800)]
        for x, y in cards:
            pyautogui.moveTo(x, y, duration=2)
            time.sleep(3)
        
        # Scroll para cima
        pyautogui.scroll(5, x=960, y=500)
        time.sleep(1)
        
        print("✓ CENA 07 concluída")
        
        # ====================================================================
        # CENA 08: CHAT COM AGENT ROUTER (1:30)
        # ====================================================================
        print("\n" + "=" * 80)
        print("CENA 08: CHAT COM AGENT ROUTER (1:30)")
        print("=" * 80)
        
        print("\n[CENA 08] Chat com roteamento...")
        
        # Clicar em "Iniciar Chat"
        pyautogui.click(1500, 250)
        print("✓ Clicou em 'Iniciar Chat'")
        time.sleep(3)
        
        # Aguardar chat
        pyautogui.moveTo(960, 540, duration=0)
        time.sleep(2)
        
        # Sidebar
        pyautogui.moveTo(150, 120, duration=2)
        time.sleep(2)
        
        # Conversa
        pyautogui.moveTo(150, 200, duration=1)
        time.sleep(2)
        
        # Campo de texto
        pyautogui.moveTo(960, 950, duration=2)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        
        # Digitar pergunta
        pyautogui.typewrite("Quais sao os riscos deste contrato?", interval=0.05)
        time.sleep(0.5)
        
        # Botão send
        pyautogui.moveTo(1750, 950, duration=1)
        time.sleep(0.5)
        pyautogui.click()
        print("✓ Clicou em Send")
        time.sleep(1)
        
        # Aguardar resposta
        pyautogui.moveTo(1700, 950, duration=0)
        time.sleep(5)
        
        # Resposta visível
        time.sleep(3)
        
        # Para resposta
        pyautogui.moveTo(800, 600, duration=2)
        time.sleep(3)
        
        # Para citações
        pyautogui.moveTo(800, 800, duration=1.5)
        time.sleep(3)
        
        # Scroll
        pyautogui.scroll(-2, x=960, y=600)
        time.sleep(1)
        
        # Disclaimer
        pyautogui.moveTo(800, 900, duration=1)
        time.sleep(3)
        
        # Posição neutra
        pyautogui.moveTo(1700, 950, duration=1.5)
        time.sleep(2)
        
        print("✓ CENA 08 concluída")
        
        # ====================================================================
        # CENA 09: ANÁLISE DE RISCOS (1:30)
        # ====================================================================
        print("\n" + "=" * 80)
        print("CENA 09: ANÁLISE DE RISCOS (1:30)")
        print("=" * 80)
        
        print("\n[CENA 09] Análise de Riscos...")
        
        # Para Riscos
        pyautogui.moveTo(570, 32, duration=2)
        time.sleep(0.5)
        pyautogui.click()
        print("✓ Clicou em 'Riscos'")
        time.sleep(3)
        
        # Aguardar página
        pyautogui.moveTo(960, 300, duration=0)
        time.sleep(2)
        
        # Botão Analyze
        pyautogui.moveTo(960, 400, duration=1.5)
        time.sleep(0.5)
        pyautogui.click()
        print("✓ Clicou em 'Analyze Risks'")
        time.sleep(5)
        
        # Resultado
        pyautogui.moveTo(1700, 950, duration=0)
        time.sleep(3)
        
        # Overall risk
        pyautogui.moveTo(960, 300, duration=2)
        time.sleep(3)
        
        # Risk card
        pyautogui.moveTo(960, 500, duration=1.5)
        time.sleep(3)
        
        # Sources
        pyautogui.moveTo(1100, 600, duration=1)
        time.sleep(0.5)
        pyautogui.click()
        print("✓ Clicou em 'Sources'")
        time.sleep(2)
        
        # Conteúdo expandido
        pyautogui.moveTo(960, 700, duration=1)
        time.sleep(3)
        
        # Scroll
        pyautogui.scroll(-3, x=960, y=600)
        time.sleep(1.5)
        time.sleep(2)
        
        # Disclaimer
        pyautogui.moveTo(960, 900, duration=2)
        time.sleep(3)
        
        # Posição neutra
        pyautogui.moveTo(1700, 950, duration=1.5)
        time.sleep(2)
        
        print("✓ CENA 09 concluída")
        
        # ====================================================================
        # CENA 10-14: AUTOMAÇÕES, REVISÕES, MÉTRICAS, COMPARAÇÃO E CONCLUSÃO
        # ====================================================================
        print("\n" + "=" * 80)
        print("CENA 10-14: AUTOMAÇÕES, REVISÕES, MÉTRICAS, COMPARAÇÃO E CONCLUSÃO")
        print("=" * 80)
        
        print("\n[CENA 10] Automações...")
        pyautogui.moveTo(660, 32, duration=2)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(3)
        
        pyautogui.moveTo(960, 300, duration=1.5)
        time.sleep(3)
        
        pyautogui.moveTo(300, 300, duration=1.5)
        time.sleep(2)
        
        pyautogui.moveTo(600, 350, duration=1.5)
        time.sleep(2)
        
        pyautogui.moveTo(1400, 350, duration=2)
        time.sleep(2)
        
        pyautogui.scroll(-3, x=960, y=600)
        time.sleep(1.5)
        time.sleep(2)
        
        pyautogui.moveTo(1700, 950, duration=2)
        time.sleep(1)
        
        print("✓ CENA 10 concluída")
        
        print("\n[CENA 11] Revisão Humana...")
        pyautogui.moveTo(770, 32, duration=2)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(3)
        
        pyautogui.moveTo(960, 400, duration=0)
        time.sleep(2)
        
        pyautogui.moveTo(300, 120, duration=2)
        time.sleep(1)
        
        pyautogui.moveTo(450, 120, duration=1)
        time.sleep(1)
        
        pyautogui.moveTo(250, 250, duration=2)
        time.sleep(2)
        
        pyautogui.click(250, 250)
        time.sleep(2)
        
        pyautogui.moveTo(1700, 950, duration=0)
        time.sleep(3)
        
        pyautogui.moveTo(1200, 400, duration=2)
        time.sleep(3)
        
        pyautogui.moveTo(1200, 800, duration=2)
        time.sleep(1)
        
        pyautogui.click(1200, 800)
        time.sleep(2)
        
        pyautogui.moveTo(1700, 950, duration=0)
        time.sleep(3)
        
        print("✓ CENA 11 concluída")
        
        print("\n[CENA 12] Métricas de Impacto...")
        pyautogui.moveTo(870, 32, duration=2)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(3)
        
        pyautogui.moveTo(960, 300, duration=0)
        time.sleep(2)
        
        pyautogui.moveTo(400, 300, duration=1.5)
        time.sleep(3)
        
        pyautogui.moveTo(1400, 300, duration=2)
        time.sleep(3)
        
        pyautogui.moveTo(400, 600, duration=2)
        time.sleep(3)
        
        pyautogui.moveTo(1400, 600, duration=2)
        time.sleep(3)
        
        pyautogui.scroll(-3, x=960, y=600)
        time.sleep(1.5)
        time.sleep(2)
        
        pyautogui.moveTo(960, 800, duration=2)
        time.sleep(3)
        
        pyautogui.moveTo(1700, 950, duration=2)
        time.sleep(2)
        
        print("✓ CENA 12 concluída")
        
        print("\n[CENA 13] Comparação de Contratos...")
        pyautogui.moveTo(970, 32, duration=2)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(3)
        
        pyautogui.moveTo(960, 300, duration=0)
        time.sleep(2)
        
        pyautogui.moveTo(400, 120, duration=1.5)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        
        pyautogui.moveTo(400, 180, duration=1)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        
        pyautogui.moveTo(1400, 120, duration=2)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        
        pyautogui.moveTo(1400, 180, duration=1)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        
        pyautogui.moveTo(960, 250, duration=1.5)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(5)
        
        pyautogui.moveTo(1700, 950, duration=0)
        time.sleep(3)
        
        pyautogui.moveTo(960, 400, duration=2)
        time.sleep(3)
        
        pyautogui.scroll(-4, x=960, y=600)
        time.sleep(2)
        time.sleep(2)
        
        pyautogui.moveTo(960, 700, duration=2)
        time.sleep(3)
        
        pyautogui.moveTo(1700, 950, duration=2)
        time.sleep(2)
        
        print("✓ CENA 13 concluída")
        
        print("\n[CENA 14] Conclusão / Encerramento...")
        pyautogui.moveTo(200, 32, duration=2)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(2)
        
        pyautogui.moveTo(960, 540, duration=0)
        time.sleep(3)
        
        pyautogui.moveTo(1750, 32, duration=2)
        time.sleep(2)
        
        pyautogui.moveTo(1750, 80, duration=1)
        time.sleep(1)
        
        pyautogui.click(1750, 80)
        time.sleep(2)
        
        pyautogui.moveTo(960, 540, duration=0)
        time.sleep(3)
        
        print("✓ CENA 14 concluída")
        
        # ====================================================================
        # CONCLUSÃO
        # ====================================================================
        print("\n" + "=" * 80)
        print("✅ GRAVAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 80)
        print("\nDuração total: ~12 minutos")
        print("Todas as 14 cenas foram executadas")
        print("\nPróximas etapas:")
        print("1. Parar a gravação de tela")
        print("2. Exportar vídeo em 1080p")
        print("3. Sincronizar áudio com narração")
        print("4. Revisar qualidade e transições")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n❌ Erro durante a gravação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
