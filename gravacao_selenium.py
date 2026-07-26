#!/usr/bin/env python3
"""
Script de Gravação com Selenium — Legal AI Copilot
Controla o navegador Chrome de verdade para executar as 14 cenas
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def main():
    print("=" * 80)
    print("GRAVAÇÃO COM SELENIUM — LEGAL AI COPILOT")
    print("=" * 80)
    print("\n⚠️  INSTRUÇÕES:")
    print("1. Inicie a gravação de tela AGORA (OBS, ScreenFlow, etc)")
    print("2. Aguarde 5 segundos para sincronização")
    print("3. O script controlará o navegador automaticamente")
    print("\n" + "=" * 80)
    
    # Aguardar 5 segundos
    print("\nAguardando 5 segundos para sincronização...")
    for i in range(5, 0, -1):
        print(f"  {i}...", end="\r")
        time.sleep(1)
    
    print("\n🎬 Iniciando gravação!\n")
    
    # Configurar Chrome
    chrome_options = Options()
    # Não usar headless para que seja visível
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Conectar ao Chrome existente
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Erro ao conectar ao Chrome: {e}")
        print("Tentando abrir novo Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # ====================================================================
        # CENA 01-03: TÍTULO, PROBLEMA E ARQUITETURA (1:45)
        # ====================================================================
        print("=" * 80)
        print("CENA 01-03: TÍTULO, PROBLEMA E ARQUITETURA (1:45)")
        print("=" * 80)
        
        print("\n[CENA 01] Título / Abertura...")
        driver.get("http://localhost:5173/login")
        time.sleep(3)
        print("✓ CENA 01 concluída")
        
        print("\n[CENA 02] Problema e Contexto...")
        time.sleep(5)
        print("✓ CENA 02 concluída")
        
        print("\n[CENA 03] Arquitetura...")
        time.sleep(3)
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
        try:
            advogado_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Advogado')]")
            advogado_btn.click()
            print("✓ Clicou em 'Advogado'")
            time.sleep(1.5)
        except Exception as e:
            print(f"✗ Erro ao clicar em Advogado: {e}")
        
        # Clicar em "Entrar"
        try:
            entrar_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
            entrar_btn.click()
            print("✓ Clicou em 'Entrar'")
            time.sleep(3)
        except Exception as e:
            print(f"✗ Erro ao clicar em Entrar: {e}")
        
        # Aguardar dashboard
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//nav"))
            )
            print("✓ Dashboard carregado")
        except Exception as e:
            print(f"✗ Erro ao carregar dashboard: {e}")
        
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
        
        # Clicar em "Upload PDF"
        try:
            upload_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload')]")
            upload_btn.click()
            print("✓ Clicou em 'Upload PDF'")
            time.sleep(2)
        except Exception as e:
            print(f"✗ Erro ao clicar em Upload: {e}")
        
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
        try:
            title_field = driver.find_element(By.XPATH, "//input[@placeholder='Título do Documento']")
            title_field.click()
            time.sleep(0.5)
            title_field.send_keys("Contrato de Prestação de Serviços — Demo")
            print("✓ Título preenchido")
            time.sleep(0.5)
        except Exception as e:
            print(f"✗ Erro ao preencher título: {e}")
        
        # Selecionar arquivo
        try:
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys("/home/leonardo/dev/Legal AI Copilot/test_contract.pdf")
            print("✓ Arquivo selecionado")
            time.sleep(2)
        except Exception as e:
            print(f"✗ Erro ao selecionar arquivo: {e}")
        
        # Clicar em "Fazer Upload"
        try:
            upload_submit = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload')]")
            upload_submit.click()
            print("✓ Clicou em 'Fazer Upload'")
            time.sleep(5)
        except Exception as e:
            print(f"✗ Erro ao clicar em Upload: {e}")
        
        # Aguardar sucesso
        time.sleep(3)
        
        # Redirect para dashboard
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//nav"))
            )
            print("✓ Redirect para dashboard")
        except Exception as e:
            print(f"✗ Erro ao redirecionar: {e}")
        
        time.sleep(3)
        print("✓ CENA 06 concluída")
        
        # ====================================================================
        # CENA 07: ANÁLISE (1:30)
        # ====================================================================
        print("\n" + "=" * 80)
        print("CENA 07: ANÁLISE (1:30)")
        print("=" * 80)
        
        print("\n[CENA 07] Análise - Resumo e Extração...")
        
        # Clicar em "Análise"
        try:
            analise_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Análise')]")
            analise_btn.click()
            print("✓ Clicou em 'Análise'")
            time.sleep(3)
        except Exception as e:
            print(f"✗ Erro ao clicar em Análise: {e}")
        
        # Aguardar análise
        time.sleep(3)
        
        # Scroll para baixo
        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(2)
        
        # Scroll para cima
        driver.execute_script("window.scrollBy(0, -400);")
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
        try:
            chat_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Chat')]")
            chat_btn.click()
            print("✓ Clicou em 'Iniciar Chat'")
            time.sleep(3)
        except Exception as e:
            print(f"✗ Erro ao clicar em Chat: {e}")
        
        # Aguardar chat
        time.sleep(2)
        
        # Campo de texto
        try:
            chat_input = driver.find_element(By.XPATH, "//input[@placeholder='Digite sua mensagem...']")
            chat_input.click()
            time.sleep(0.5)
            chat_input.send_keys("Quais são os riscos deste contrato?")
            print("✓ Pergunta digitada")
            time.sleep(0.5)
        except Exception as e:
            print(f"✗ Erro ao digitar pergunta: {e}")
        
        # Clicar em Send
        try:
            send_btn = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'send')]")
            send_btn.click()
            print("✓ Clicou em Send")
            time.sleep(1)
        except Exception as e:
            print(f"✗ Erro ao clicar em Send: {e}")
        
        # Aguardar resposta
        time.sleep(5)
        time.sleep(3)
        
        print("✓ CENA 08 concluída")
        
        # ====================================================================
        # CENA 09: ANÁLISE DE RISCOS (1:30)
        # ====================================================================
        print("\n" + "=" * 80)
        print("CENA 09: ANÁLISE DE RISCOS (1:30)")
        print("=" * 80)
        
        print("\n[CENA 09] Análise de Riscos...")
        
        # Clicar em "Riscos"
        try:
            riscos_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Riscos')]")
            riscos_btn.click()
            print("✓ Clicou em 'Riscos'")
            time.sleep(3)
        except Exception as e:
            print(f"✗ Erro ao clicar em Riscos: {e}")
        
        # Aguardar página
        time.sleep(2)
        
        # Clicar em "Analyze Risks"
        try:
            analyze_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Analyze')]")
            analyze_btn.click()
            print("✓ Clicou em 'Analyze Risks'")
            time.sleep(5)
        except Exception as e:
            print(f"✗ Erro ao clicar em Analyze: {e}")
        
        # Resultado
        time.sleep(3)
        
        # Scroll
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1.5)
        time.sleep(2)
        
        # Scroll para cima
        driver.execute_script("window.scrollBy(0, -300);")
        time.sleep(2)
        
        print("✓ CENA 09 concluída")
        
        # ====================================================================
        # CENA 10-14: AUTOMAÇÕES, REVISÕES, MÉTRICAS, COMPARAÇÃO E CONCLUSÃO
        # ====================================================================
        print("\n" + "=" * 80)
        print("CENA 10-14: AUTOMAÇÕES, REVISÕES, MÉTRICAS, COMPARAÇÃO E CONCLUSÃO")
        print("=" * 80)
        
        print("\n[CENA 10] Automações...")
        try:
            automacoes_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Automações')]")
            automacoes_btn.click()
            time.sleep(3)
        except Exception as e:
            print(f"✗ Erro ao clicar em Automações: {e}")
        
        time.sleep(3)
        print("✓ CENA 10 concluída")
        
        print("\n[CENA 11] Revisão Humana...")
        try:
            revisoes_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Revisões')]")
            revisoes_btn.click()
            time.sleep(3)
        except Exception as e:
            print(f"✗ Erro ao clicar em Revisões: {e}")
        
        time.sleep(3)
        print("✓ CENA 11 concluída")
        
        print("\n[CENA 12] Métricas de Impacto...")
        try:
            metricas_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Métricas')]")
            metricas_btn.click()
            time.sleep(3)
        except Exception as e:
            print(f"✗ Erro ao clicar em Métricas: {e}")
        
        time.sleep(3)
        print("✓ CENA 12 concluída")
        
        print("\n[CENA 13] Comparação de Contratos...")
        try:
            comparacao_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Comparação')]")
            comparacao_btn.click()
            time.sleep(3)
        except Exception as e:
            print(f"✗ Erro ao clicar em Comparação: {e}")
        
        time.sleep(3)
        print("✓ CENA 13 concluída")
        
        print("\n[CENA 14] Conclusão / Encerramento...")
        try:
            dashboard_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Dashboard')]")
            dashboard_btn.click()
            time.sleep(2)
        except Exception as e:
            print(f"✗ Erro ao clicar em Dashboard: {e}")
        
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
    finally:
        # Não fechar o navegador para que o usuário possa ver o resultado
        print("\nNavigador permanecerá aberto para revisão.")

if __name__ == "__main__":
    main()
