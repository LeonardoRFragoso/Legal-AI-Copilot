# Checklist Pré-Gravação — Legal AI Copilot

## Ambiente

- [ ] Backend iniciado (`cd backend && source venv/bin/activate && uvicorn app.main:app --reload`)
- [ ] Frontend iniciado (`cd frontend && npm run dev`)
- [ ] Banco resetado (`python -m scripts.demo_reset`) ou dados de demo carregados
- [ ] Migrations em head (`alembic upgrade head`)
- [ ] Seed executado (`python -m app.seed`) — usuários demo criados
- [ ] `OPENAI_API_KEY` configurada no `.env` (necessária para resumo, extração, Q&A)
- [ ] Webhook desativado (`AUTOMATION_WEBHOOK_ENABLED=false`) ou configurado
- [ ] `VITE_DEMO_MODE=true` no `.env` do frontend (credenciais demo visíveis)
- [ ] Documento sintético disponível (`Contrato_Prestacao_Servicos_Teste.pdf` ou `tests/fixtures/synthetic_contract.txt`)
- [ ] `demo_check.py` executado e todos os checks passaram

## Navegador

- [ ] Zoom em 110-125% para legibilidade em vídeo
- [ ] Resolução 1920x1080 ou superior
- [ ] Console do navegador fechado (F12)
- [ ] Apenas abas necessárias abertas
- [ ] Notificações desativadas (browser e sistema)
- [ ] Senhas não visíveis na gravação (autofill via botão demo, não digitar manualmente)
- [ ] Dados pessoais ocultos (email, fotos de perfil, favoritos)
- [ ] Tema do navegador consistente (claro ou escuro, não alternar)

## Fluxo — Pré-gravar para ter fallback

- [ ] Login como LAWYER (lawyer@demo.com) — testar antes
- [ ] Upload de documento — testar antes (pode demorar com API key)
- [ ] Automação concluída — ter pelo menos 1 AutomationRun COMPLETED
- [ ] Chat com Q&A — ter pelo menos 1 conversa com resposta e citações
- [ ] Análise de riscos — ter pelo menos 1 análise com riscos identificados
- [ ] Revisão humana — ter pelo menos 1 análise em PENDING_REVIEW
- [ ] Métricas — ter dados suficientes para dashboard não vazio
- [ ] Logout funcional — testar antes
- [ ] Login como ADMIN (opcional) — testar system-status

## Plano Alternativo (se algo falhar durante a gravação)

- [ ] Screenshots de todas as telas salvas como fallback
- [ ] Análise previamente gerada e aprovada disponível
- [ ] Automação já concluída (não depender de execução ao vivo)
- [ ] Resposta de Q&A salva (não depender de chamada à OpenAI ao vivo)
- [ ] Banco de demo restaurável (`demo_reset.py`) para re-gravar se necessário
- [ ] Script de fala impresso ou em segundo monitor

## Verificações Finais antes de pressionar Record

- [ ] Microfone testado
- [ ] Iluminação adequada
- [ ] Sem notificações de email/mensagem/telefone
- [ ] Disco espaço suficiente para gravação
- [ ] Software de gravação configurado (OBS, Loom, etc.)
- [ ] Cronômetro ou timer visível apenas para você
