# Guia de Retomada de Cenas — Legal AI Copilot

> Como regravar cenas específicas sem comprometer a continuidade do vídeo final.

---

## 1. Princípios de Continuidade

### Estado da Aplicação
- Antes de regravavar qualquer cena, garantir que o estado da aplicação seja idêntico ao da gravação original
- Documento selecionado, conversa ativa, filtros aplicados — tudo deve estar igual
- Se a cena original usou um documento específico, usar o mesmo

### Aparência
- Mesma roupa (se cena de webcam)
- Mesma iluminação
- Mesma posição da câmera
- Mesma configuração do navegador (zoom, tema, perfil)

### Áudio
- Mesmo microfone, mesma distância, mesmos filtros
- Mesmo tom e ritmo de voz
- Gravar no mesmo ambiente (mesmo eco, mesma temperatura)

---

## 2. Pontos de Corte por Cena

Cada cena tem pontos de entrada e saída definidos para permitir cortes limpos na edição.

### Cena 01 — Abertura

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Tela preta / fade in | 0s |
| **Saída** | Após "limitações" — pausa 2s | ~30s |
| **Corte limpo** | Início: 2s de silêncio antes da primeira palavra. Fim: 2s de silêncio após última palavra |

### Cena 02 — Problema

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Fade in / webcam ativa | 0s |
| **Saída** | Após "revisão humana" — pausa 2s | ~45s |
| **Corte limpo** | Início: 2s silêncio. Fim: 2s silêncio |

### Cena 03 — Arquitetura

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Fade in | 0s |
| **Saída** | Após "API key da OpenAI" — pausa 2s | ~45s |
| **Corte limpo** | Início: 2s silêncio. Fim: 2s silêncio |

### Cena 04 — Login

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Tela de login carregada e estática por 3s | 0s |
| **Saída** | Dashboard carregado e estático por 3s | ~30s |
| **Corte limpo** | Entrada: tela de login sem cursor movendo. Saída: dashboard sem cursor movendo |
| **Regravação** | Fazer logout, aguardar tela de login, regravar |

### Cena 05 — Dashboard

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Dashboard carregado, cursor parado, 3s | 0s |
| **Saída** | Antes de clicar "Upload PDF" — pausa 2s | ~30s |
| **Corte limpo** | Entrada: dashboard estático. Saída: cursor sobre o botão "Upload PDF" |
| **Regravação** | Navegar para `/dashboard`, aguardar carregamento, regravar |

### Cena 06 — Upload

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Tela de upload carregada, 3s | 0s |
| **Saída** | Dashboard com novo documento visível, 3s | ~60s |
| **Corte limpo** | Entrada: formulário vazio. Saída: dashboard atualizado |
| **Regravação** | Deletar o documento criado, voltar para `/upload`, regravar |
| **Atenção** | Se regravar, o título do documento deve ser o mesmo. Se o filename mudar (UUID), não é problema — o título é o que aparece na tela |

### Cena 07 — Análise

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Página de análise carregada, 3s | 0s |
| **Saída**** | Após mostrar todos os 4 cards, pausa 2s | ~90s |
| **Corte limpo** | Entrada: dropdown visível (ou documento já selecionado). Saída: página rolada até o final dos cards |
| **Regravação** | Navegar para `/analysis`, selecionar mesmo documento, regravar |

### Cena 08 — Chat

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Tela de chat carregada, 3s | 0s |
| **Saída** | Após mostrar resposta + citações + disclaimer, 3s | ~90s |
| **Corte limpo** | Entrada: chat vazio ou conversa selecionada. Saída: resposta completa visível |
| **Regravação** | Criar nova conversa ou reabrir a mesma. Se recriar conversa, o ID muda mas a tela é idêntica |
| **Atenção** | A resposta do agente pode variar ligeiramente entre execuções. Regravar até obter resposta similar |

### Cena 09 — Riscos

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Página de riscos carregada, 3s | 0s |
| **Saída** | Após mostrar disclaimer, 3s | ~90s |
| **Corte limpo** | Entrada: botão "Analyze Risks" visível. Saída: disclaimer visível |
| **Regravação** | Navegar para `/risks`, selecionar mesmo documento, regravar. A análise é determinística — mesmo resultado |

### Cena 10 — Automações

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Lista de automações carregada, 3s | 0s |
| **Saída** | Após mostrar links e botões, 3s | ~45s |
| **Corte limpo** | Entrada: lista estática. Saída: lista estática |
| **Regravação** | Navegar para `/automations`, regravar |

### Cena 11 — Revisões

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Lista de revisões carregada, 3s | 0s |
| **Saída** | Após confirmar revisão e mostrar histórico, 3s | ~60s |
| **Corte limpo** | Entrada: lista visível. Saída: histórico atualizado visível |
| **Regravação** | Se já revisou, o status mudou. Para regravar: criar nova análise via chat/upload, ou usar outra análise pendente |
| **Atenção** | A state machine é irreversível. Uma análise aprovada não volta a pendente. Planejar qual análise revisar |

### Cena 12 — Métricas

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Dashboard de métricas carregado, 3s | 0s |
| **Saída** | Após mostrar estimativa e aviso, 3s | ~45s |
| **Corte limpo** | Entrada: números carregados. Saída: aviso visível |
| **Regravação** | Navegar para `/insights`, regravar. Números podem mudar se novas análises foram criadas |

### Cena 13 — Comparação

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Página de comparação carregada, 3s | 0s |
| **Saída** | Após mostrar resultado, 3s | ~30s |
| **Corte limpo** | Entrada: dropdowns vazios. Saída: resultado visível |
| **Regravação** | Navegar para `/comparison`, selecionar mesmos documentos, regravar |

### Cena 14 — Encerramento

| Ponto | Descrição | Frame de referência |
|-------|-----------|---------------------|
| **Entrada** | Fade in / webcam | 0s |
| **Saída** | Fade out após 2s de silêncio | ~60s |
| **Corte limpo** | Início: 2s silêncio. Fim: 2s silêncio + fade |

---

## 3. Procedimento de Regravação

### Passo a Passo

1. **Identificar a cena a regravar** e marcar na checklist (06_RECORDING_CHECKLIST.md)
2. **Restaurar o estado da aplicação**:
   - Logout se necessário (Cena 04)
   - Navegar para a URL correta
   - Selecionar o mesmo documento/conversa
   - Aplicar os mesmos filtros
3. **Verificar aparência** (se webcam): mesma roupa, iluminação, posição
4. **Iniciar gravação no OBS** com a cena correta
5. **Aguardar 3s de tela estática** antes de falar
6. **Seguir o roteiro** normalmente
7. **Aguardar 3s de tela estática** ao final
8. **Parar gravação**
9. **Reproduzir e verificar**
10. **Substituir o arquivo original** se aprovado

### Nomeação de Arquivos de Retake

```
cena_04_login.mp4          ← original
cena_04_login_retake01.mp4 ← primeira retomada
cena_04_login_retake02.mp4 ← segunda retomada
```

Manter o original até o retake ser aprovado. Depois, renomear o retake aprovado para o nome padrão.

---

## 4. Cenas Críticas (Maior Risco de Retake)

| Cena | Risco | Motivo | Mitigação |
|------|-------|--------|-----------|
| 06 — Upload | Alto | Depende de processamento backend, pode falhar | Testar upload 3x antes de gravar |
| 08 — Chat | Alto | Resposta do agente pode variar | Gravar 3 tentativas, escolher a melhor |
| 11 — Revisões | Médio | State machine irreversível | Planejar qual análise revisar. Ter backup |
| 07 — Análise | Médio | Extração pode retornar vazia | Verificar documento antes. Ter documento backup |
| 09 — Riscos | Baixo | Análise é determinística | Mesmo resultado sempre |

---

## 5. Cenas Independentes (Fáceis de Regravar Isoladamente)

Estas cenas não dependem do estado de cenas anteriores e podem ser regravadas isoladamente:

- **Cena 01 — Abertura** (webcam apenas)
- **Cena 02 — Problema** (webcam apenas)
- **Cena 03 — Arquitetura** (webcam apenas)
- **Cena 14 — Encerramento** (webcam apenas)
- **Cena 05 — Dashboard** (navegação visual apenas)
- **Cena 10 — Automações** (navegação visual apenas)
- **Cena 12 — Métricas** (navegação visual apenas)

---

## 6. Ordem Recomendada de Gravação

Para minimizar retakes, gravar nesta ordem:

1. **Primeiro**: Cenas de webcam (01, 02, 03, 14) — sem dependência de aplicação
2. **Segundo**: Setup completo — login, upload, aguardar automação completar
3. **Terceiro**: Cenas de tela em sequência (04→05→06→07→08→09→10→11→12→13)
4. **Quarto**: Regravar qualquer cena que teve erro

Esta ordem permite que as automações rodem em background enquanto as cenas iniciais são gravadas, e garante que os dados estejam prontos para as cenas de Automações, Revisões e Métricas.
