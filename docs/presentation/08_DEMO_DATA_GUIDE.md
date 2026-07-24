# Guia de Dados de Demonstração — Legal AI Copilot

> Instruções para preparar e manter os dados de demonstração para o vídeo de apresentação.

---

## 1. Usuários Demo

### Credenciais

| Perfil | Email | Senha | Role | Nome |
|--------|-------|-------|------|------|
| Advogado | `lawyer@demo.com` | `demo123456` | LAWYER | Advogado Demo |
| Admin | `admin@demo.com` | `admin123456` | ADMIN | Admin Demo |

### Criação

```bash
cd backend
source venv/bin/activate
ENVIRONMENT=development python -m app.seed
```

### Reset Completo (apaga todos os dados e recria usuários)

```bash
cd backend
source venv/bin/activate
ENVIRONMENT=development python -m scripts.demo_reset
```

> **Aviso**: `demo_reset` apaga TODOS os dados (documentos, conversas, mensagens, análises, revisões, automações). Usar apenas para resetar antes de preparar a demo.

### Verificação

```bash
cd backend
source venv/bin/activate
ENVIRONMENT=development python -m scripts.demo_check
```

Verifica: banco acessível, tabelas existentes, migrations, usuários demo, API key (opcional), build do frontend, documento de demo.

---

## 2. Documentos de Demonstração

### Arquivos PDF Disponíveis

| Arquivo | Localização | Uso recomendado |
|---------|-------------|-----------------|
| `Contrato_Prestacao_Servicos_Teste.pdf` | Raiz do projeto | Documento principal da demo |
| `Contrato_Prestacao_Servicos_Completo.pdf` | Raiz do projeto | Segundo documento para comparação |
| `contrato.pdf` | Raiz do projeto | Documento alternativo |
| `test_contract.pdf` | Raiz do projeto | Documento alternativo |

### Preparação de Documentos para a Demo

Para a demonstração completa, são necessários **pelo menos 2 documentos** (Comparação exige 2).

#### Documento 1 — Principal

1. Login como `lawyer@demo.com`
2. Navegar para `/upload`
3. Título: `Contrato de Prestação de Serviços — Demo`
4. Arquivo: `Contrato_Prestacao_Servicos_Teste.pdf`
5. Fazer upload
6. Aguardar processamento (status muda para "Pronto")

#### Documento 2 — Para Comparação

1. Navegar para `/upload`
2. Título: `Contrato de Prestação de Serviços — Versão 2`
3. Arquivo: `Contrato_Prestacao_Servicos_Completo.pdf` (ou `contrato.pdf`)
4. Fazer upload
5. Aguardar processamento

### Verificação de Documentos

Após upload, verificar no dashboard:
- Status "Pronto" (badge verde)
- Número de páginas correto
- Data de criação visível

---

## 3. Dados Necessários por Cena

### Cena 04 — Login
- **Necessário**: Usuários demo criados (seed)
- **Não necessário**: Dados pré-carregados

### Cena 05 — Dashboard
- **Necessário**: Pelo menos 1 documento uploaded
- **Ideal**: 2 documentos para mostrar lista mais rica

### Cena 06 — Upload
- **Necessário**: Arquivo PDF acessível
- **Resultado**: Novo documento no dashboard
- **Atenção**: Esta cena cria um documento novo. Se já há 2 documentos, após esta cena haverá 3 — o que é fine

### Cena 07 — Análise
- **Necessário**: Pelo menos 1 documento com status "Pronto"
- **Resultado**: Resumo e extração exibidos

### Cena 08 — Chat
- **Necessário**: Pelo menos 1 documento processado
- **Resultado**: Conversa com mensagens
- **Preparação**: Pode-se criar a conversa a partir da página de Análise (botão "Iniciar Chat") ou diretamente no Chat

### Cena 09 — Riscos
- **Necessário**: Pelo menos 1 documento processado
- **Resultado**: Análise de riscos com cards

### Cena 10 — Automações
- **Necessário**: Pelo menos 1 automação executada (criada automaticamente no upload)
- **Ideal**: Automação com status COMPLETED ou PARTIAL_SUCCESS
- **Se webhook desabilitado**: Status do webhook será "pending" — explicar na narração

### Cena 11 — Revisões
- **Necessário**: Pelo menos 1 AnalysisRecord
- **Como gerar**: Fazer upload (cria records de summary e risk) OU usar chat (cria records conforme tipo de análise)
- **Para demonstrar revisão**: Precisa de um record com status "generated" ou "pending_review"
- **Login como**: LAWYER ou ADMIN (apenas estes podem revisar)

### Cena 12 — Métricas
- **Necessário**: Dados agregados — documentos, análises, revisões
- **Ideal**: Pelo menos 2 documentos, 3+ análises, 1+ revisão
- **Se dados insuficientes**: Métricas mostrarão zeros. Fazer mais uploads e análises

### Cena 13 — Comparação
- **Necessário**: Pelo menos 2 documentos no sistema
- **Preparação**: Garantir que ambos têm status "Pronto"

---

## 4. Sequência de Preparação de Dados

Executar esta sequência **antes** de começar a gravar:

### Passo 1 — Reset e Seed

```bash
cd backend
source venv/bin/activate
ENVIRONMENT=development python -m scripts.demo_reset
```

### Passo 2 — Iniciar Servidores

```bash
# Terminal 1
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2
cd frontend && npm run dev
```

### Passo 3 — Upload de Documentos (via UI)

1. Login como `lawyer@demo.com` / `demo123456`
2. Upload `Contrato_Prestacao_Servicos_Teste.pdf` — título: "Contrato de Prestação de Serviços — Demo"
3. Upload `Contrato_Prestacao_Servicos_Completo.pdf` — título: "Contrato de Prestação de Serviços — Versão 2"
4. Aguardar ambos com status "Pronto" (ver no dashboard)

### Passo 4 — Gerar Análises

1. Ir para `/analysis`, selecionar Documento 1, aguardar carregamento
2. Ir para `/risks`, selecionar Documento 1, clicar "Analyze Risks", aguardar
3. Ir para `/comparison`, selecionar Doc 1 e Doc 2, clicar "Comparar", aguardar

### Passo 5 — Gerar Conversa de Chat

1. Ir para `/chat`, clicar "Nova Conversa"
2. Digitar: "Resuma este contrato"
3. Aguardar resposta
4. Digitar: "Quais são os riscos deste contrato?"
5. Aguardar resposta

### Passo 6 — Gerar Revisão (para Cena 11)

1. Ir para `/reviews`
2. Verificar se há analysis records (gerados pelos passos 4 e 5)
3. Se houver records com status "generated" ou "pending_review":
   - Clicar em um record
   - Aprovar com comentário: "Análise correta, cláusulas identificadas adequadamente"
4. Deixar pelo menos 1 record sem revisar para a gravação da Cena 11

### Passo 7 — Verificar Automações

1. Ir para `/automations`
2. Verificar que há runs com status COMPLETED ou PARTIAL_SUCCESS
3. Se houver runs FAILED, usar botão "Tentar Novamente"

### Passo 8 — Verificar Métricas

1. Ir para `/insights`
2. Verificar que os números não estão todos zerados
3. Se zerados, repetir passos 4–6 para gerar mais dados

### Passo 9 — Demo Check Final

```bash
cd backend
source venv/bin/activate
ENVIRONMENT=development python -m scripts.demo_check
```

---

## 5. Estado Ideal para Gravação

| Elemento | Quantidade | Estado |
|----------|-----------|--------|
| Documentos | 2–3 | Status "Pronto" |
| Conversas | 1–2 | Com mensagens |
| Análises | 3–5 | Records gerados |
| Riscos | 1+ | Análise executada |
| Revisões | 1 aprovada + 1 pendente | Para mostrar histórico e formulário |
| Automações | 2–3 | Completas ou sucesso parcial |
| Métricas | Populadas | Números não-zero |

---

## 6. Variáveis de Ambiente Relevantes

### Backend (`backend/.env`)

| Variável | Valor para demo | Impacto |
|----------|----------------|---------|
| `ENVIRONMENT` | `development` | Permite seed e demo_reset |
| `OPENAI_API_KEY` | Vazio ou chave real | Vazio = modo heurístico. Com chave = embeddings + LLM |
| `AUTOMATION_WEBHOOK_ENABLED` | `false` | Webhook não enviado (status "pending") |
| `SECRET_KEY` | Vazio (auto em dev) | JWT assinado com chave auto-gerada |

### Frontend (`frontend/.env`)

| Variável | Valor para demo | Impacto |
|----------|----------------|---------|
| `VITE_API_URL` | `http://localhost:8000` | URL do backend |
| `VITE_DEMO_MODE` | `true` | Mostra credenciais demo na tela de login |

---

## 7. Cenários de Modo

### Modo Heurístico (sem OpenAI API Key)

- Análise de riscos: heurística por palavras-chave
- Embeddings: não gerados (ou fixos)
- Chat: respostas baseadas em heurística
- **Recomendado para demo**: Funciona sem dependências externas

### Modo LLM (com OpenAI API Key)

- Análise de riscos: ainda heurística (não muda)
- Embeddings: gerados via OpenAI
- Chat: respostas podem usar LLM se configurado
- **Para demo**: Funciona, mas adiciona dependência de rede e latência

> **Recomendação**: Gravar em modo heurístico para evitar variações e dependências externas.

---

## 8. Backup e Restore

### Backup dos Dados (após preparação)

```bash
cp backend/legal_ai.db backend/legal_ai.db.backup
```

### Restore dos Dados (se algo der errado)

```bash
# Parar backend
cp backend/legal_ai.db.backup backend/legal_ai.db
# Reiniciar backend
```

> **Nota**: O arquivo do banco SQLite pode estar em `backend/legal_ai.db` ou em outro local conforme configuração. Verificar `backend/app/database.py` para confirmar o caminho.

---

## 9. Troubleshooting de Dados

| Problema | Causa | Solução |
|----------|-------|---------|
| Login falha | Usuários não criados | `python -m app.seed` |
| Sem documentos | Upload não feito ou falhou | Fazer upload via UI |
| Documento "Processando" indefinidamente | Backend parou durante processamento | Reiniciar backend. Se persistir, deletar documento e re-upload |
| Análise vazia | Documento sem texto extraído | Verificar se PDF tem texto (não é imagem). Usar outro PDF |
| Sem automações | Upload feito com backend parado | Re-upload com backend rodando |
| Sem analysis records | Nenhuma análise executada | Fazer upload + chat + risk analysis |
| Métricas zeradas | Dados insuficientes | Gerar mais análises e revisões |
| Revisões vazias | Sem records ou sem permissão | Login como LAWYER/ADMIN. Gerar records via upload/chat |
