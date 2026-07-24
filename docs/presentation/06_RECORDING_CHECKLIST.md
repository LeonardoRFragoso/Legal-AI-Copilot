# Checklist de Gravação — Legal AI Copilot

> Checklist completo: antes, durante e depois da gravação.

---

## 1. Pré-Gravação — Ambiente (24h antes)

### Servidor e Aplicação

- [ ] Backend rodando: `cd backend && source venv/bin/activate && uvicorn app.main:app --reload`
- [ ] Frontend rodando: `cd frontend && npm run dev`
- [ ] Backend acessível em `http://localhost:8000/docs` (Swagger UI)
- [ ] Frontend acessível em `http://localhost:5173`
- [ ] Migrations aplicadas: `alembic upgrade head`
- [ ] Seed executado: `ENVIRONMENT=development python -m app.seed`
- [ ] Demo check aprovado: `ENVIRONMENT=development python -m scripts.demo_check`
- [ ] VITE_DEMO_MODE=true no `.env` do frontend
- [ ] VITE_API_URL=http://localhost:8000 no `.env` do frontend
- [ ] OPENAI_API_KEY configurada (opcional — modo heurístico funciona sem ela)

### Dados de Demonstração

- [ ] Pelo menos 2 documentos uploaded (necessário para Comparação)
- [ ] Pelo menos 1 conversa com mensagens (para Chat)
- [ ] Pelo menos 1 análise de riscos executada (para Riscos)
- [ ] Pelo menos 1 automação completada (para Automações)
- [ ] Pelo menos 1 analysis record com revisão (para Revisões)
- [ ] Métricas populadas (para Insights)
- [ ] Arquivo PDF de demo acessível: `Contrato_Prestacao_Servicos_Teste.pdf`

### Navegador

- [ ] Google Chrome instalado e atualizado
- [ ] Perfil limpo criado ("Demo Profile")
- [ ] Histórico limpo
- [ ] Cache limpo
- [ ] Cookies limpos
- [ ] Preenchimento automático desabilitado
- [ ] Barra de favoritos oculta (Ctrl+Shift+B)
- [ ] Extensões desabilitadas
- [ ] Zoom em 100% (Ctrl+0)
- [ ] Tema claro

### Sistema Operacional

- [ ] Monitor em 1920×1080
- [ ] Escala/DPI em 100%
- [ ] Área de trabalho limpa (sem ícones)
- [ ] Papel de parede neutro (cor sólida)
- [ ] Dock/Barra de tarefas em auto-ocultar
- [ ] "Não perturbe" ativado
- [ ] Notificações de apps desabilitadas (Slack, Discord, Email)
- [ ] Notificações do navegador desabilitadas
- [ ] Telefone silenciado

---

## 2. Pré-Gravação — Equipamento (1h antes)

### OBS Studio

- [ ] OBS Studio instalado e atualizado
- [ ] Cena "Tela Cheia" configurada (Display Capture)
- [ ] Cena "Apresentador" configurada (Webcam)
- [ ] Resolução base: 1920×1080
- [ ] Resolução de saída: 1920×1080
- [ ] FPS: 30
- [ ] Bitrate: 6000 Kbps
- [ ] Encoder: x264 ou NVENC
- [ ] Formato de gravação: MKV
- [ ] Pasta de saída definida e com espaço suficiente (>5 GB)

### Áudio

- [ ] Microfone USB conectado
- [ ] Microfone testado (nível de pico entre -12 dB e -6 dB)
- [ ] Noise Gate configurado (threshold -40 dB)
- [ ] Noise Suppression (RNNoise) aplicado
- [ ] Compressor aplicado (ratio 3:1, threshold -18 dB)
- [ ] Ganho ajustado (+3 dB se necessário)
- [ ] Fones de ouvido conectados para monitoramento
- [ ] Sem ruído de fundo audível nos fones
- [ ] Áudio de desktop DESABILITADO (não capturar som do sistema)

### Webcam

- [ ] Webcam conectada e testada
- [ ] Posição no nível dos olhos
- [ ] Iluminação frontal e difusa
- [ ] Fundo neutro
- [ ] Enquadramento: head and shoulders
- [ ] Sem reflexos nos óculos (se usar)

### Backup

- [ ] Celular com app gravador de áudio pronto (fallback)
- [ ] Segundo monitor com roteiro aberto (ou impresso)

---

## 3. Pré-Gravação — Pessoal (30min antes)

- [ ] Roteiro lido 3x em voz alta
- [ ] Termos técnicos ensaiados
- [ ] Voz aquecida
- [ ] Água bebida (15 min antes)
- [ ] Evitado leite e café excessivo
- [ ] Roupa neutra vestida (sem estampas, sem vermelho)
- [ ] Cabelo arrumado
- [ ] Barba feita (se aplicável)
- [ ] Postura verificada

---

## 4. Durante a Gravação — Por Cena

### Antes de Cada Cena

- [ ] Cena correta selecionada no OBS
- [ ] URL correta no navegador (se cena de tela)
- [ ] Estado da aplicação correto (dados carregados, loading completo)
- [ ] 3 segundos de silêncio e tela estática antes de falar
- [ ] Respiro fundo

### Durante Cada Cena

- [ ] Seguir o roteiro de fala (04_VIDEO_SPEECH_SCRIPT.md)
- [ ] Seguir o roteiro de navegação (03_SCREEN_NAVIGATION_SCRIPT.md)
- [ ] Pausar conforme marcações [PAUSA Xs]
- [ ] Não usar fillers ("ééé", "hmm", "tipo")
- [ ] Mover cursor lentamente ao apontar elementos
- [ ] Aguardar loading completar antes de narrar resultado
- [ ] Manter volume e ritmo consistentes
- [ ] Nomear o arquivo do clipe: `cena_XX_nome.mp4`

### Após Cada Cena

- [ ] 3 segundos de silêncio e tela estática
- [ ] Parar gravação
- [ ] Reproduzir o clipe para verificar áudio e vídeo
- [ ] Se erro: registrar na lista de retakes e regravar
- [ ] Se OK: marcar cena como gravada

### Checklist por Cena

| Cena | Nome | Gravada | Aprovada |
|------|------|---------|----------|
| 01 | Abertura | [ ] | [ ] |
| 02 | Problema | [ ] | [ ] |
| 03 | Arquitetura | [ ] | [ ] |
| 04 | Login | [ ] | [ ] |
| 05 | Dashboard | [ ] | [ ] |
| 06 | Upload | [ ] | [ ] |
| 07 | Análise | [ ] | [ ] |
| 08 | Chat | [ ] | [ ] |
| 09 | Riscos | [ ] | [ ] |
| 10 | Automações | [ ] | [ ] |
| 11 | Revisões | [ ] | [ ] |
| 12 | Métricas | [ ] | [ ] |
| 13 | Comparação | [ ] | [ ] |
| 14 | Encerramento | [ ] | [ ] |

---

## 5. Pós-Gravação

### Verificação Imediata

- [ ] Todos os 14 clipes gravados
- [ ] Todos os clipes reproduzidos e verificados
- [ ] Áudio sem ruído, clipe ou queda em todos os clipes
- [ ] Vídeo sem lag, drop frame ou artefatos
- [ ] Nenhuma notificação apareceu durante a gravação
- [ ] Nenhum elemento externo visível (barra de tarefas, notificação, etc.)

### Backup

- [ ] Copiar todos os clipes para local secundário (HD externo, nuvem)
- [ ] Verificar integridade dos arquivos copiados
- [ ] Manter arquivos MKV originais (não converter ainda)

### Edição (se aplicável)

- [ ] Converter MKV para MP4 (sem re-encode: `ffmpeg -i input.mkv -c copy output.mp4`)
- [ ] Ordenar clipes conforme timeline (02_DEMO_TIMELINE.md)
- [ ] Adicionar transições (fade 0.5s entre cenas)
- [ ] Verificar áudio contínuo entre cortes
- [ ] Exportar versão final em 1080p, 30 FPS
- [ ] Verificar versão final em 720p (legibilidade)

### Limpeza

- [ ] Restaurar configurações do sistema (notificações, papel de parede, dock)
- [ ] Fechar OBS Studio
- [ ] Desconectar equipamentos (se necessário)
- [ ] Restaurar navegador (perfil normal)

---

## 6. Contingência — Se Algo Der Errado

| Problema | Ação |
|----------|------|
| Backend cai | Reiniciar: `uvicorn app.main:app --reload`. Regravar cena afetada |
| Frontend não carrega | Verificar `npm run dev`. Limpar cache: `rm -rf node_modules/.vite` |
| Login falha | Verificar seed: `python -m app.seed`. Verificar backend rodando |
| Upload falha | Verificar pasta `uploads/` com permissão. Tentar outro PDF |
| Análise retorna vazia | Tentar outro documento. Verificar se status é "ready" |
| Chat não responde | Verificar backend. Tentar pergunta mais simples |
| Riscos vazios | Documento pode não ter cláusulas problemáticas. Explicar na narração |
| Automação não aparece | Fazer novo upload para gerar automação |
| Revisões vazias | Fazer upload + chat para gerar analysis records |
| Métricas zeradas | Dados insuficientes. Fazer mais uploads e análises |
| Comparação falha | Verificar 2+ documentos. Tentar documentos diferentes |
| Áudio com ruído | Verificar filtros. Aumentar Noise Suppression. Regravar |
| Vídeo com lag | Baixar bitrate para 4000 Kbps. Fechar apps desnecessários |
| Notificação aparece | Regravar cena afetada. Reforçar "Não perturbe" |
