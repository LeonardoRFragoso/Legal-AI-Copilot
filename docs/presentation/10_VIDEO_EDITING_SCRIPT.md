# Guia de Edição de Pós-Produção — Legal AI Copilot

> Documento completo para edição profissional do vídeo de apresentação.
> Qualquer editor pode montar o vídeo final seguindo estas instruções.
> Sincronizado com `02_DEMO_TIMELINE.md`, `03_SCREEN_NAVIGATION_SCRIPT.md` e `04_VIDEO_SPEECH_SCRIPT.md`.

---

## 1. Introdução

### Objetivo da Edição

Montar um vídeo de apresentação técnica do Legal AI Copilot, com 14 cenas gravadas independentemente, em um produto audiovisual coeso, profissional e fluido. O resultado deve permitir que um espectador compreenda o problema, a arquitetura, todas as funcionalidades demonstradas e as limitações do MVP.

### Duração Final Desejada

- **Alvo**: 12:30–13:30
- **Mínimo**: 11:00 (cortes agressivos em esperas)
- **Máximo**: 15:00 (pausas naturais preservadas)
- **Tolerância**: ±30s em relação ao alvo

### Ritmo

- **Abertura (Cenas 01–03)**: Ritmo moderado, pausas respiradas. O espectador precisa absorver contexto.
- **Demo principal (Cenas 04–09)**: Ritmo dinâmico, cortes mais frequentes. Mostrar ação e resultado sem enrolar.
- **Workflow (Cenas 10–11)**: Ritmo moderado. Explicar processos com clareza.
- **Métricas e Comparação (Cenas 12–13)**: Ritmo ágil. Apresentar dados sem demorar.
- **Encerramento (Cena 14)**: Ritmo moderado, tom reflexivo. Dar peso às limitações.

### Estilo

- **Visual**: Limpo, sem efeitos exagerados. Cortes secos predominam. Dissolves apenas em transições webcam↔tela.
- **Áudio**: Voz clara e natural. Sem trilha sonora de fundo. Sem efeitos sonoros.
- **Texto na tela**: Discreto, apenas quando agrega informação. Sem animações chamativas.
- **Cor**: Sem grading agressivo. Correção de white balance e exposição apenas se necessário.

### Softwares Compatíveis

| Software | Versão mínima | Compatibilidade |
|----------|---------------|-----------------|
| DaVinci Resolve | 18 | Total — todas as funções deste guia |
| Adobe Premiere Pro | 2023 | Total — todas as funções deste guia |
| CapCut Desktop | 3.0 | Total — todas as funções deste guia |
| Final Cut Pro | 10.7 | Total — todas as funções deste guia |

> **Nota**: Os termos de funcionalidade neste guia usam nomenclatura genérica. Adaptar para o software escolhido (ex: "cross dissolve" = "Dissolve" no Premiere, "Cross Dissolve" no Final Cut, "Dissolve" no CapCut).

---

## 2. Configuração do Projeto

### Vídeo

| Parâmetro | Valor |
|-----------|-------|
| Resolução da timeline | 1920×1080 |
| Aspect ratio | 16:9 |
| FPS | 30 |
| Codec de origem | H.264 (MKV convertido para MP4) |
| Codec de edição | ProRes 422 ou DNxHR (intermediário) |
| Color space | Rec.709 |
| Color depth | 8-bit |

### Áudio

| Parâmetro | Valor |
|-----------|-------|
| Sample rate | 48 kHz |
| Canais | Stereo |
| Bit depth | 24-bit |
| Volume alvo da voz | -16 LUFS (integrated) |
| True peak máximo | -1.5 dBTP |
| Volume do sistema (desktop) | -30 dB (se capturado) — geralmente não capturado |

### Exportação

| Parâmetro | Valor |
|-----------|-------|
| Formato | MP4 |
| Codec | H.264 (x264) |
| Resolução | 1920×1080 |
| FPS | 30 |
| Bitrate de vídeo | 8 Mbps (CBR) |
| Profile | High |
| Level | 4.0 |
| Codec de áudio | AAC |
| Bitrate de áudio | 192 Kbps |
| Sample rate de áudio | 48 kHz |
| Canais de áudio | Stereo |
| Container | MP4 |
| Nome do arquivo final | `legal_ai_copilot_demo.mp4` |

### Tamanho Estimado do Arquivo Final

- ~12:30 de vídeo a 8 Mbps vídeo + 192 Kbps áudio
- **Estimado**: ~750 MB – 850 MB

---

## 3. Linha do Tempo Completa

> Cada cena corresponde a um clipe gravado independente (ver `07_SCENE_RETAKE_GUIDE.md`).
> Os tempos abaixo são os tempos **na timeline final**, não no clipe original.

---

### Cena 01 — Abertura

| Campo | Valor |
|------|-------|
| **Número** | 01 |
| **Nome** | Abertura |
| **Tempo de início** | 00:00:00 |
| **Tempo de término** | 00:00:30 |
| **Duração na timeline** | 30s |
| **Arquivo de vídeo** | `cena_01_abertura.mp4` |
| **Trecho utilizado** | Do frame 0 (após 2s de silêncio inicial) até o final da fala + 2s de silêncio |
| **Tipo de corte na entrada** | Fade in from black — 0.5s |
| **Tipo de corte na saída** | Cross dissolve para Cena 02 — 0.5s |
| **Transição** | Fade in from black no início. Cross dissolve no fim. |
| **Tempo da transição** | 0.5s entrada, 0.5s saída |

**Instruções de edição:**
1. Importar `cena_01_abertura.mp4`
2. Cortar os primeiros 2s de silêncio (ou manter se o clipe já começa com tela estática)
3. Posicionar no início da timeline (00:00:00)
4. Aplicar fade in from black de 0.5s no início
5. Aplicar cross dissolve de 0.5s no final, sobrepondo com o início da Cena 02
6. Verificar que o áudio começa limpo, sem clique ou ruído no corte

---

### Cena 02 — Problema e Contexto

| Campo | Valor |
|------|-------|
| **Número** | 02 |
| **Nome** | Problema |
| **Tempo de início** | 00:00:30 |
| **Tempo de término** | 00:01:15 |
| **Duração na timeline** | 45s |
| **Arquivo de vídeo** | `cena_02_problema.mp4` |
| **Trecho utilizado** | Início da fala até final da fala + 2s de silêncio |
| **Tipo de corte na entrada** | Cross dissolve da Cena 01 — 0.5s |
| **Tipo de corte na saída** | Cross dissolve para Cena 03 — 0.5s |
| **Transição** | Cross dissolve entrada e saída |
| **Tempo da transição** | 0.5s entrada, 0.5s saída |

**Instruções de edição:**
1. Importar `cena_02_problema.mp4`
2. Cortar silêncio inicial e final (manter 1s de respiro em cada lado)
3. Sobrepor 0.5s com o final da Cena 01 (cross dissolve)
4. Sobrepor 0.5s com o início da Cena 03 (cross dissolve)
5. Verificar continuidade de áudio — a voz deve fluir naturalmente entre cenas

---

### Cena 03 — Arquitetura

| Campo | Valor |
|------|-------|
| **Número** | 03 |
| **Nome** | Arquitetura |
| **Tempo de início** | 00:01:15 |
| **Tempo de término** | 00:02:00 |
| **Duração na timeline** | 45s |
| **Arquivo de vídeo** | `cena_03_arquitetura.mp4` |
| **Trecho utilizado** | Início da fala até final da fala + 2s de silêncio |
| **Tipo de corte na entrada** | Cross dissolve da Cena 02 — 0.5s |
| **Tipo de corte na saída** | Cross dissolve para Cena 04 — 0.8s |
| **Transição** | Cross dissolve entrada. Cross dissolve mais longo na saída (transição webcam→tela). |
| **Tempo da transição** | 0.5s entrada, 0.8s saída |

**Instruções de edição:**
1. Importar `cena_03_arquitetura.mp4`
2. Cortar silêncio inicial e final
3. Sobrepor 0.5s com Cena 02 (cross dissolve)
4. Sobrepor 0.8s com Cena 04 (cross dissolve — transição webcam→tela de aplicação)
5. O dissolve mais longo (0.8s) suaviza a mudança de contexto (apresentador→tela)

---

### Cena 04 — Login

| Campo | Valor |
|------|-------|
| **Número** | 04 |
| **Nome** | Login |
| **Tempo de início** | 00:02:00 |
| **Tempo de término** | 00:02:30 |
| **Duração na timeline** | 30s |
| **Arquivo de vídeo** | `cena_04_login.mp4` |
| **Trecho utilizado** | 3s de tela estática (login carregado) → fala → clique "Advogado" → fala → clique "Entrar" → aguardar redirect → 3s de dashboard estático |
| **Tipo de corte na entrada** | Cross dissolve da Cena 03 — 0.8s |
| **Tipo de corte na saída** | Cut seco para Cena 05 |
| **Transição** | Cross dissolve na entrada (fim da transição webcam→tela). Cut seco na saída (dashboard já está visível). |
| **Tempo da transição** | 0.8s entrada, 0s saída (cut) |

**Instruções de edição:**
1. Importar `cena_04_login.mp4`
2. Garantir 3s de tela estática (login carregado) no início
3. Sobrepor 0.8s com Cena 03 (cross dissolve)
4. Cortar no frame em que o dashboard está totalmente carregado e estático
5. Cut seco para Cena 05 — ambas as cenas mostram o dashboard, então o corte é invisível se o estado for idêntico
6. **Atenção**: Se o estado do dashboard mudou entre as gravações (documentos diferentes), usar cross dissolve de 0.3s para suavizar

---

### Cena 05 — Dashboard

| Campo | Valor |
|------|-------|
| **Número** | 05 |
| **Nome** | Dashboard |
| **Tempo de início** | 00:02:30 |
| **Tempo de término** | 00:03:00 |
| **Duração na timeline** | 30s |
| **Arquivo de vídeo** | `cena_05_dashboard.mp4` |
| **Trecho utilizado** | Dashboard carregado e estático → fala apontando navbar → fala apontando usuário/role → 2s antes de clicar "Upload PDF" |
| **Tipo de corte na entrada** | Cut seco da Cena 04 (ou cross dissolve 0.3s se estado diferente) |
| **Tipo de corte na saída** | Cut seco para Cena 06 |
| **Transição** | Cut seco em ambos os lados. A ação de clicar "Upload PDF" serve como transição natural. |
| **Tempo da transição** | 0s entrada, 0s saída |

**Instruções de edição:**
1. Importar `cena_05_dashboard.mp4`
2. Garantir que o dashboard está totalmente carregado no frame inicial
3. Cortar qualquer silêncio inicial excessivo (manter 1s)
4. O final deve mostrar o cursor sobre o botão "Upload PDF" por 1–2s antes do corte
5. Cut seco para Cena 06 — o clique no botão ocorre no início da Cena 06

---

### Cena 06 — Upload de Contrato

| Campo | Valor |
|------|-------|
| **Número** | 06 |
| **Nome** | Upload |
| **Tempo de início** | 00:03:00 |
| **Tempo de término** | 00:04:00 |
| **Duração na timeline** | 60s |
| **Arquivo de vídeo** | `cena_06_upload.mp4` |
| **Trecho utilizado** | Tela de upload carregada → digitação do título → seleção de arquivo → clique "Fazer Upload" → loading → tela de sucesso → redirect para dashboard |
| **Tipo de corte na entrada** | Cut seco da Cena 05 |
| **Tipo de corte na saída** | Cut seco para Cena 07 |
| **Transição** | Cut seco em ambos os lados. A navegação entre páginas serve como transição natural. |
| **Tempo da transição** | 0s entrada, 0s saída |

**Instruções de edição:**
1. Importar `cena_06_upload.mp4`
2. **Cortes internos permitidos**:
   - Acelerar a digitação do título se for muito lenta (speed ramp 150–200%)
   - Cortar tempo entre seleção de arquivo e clique em "Fazer Upload" se houver hesitação
   - **NÃO cortar** a tela de "Processando..." — mostrar a transição para a tela de sucesso
   - **NÃO cortar** a tela de sucesso — deixar visível por 2s completos
3. O final deve mostrar o dashboard com o novo documento visível por 2–3s
4. Cut seco para Cena 07

---

### Cena 07 — Análise (Resumo + Extração)

| Campo | Valor |
|------|-------|
| **Número** | 07 |
| **Nome** | Análise |
| **Tempo de início** | 00:04:00 |
| **Tempo de término** | 00:05:30 |
| **Duração na timeline** | 90s |
| **Arquivo de vídeo** | `cena_07_analise.mp4` |
| **Trecho utilizado** | Página de análise → loading spinner → resumo → scroll para grid 2x2 → Partes → Datas → Valores → Cláusulas → botão "Iniciar Chat" |
| **Tipo de corte na entrada** | Cut seco da Cena 06 |
| **Tipo de corte na saída** | Cross dissolve para Cena 08 — 0.3s |
| **Transição** | Cut seco na entrada. Cross dissolve curto na saída (transição entre páginas via botão "Iniciar Chat"). |
| **Tempo da transição** | 0s entrada, 0.3s saída |

**Instruções de edição:**
1. Importar `cena_07_analise.mp4`
2. **Cortes internos permitidos**:
   - Acelerar o loading spinner se durar mais de 5s (speed ramp ou cortar para o resultado)
   - **NÃO cortar** o momento em que o resumo aparece — mostrar a transição
   - Acelerar o scroll entre os 4 cards se for muito lento (150% speed)
   - **NÃO cortar** a aparição de cada card — o espectador precisa ver cada um
3. Deixar 2s no final com a página totalmente carregada e os cards visíveis
4. Cross dissolve de 0.3s para Cena 08

---

### Cena 08 — Chat com Agent Router

| Campo | Valor |
|------|-------|
| **Número** | 08 |
| **Nome** | Chat |
| **Tempo de início** | 00:05:30 |
| **Tempo de término** | 00:07:00 |
| **Duração na timeline** | 90s |
| **Arquivo de vídeo** | `cena_08_chat.mp4` |
| **Trecho utilizado** | Tela de chat → sidebar de conversas → digitação da pergunta → send → aguardar resposta → resposta estruturada → citações → disclaimer |
| **Tipo de corte na entrada** | Cross dissolve da Cena 07 — 0.3s |
| **Tipo de corte na saída** | Cut seco para Cena 09 |
| **Transição** | Cross dissolve curto na entrada. Cut seco na saída. |
| **Tempo da transição** | 0.3s entrada, 0s saída |

**Instruções de edição:**
1. Importar `cena_08_chat.mp4`
2. **Cortes internos permitidos**:
   - Acelerar a digitação da pergunta se for muito lenta (150–200% speed)
   - **NÃO cortar** o momento de envio da mensagem — mostrar o clique no botão Send
   - **NÃO cortar** o aparecimento da resposta — o espectador precisa ver a resposta chegando
   - Se a resposta demorar mais de 8s para aparecer, considerar cortar o meio do loading (jump cut suave ou cross dissolve de 0.2s)
   - **NÃO cortar** as citações — mostrar por pelo menos 3s
   - **NÃO cortar** o disclaimer — mostrar por pelo menos 2s
3. Deixar 3s no final com a resposta completa visível
4. Cut seco para Cena 09

---

### Cena 09 — Análise de Riscos

| Campo | Valor |
|------|-------|
| **Número** | 09 |
| **Nome** | Riscos |
| **Tempo de início** | 00:07:00 |
| **Tempo de término** | 00:08:30 |
| **Duração na timeline** | 90s |
| **Arquivo de vídeo** | `cena_09_riscos.mp4` |
| **Trecho utilizado** | Página de riscos → seleção de documento → clique "Analyze Risks" → loading → overall risk card → risk cards → expandir "Sources" → disclaimer |
| **Tipo de corte na entrada** | Cut seco da Cena 08 |
| **Tipo de corte na saída** | Cut seco para Cena 10 |
| **Transição** | Cut seco em ambos os lados. |
| **Tempo da transição** | 0s entrada, 0s saída |

**Instruções de edição:**
1. Importar `cena_09_riscos.mp4`
2. **Cortes internos permitidos**:
   - Acelerar o loading da análise de riscos se durar mais de 5s (speed ramp ou cortar para o resultado)
   - **NÃO cortar** o aparecimento do overall risk card — mostrar a transição
   - Acelerar o scroll entre risk cards se houver muitos (150% speed)
   - **NÃO cortar** a expansão de "Sources" — mostrar o clique e o conteúdo aparecendo
   - **NÃO cortar** o disclaimer — mostrar por pelo menos 2s
3. Deixar 3s no final com a página totalmente visível
4. Cut seco para Cena 10

---

### Cena 10 — Automações

| Campo | Valor |
|------|-------|
| **Número** | 10 |
| **Nome** | Automações |
| **Tempo de início** | 00:08:30 |
| **Tempo de término** | 00:09:15 |
| **Duração na timeline** | 45s |
| **Arquivo de vídeo** | `cena_10_automacoes.mp4` |
| **Trecho utilizado** | Lista de automações → cards com status → barra de progresso → webhook status → links → filtro → botão "Tentar Novamente" (se houver) |
| **Tipo de corte na entrada** | Cut seco da Cena 09 |
| **Tipo de corte na saída** | Cut seco para Cena 11 |
| **Transição** | Cut seco em ambos os lados. |
| **Tempo da transição** | 0s entrada, 0s saída |

**Instruções de edição:**
1. Importar `cena_10_automacoes.mp4`
2. **Cortes internos permitidos**:
   - Acelerar o scroll entre os cards de automação se houver muitos (150% speed)
   - **NÃO cortar** a aparição dos cards — o espectador precisa ver os status badges
   - Se houver runs com status diferente, garantir que pelo menos um COMPLETED e um FAILED/PARTIAL_SUCCESS sejam visíveis
3. Deixar 2s no final com a lista estática
4. Cut seco para Cena 11

---

### Cena 11 — Revisão Humana

| Campo | Valor |
|------|-------|
| **Número** | 11 |
| **Nome** | Revisões |
| **Tempo de início** | 00:09:15 |
| **Tempo de término** | 00:10:15 |
| **Duração na timeline** | 60s |
| **Arquivo de vídeo** | `cena_11_revisoes.mp4` |
| **Trecho utilizado** | Lista de análises → filtros → clicar em uma análise → painel de detalhe → histórico → clicar "Aprovar" → digitar comentário → "Confirmar Revisão" → histórico atualizado |
| **Tipo de corte na entrada** | Cut seco da Cena 10 |
| **Tipo de corte na saída** | Cut seco para Cena 12 |
| **Transição** | Cut seco em ambos os lados. |
| **Tempo da transição** | 0s entrada, 0s saída |

**Instruções de edição:**
1. Importar `cena_11_revisoes.mp4`
2. **Cortes internos permitidos**:
   - Acelerar a digitação do comentário de revisão (150–200% speed)
   - **NÃO cortar** o clique em uma análise da lista — mostrar o painel de detalhe abrindo
   - **NÃO cortar** o histórico de revisões — mostrar por pelo menos 3s
   - **NÃO cortar** o clique em "Aprovar" e "Confirmar Revisão" — mostrar a ação
   - **NÃO cortar** o histórico atualizado após a revisão — mostrar por 2s
3. Deixar 2s no final com o histórico atualizado visível
4. Cut seco para Cena 12

---

### Cena 12 — Métricas de Impacto

| Campo | Valor |
|------|-------|
| **Número** | 12 |
| **Nome** | Métricas |
| **Tempo de início** | 00:10:15 |
| **Tempo de término** | 00:11:00 |
| **Duração na timeline** | 45s |
| **Arquivo de vídeo** | `cena_12_metricas.mp4` |
| **Trecho utilizado** | Dashboard de métricas → 4 cards superiores → grid 2x2 → estimativa de produtividade → aviso |
| **Tipo de corte na entrada** | Cut seco da Cena 11 |
| **Tipo de corte na saída** | Cut seco para Cena 13 |
| **Transição** | Cut seco em ambos os lados. |
| **Tempo da transição** | 0s entrada, 0s saída |

**Instruções de edição:**
1. Importar `cena_12_metricas.mp4`
2. **Cortes internos permitidos**:
   - Acelerar o scroll entre as seções do dashboard (150% speed)
   - **NÃO cortar** os 4 cards superiores — o espectador precisa ver os números
   - **NÃO cortar** o grid 2x2 — mostrar cada visualização por pelo menos 2s
   - **NÃO cortar** o aviso de estimativa — mostrar por pelo menos 3s (é uma mensagem importante)
3. Deixar 2s no final com o dashboard totalmente visível
4. Cut seco para Cena 13

---

### Cena 13 — Comparação de Contratos

| Campo | Valor |
|------|-------|
| **Número** | 13 |
| **Nome** | Comparação |
| **Tempo de início** | 00:11:00 |
| **Tempo de término** | 00:11:30 |
| **Duração na timeline** | 30s |
| **Arquivo de vídeo** | `cena_13_comparacao.mp4` |
| **Trecho utilizado** | Página de comparação → selecionar Documento A → selecionar Documento B → clicar "Comparar Documentos" → loading → resultado |
| **Tipo de corte na entrada** | Cut seco da Cena 12 |
| **Tipo de corte na saída** | Cross dissolve para Cena 14 — 0.8s |
| **Transição** | Cut seco na entrada. Cross dissolve mais longo na saída (transição tela→webcam). |
| **Tempo da transição** | 0s entrada, 0.8s saída |

**Instruções de edição:**
1. Importar `cena_13_comparacao.mp4`
2. **Cortes internos permitidos**:
   - Acelerar a seleção dos documentos nos dropdowns se for muito lenta (150% speed)
   - **NÃO cortar** o clique em "Comparar Documentos" — mostrar a ação
   - Acelerar o loading se durar mais de 5s (speed ramp ou cortar para o resultado)
   - **NÃO cortar** o aparecimento do resultado — mostrar por pelo menos 3s
3. Deixar 2s no final com o resultado visível
4. Cross dissolve de 0.8s para Cena 14 (transição tela→webcam)

---

### Cena 14 — Encerramento

| Campo | Valor |
|------|-------|
| **Número** | 14 |
| **Nome** | Encerramento |
| **Tempo de início** | 00:11:30 |
| **Tempo de término** | 00:12:30 |
| **Duração na timeline** | 60s |
| **Arquivo de vídeo** | `cena_14_encerramento.mp4` |
| **Trecho utilizado** | Início da fala sobre limitações → lista de limitações → modo heurístico → conclusão → 2s de silêncio |
| **Tipo de corte na entrada** | Cross dissolve da Cena 13 — 0.8s |
| **Tipo de corte na saída** | Fade out to black — 1.0s |
| **Transição** | Cross dissolve na entrada (fim da transição tela→webcam). Fade out to black no fim. |
| **Tempo da transição** | 0.8s entrada, 1.0s saída |

**Instruções de edição:**
1. Importar `cena_14_encerramento.mp4`
2. Cortar silêncio inicial (manter 1s)
3. Sobrepor 0.8s com Cena 13 (cross dissolve)
4. **NÃO cortar** nenhuma parte da fala — todas as limitações devem ser mencionadas
5. Manter 2s de silêncio no final após a última palavra
6. Aplicar fade out to black de 1.0s
7. Garantir que o áudio fade out seja suave (não cortar abruptamente)

---

### Resumo da Timeline

| Cena | Início | Fim | Duração | Entrada | Saída |
|------|--------|-----|---------|---------|-------|
| 01 | 00:00:00 | 00:00:30 | 30s | Fade in 0.5s | X-Dissolve 0.5s |
| 02 | 00:00:30 | 00:01:15 | 45s | X-Dissolve 0.5s | X-Dissolve 0.5s |
| 03 | 00:01:15 | 00:02:00 | 45s | X-Dissolve 0.5s | X-Dissolve 0.8s |
| 04 | 00:02:00 | 00:02:30 | 30s | X-Dissolve 0.8s | Cut |
| 05 | 00:02:30 | 00:03:00 | 30s | Cut | Cut |
| 06 | 00:03:00 | 00:04:00 | 60s | Cut | Cut |
| 07 | 00:04:00 | 00:05:30 | 90s | Cut | X-Dissolve 0.3s |
| 08 | 00:05:30 | 00:07:00 | 90s | X-Dissolve 0.3s | Cut |
| 09 | 00:07:00 | 00:08:30 | 90s | Cut | Cut |
| 10 | 00:08:30 | 00:09:15 | 45s | Cut | Cut |
| 11 | 00:09:15 | 00:10:15 | 60s | Cut | Cut |
| 12 | 00:10:15 | 00:11:00 | 45s | Cut | Cut |
| 13 | 00:11:00 | 00:11:30 | 30s | Cut | X-Dissolve 0.8s |
| 14 | 00:11:30 | 00:12:30 | 60s | X-Dissolve 0.8s | Fade out 1.0s |

---

## 4. Sincronização da Fala

> Referência cruzada com `04_VIDEO_SPEECH_SCRIPT.md`.
> As marcações abaixo indicam o que acontece na **imagem** em cada momento da **fala**.

### Cena 01 — Abertura

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| 2s iniciais (silêncio) | Webcam estática | Sim | Não |
| "Este é o Legal AI Copilot..." | Webcam | Sim | Não |
| [PAUSA 1s] | Webcam | Sim | Não |
| "Nesta demonstração, vou percorrer..." | Webcam | Sim | Não |
| 2s finais (silêncio) | Webcam | Sim | Não |

### Cena 02 — Problema

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| "A análise manual de contratos..." | Webcam | Sim | Não |
| [PAUSA 1s] | Webcam | Sim | Não |
| "O Legal AI Copilot aborda..." | Webcam | Sim | Não |
| 2s finais (silêncio) | Webcam | Sim | Não |

### Cena 03 — Arquitetura

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| "A stack do projeto inclui..." | Webcam/diagrama | Sim | Não |
| [PAUSA 1s] | Webcam | Sim | Não |
| "A autenticação usa JWT..." | Webcam | Sim | Não |
| [PAUSA 1s] | Webcam | Sim | Não |
| "O agent router é determinístico..." | Webcam | Sim | Não |
| 2s finais (silêncio) | Webcam | Sim | Não |

### Cena 04 — Login

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| [TRANSIÇÃO] | Tela de login carregando | Não | Sim |
| 3s tela estática | Tela de login | Não | Sim |
| "A tela de login oferece dois perfis..." | Tela de login | Não | Sim |
| [CLICAR "Advogado"] | Tela de login — campos preenchidos | Não | Sim |
| "Vou usar o perfil de advogado..." | Tela de login | Não | Sim |
| [CLICAR "Entrar"] | Tela de login → redirect | Não | Sim |
| "O sistema autentica com JWT..." | Dashboard carregando | Não | Sim |
| 3s dashboard estático | Dashboard | Não | Sim |

### Cena 05 — Dashboard

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| "O dashboard lista todos os documentos..." | Dashboard — cards visíveis | Não | Sim |
| [APONTAR navbar] | Cursor move-se sobre a navbar | Não | Sim |
| "A barra de navegação superior..." | Navbar destacada | Não | Sim |
| [APONTAR usuário/role] | Cursor move-se para canto direito | Não | Sim |
| "No canto direito, vemos o nome..." | Nome e role badge visíveis | Não | Sim |
| 2s antes de clicar "Upload PDF" | Cursor sobre botão "Upload PDF" | Não | Sim |

### Cena 06 — Upload

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| [CLICAR "Upload PDF"] | Navegação para /upload | Não | Sim |
| "Vou fazer o upload de um contrato..." | Tela de upload | Não | Sim |
| [DIGITAR título] | Campo sendo preenchido | Não | Sim |
| [SELECIONAR PDF] | File picker → arquivo selecionado | Não | Sim |
| [CLICAR "Fazer Upload"] | Botão mostra "Processando..." | Não | Sim |
| "O processamento extrai o texto..." | Loading / "Processando..." | Não | Sim |
| [AGUARDAR sucesso] | Tela verde com CheckCircle | Não | Sim |
| "Upload concluído. O documento já aparece..." | Dashboard com novo documento | Não | Sim |

### Cena 07 — Análise

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| [CLICAR "Análise"] | Navegação para /analysis | Não | Sim |
| [SELECIONAR documento] | Dropdown — documento selecionado | Não | Sim |
| "A página de análise gera um resumo..." | Loading spinner | Não | Sim |
| [APONTAR card de resumo] | Card de resumo visível | Não | Sim |
| "O resumo é gerado automaticamente..." | Texto do resumo | Não | Sim |
| [ROLAR para baixo] | Scroll suave para grid 2x2 | Não | Sim |
| "Abaixo, temos quatro cards..." | Grid 2x2 visível | Não | Sim |
| [APONTAR Partes] | Card "Partes Envolvidas" | Não | Sim |
| "As partes identificadas incluem..." | Conteúdo do card | Não | Sim |
| [APONTAR Datas] | Card "Datas Importantes" | Não | Sim |
| "As datas extraídas incluem..." | Conteúdo do card | Não | Sim |
| [APONTAR Valores] | Card "Valores" | Não | Sim |
| "Os valores monetários são identificados..." | Conteúdo do card | Não | Sim |
| [APONTAR Cláusulas] | Card "Cláusulas Importantes" | Não | Sim |
| "Cada cláusula tem um badge de risco..." | Badges de risco visíveis | Não | Sim |

### Cena 08 — Chat

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| [CLICAR "Iniciar Chat" ou /chat] | Navegação para /chat | Não | Sim |
| "O chat permite interagir..." | Tela de chat | Não | Sim |
| [APONTAR sidebar] | Sidebar com conversas | Não | Sim |
| "A barra lateral mostra conversas..." | Sidebar destacada | Não | Sim |
| [DIGITAR pergunta] | Campo de texto sendo preenchido | Não | Sim |
| [CLICAR Send] | Mensagem enviada | Não | Sim |
| "O agent router classifica a intenção..." | Loading / aguardando resposta | Não | Sim |
| [APONTAR resposta estruturada] | Resposta do assistente | Não | Sim |
| "A resposta inclui riscos identificados..." | Risk cards na resposta | Não | Sim |
| [APONTAR citações] | Citações abaixo da resposta | Não | Sim |
| "Cada resposta inclui citações..." | Citações visíveis | Não | Sim |
| [APONTAR disclaimer] | Disclaimer ao final | Não | Sim |
| "E um disclaimer jurídico..." | Disclaimer visível | Não | Sim |
| 3s resposta completa | Tela de chat estática | Não | Sim |

### Cena 09 — Riscos

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| [CLICAR "Riscos"] | Navegação para /risks | Não | Sim |
| [SELECIONAR documento] | Dropdown — documento selecionado | Não | Sim |
| "A página de análise de riscos..." | Tela de riscos | Não | Sim |
| [CLICAR "Analyze Risks"] | Botão clicado | Não | Sim |
| Loading | Spinner de análise | Não | Sim |
| [APONTAR overall risk] | Card de Overall Risk | Não | Sim |
| "O resultado mostra um risco geral..." | Overall risk visível | Não | Sim |
| [APONTAR risk cards] | Lista de risk cards | Não | Sim |
| "Cada risco identificado tem severidade..." | Risk cards visíveis | Não | Sim |
| [CLICAR "Sources"] | Sources expandindo | Não | Sim |
| "As citações mostram o trecho exato..." | Sources expandidas | Não | Sim |
| [APONTAR disclaimer] | Disclaimer | Não | Sim |
| "É importante destacar que esta análise é heurística..." | Disclaimer visível | Não | Sim |
| 3s página estática | Tela de riscos completa | Não | Sim |

### Cena 10 — Automações

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| [CLICAR "Automações"] | Navegação para /automations | Não | Sim |
| "Cada upload dispara uma automação..." | Lista de automações | Não | Sim |
| [APONTAR cards] | Cards de automação | Não | Sim |
| "Cada run mostra o status..." | Status badges visíveis | Não | Sim |
| [APONTAR filtro] | Filtro de status | Não | Sim |
| "É possível filtrar por status..." | Filtro destacado | Não | Sim |
| [APONTAR links] | Links "Ver documento" e "Ver riscos" | Não | Sim |
| "Cada run tem links diretos..." | Links visíveis | Não | Sim |
| 2s tela estática | Lista de automações | Não | Sim |

### Cena 11 — Revisões

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| [CLICAR "Revisões"] | Navegação para /reviews | Não | Sim |
| "A revisão humana é o controle de qualidade..." | Lista de análises | Não | Sim |
| [APONTAR lista] | Cards na lista à esquerda | Não | Sim |
| "A lista mostra cada análise..." | Lista visível | Não | Sim |
| [CLICAR em uma análise] | Painel de detalhe abrindo | Não | Sim |
| "O painel de detalhe mostra..." | Detalhe da análise | Não | Sim |
| [APONTAR histórico] | Histórico de revisões | Não | Sim |
| "O histórico é append-only..." | Histórico visível | Não | Sim |
| [CLICAR "Aprovar"] | Botão selecionado | Não | Sim |
| [DIGITAR comentário] | Campo sendo preenchido | Não | Sim |
| [CLICAR "Confirmar Revisão"] | Revisão enviada | Não | Sim |
| "A state machine controla o fluxo..." | Histórico atualizado | Não | Sim |
| 2s tela estática | Histórico atualizado visível | Não | Sim |

### Cena 12 — Métricas

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| [CLICAR "Métricas"] | Navegação para /insights | Não | Sim |
| "O dashboard de métricas agrega..." | Dashboard de métricas | Não | Sim |
| [APONTAR 4 cards] | Cards superiores | Não | Sim |
| "Os cards superiores mostram..." | Números visíveis | Não | Sim |
| [APONTAR grid 2x2] | Grid de visualizações | Não | Sim |
| "Abaixo, quatro visualizações..." | Grid visível | Não | Sim |
| [APONTAR estimativa] | Card de estimativa | Não | Sim |
| "A estimativa de produtividade compara..." | Estimativa visível | Não | Sim |
| [APONTAR aviso] | Aviso em itálico | Não | Sim |
| "Administradores veem métricas globais..." | Aviso visível | Não | Sim |
| 2s tela estática | Dashboard completo | Não | Sim |

### Cena 13 — Comparação

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| [CLICAR "Comparação"] | Navegação para /comparison | Não | Sim |
| "A comparação permite analisar..." | Tela de comparação | Não | Sim |
| [SELECIONAR Documento A] | Dropdown A selecionado | Não | Sim |
| [SELECIONAR Documento B] | Dropdown B selecionado | Não | Sim |
| [CLICAR "Comparar Documentos"] | Botão clicado | Não | Sim |
| Loading | "Comparando..." | Não | Sim |
| "O resultado destaca semelhanças..." | Resultado visível | Não | Sim |
| 2s resultado estático | Resultado da comparação | Não | Sim |

### Cena 14 — Encerramento

| Momento da fala | Imagem | Webcam | Tela |
|----------------|--------|--------|------|
| [TRANSIÇÃO] | Cross dissolve tela→webcam | Sim | Não |
| "Para concluir, é importante ser transparente..." | Webcam | Sim | Não |
| [PAUSA 1s] | Webcam | Sim | Não |
| "A análise de riscos é heurística..." | Webcam | Sim | Não |
| [PAUSA 1s] | Webcam | Sim | Não |
| "O sistema funciona em modo heurístico..." | Webcam | Sim | Não |
| [PAUSA 1s] | Webcam | Sim | Não |
| "O Legal AI Copilot demonstra um fluxo completo..." | Webcam | Sim | Não |
| [PAUSA 2s] | Webcam | Sim | Não |
| Fade out | Fade to black | — | — |

---

## 5. Movimentos Visuais

### Zoom Digital

| Cena | Aplicar zoom? | Detalhe |
|------|--------------|---------|
| 01 — Abertura | **Não** | Webcam estática |
| 02 — Problema | **Não** | Webcam estática |
| 03 — Arquitetura | **Não** | Webcam/diagrama estático |
| 04 — Login | **Sim — opcional** | Zoom 110% no botão "Advogado" ao clicar. Zoom 110% no botão "Entrar" ao clicar. Duração: 0.5s in, 0.5s out. |
| 05 — Dashboard | **Sim — opcional** | Zoom 105% na navbar ao apontar. Zoom 105% no nome/role ao apontar. Duração: 0.5s in, 0.5s out. |
| 06 — Upload | **Não** | A ação de digitar e clicar já é clara |
| 07 — Análise | **Sim — opcional** | Zoom 105% nos badges de risco das cláusulas ao apontar. Duração: 0.5s in, 0.5s out. |
| 08 — Chat | **Sim — recomendado** | Zoom 110% na resposta do assistente quando aparecer. Zoom 105% nas citações ao apontar. Duração: 0.5s in, 0.5s out. |
| 09 — Riscos | **Sim — recomendado** | Zoom 110% no overall risk card quando aparecer. Zoom 105% em "Sources" ao expandir. Duração: 0.5s in, 0.5s out. |
| 10 — Automações | **Sim — opcional** | Zoom 105% nos status badges ao apontar. Duração: 0.5s in, 0.5s out. |
| 11 — Revisões | **Sim — recomendado** | Zoom 105% no histórico de revisões ao apontar. Zoom 105% no formulário de revisão. Duração: 0.5s in, 0.5s out. |
| 12 — Métricas | **Sim — opcional** | Zoom 105% nos 4 cards superiores ao apontar. Zoom 105% no aviso de estimativa. Duração: 0.5s in, 0.5s out. |
| 13 — Comparação | **Não** | A ação é simples e clara |
| 14 — Encerramento | **Não** | Webcam estática |

### Quando NÃO Aplicar Zoom

- **Nunca** aplicar zoom durante a digitação de texto
- **Nunca** aplicar zoom durante scroll
- **Nunca** aplicar zoom em cenas de webcam
- **Nunca** aplicar zoom superior a 115% (degrada a imagem)
- **Nunca** aplicar zoom com duração inferior a 0.3s (muito abrupto)
- **Nunca** aplicar zoom sem retorno suave (ease in/out)

### Destaque de Área

| Cena | Elemento | Tipo de destaque |
|------|---------|-----------------|
| 05 — Dashboard | Navbar | Zoom 105% ou cursor parado sobre a área |
| 07 — Análise | Badges de risco | Zoom 105% |
| 08 — Chat | Resposta do assistente | Zoom 110% |
| 08 — Chat | Citações | Zoom 105% |
| 08 — Chat | Disclaimer | Zoom 105% |
| 09 — Riscos | Overall risk | Zoom 110% |
| 09 — Riscos | Sources expandidas | Zoom 105% |
| 11 — Revisões | Histórico | Zoom 105% |
| 12 — Métricas | Aviso de estimativa | Zoom 105% |

> **Nota**: O destaque por zoom é preferível a overlays (caixas, setas, círculos). Se zoom não for suficiente, usar um retângulo sutil com borda azul (`#3b82f6`) e opacidade 50%, sem preenchimento.

### Cursor

| Situação | Orientação |
|----------|-----------|
| Apontar elemento | Mover cursor lentamente até o elemento e parar |
| Antes de clicar | Cursor parado sobre o elemento por 0.5–1s |
| Após clique | Manter cursor parado por 0.5s (não mover imediatamente) |
| Entre apontamentos | Mover cursor lentamente em linha reta (não em curvas erráticas) |
| Durante fala descritiva | Cursor parado ou movendo-se lentamente para o elemento mencionado |
| Durante loading | Cursor parado (não mexer) |

---

## 6. Cursor

### Velocidade

- **Movimento entre elementos**: Lento e constante. Aceleração suave (ease in/out).
- **Movimento para apontar**: Linear e direto. Sem zig-zag.
- **Velocidade recomendada**: ~200 pixels/segundo

### Movimentos a Evitar

- **Movimentos bruscos**: Qualquer movimento que pareça um "salto" deve ser cortado ou suavizado com speed ramp
- **Movimentos circulares**: Não fazer círculos com o cursor para apontar
- **Movimentos repetidos**: Não passar o cursor várias vezes sobre o mesmo elemento
- **Cursor ocioso**: Se o cursor não está apontando nada, deve estar parado em local neutro (canto inferior direito, por exemplo)

### Tempo Parado

| Momento | Tempo parado |
|---------|-------------|
| Antes de clicar um botão | 0.5–1s |
| Após clicar um botão | 0.5s |
| Ao apontar um elemento para narração | 2–3s (enquanto a fala descreve) |
| Durante loading | Até completar (não mover) |
| Entre cenas (frame final) | 2–3s |

---

## 7. Ritmo

### Diretrizes por Cena

| Cena | Pode acelerar? | Pode cortar silêncio? | Precisa mostrar animação completa? | Pode remover espera? |
|------|----------------|----------------------|-------------------------------------|---------------------|
| 01 — Abertura | **Não** | **Não** — pausas são intencionais | N/A | **Não** |
| 02 — Problema | **Não** | **Não** | N/A | **Não** |
| 03 — Arquitetura | **Não** | **Não** | N/A | **Não** |
| 04 — Login | **Não** | Cortar silêncio >3s | **Sim** — mostrar redirect | Cortar espera >3s no redirect |
| 05 — Dashboard | **Não** | Cortar silêncio >2s | N/A | **Não** |
| 06 — Upload | **Sim** — digitação (150–200%) | Cortar silêncio >2s | **Sim** — mostrar "Processando..." e tela de sucesso | Cortar espera entre seleção de arquivo e clique |
| 07 — Análise | **Sim** — scroll (150%) | Cortar silêncio >2s | **Sim** — mostrar loading e cards aparecendo | Cortar loading >5s (jump cut suave) |
| 08 — Chat | **Sim** — digitação (150–200%) | Cortar silêncio >2s | **Sim** — mostrar resposta chegando | Cortar espera de resposta >8s (cross dissolve 0.2s) |
| 09 — Riscos | **Sim** — scroll (150%) | Cortar silêncio >2s | **Sim** — mostrar overall risk aparecendo | Cortar loading >5s (jump cut suave) |
| 10 — Automações | **Sim** — scroll (150%) | Cortar silêncio >2s | N/A | **Não** |
| 11 — Revisões | **Sim** — digitação (150–200%) | Cortar silêncio >2s | **Sim** — mostrar histórico atualizado | Cortar espera entre "Aprovar" e formulário |
| 12 — Métricas | **Sim** — scroll (150%) | Cortar silêncio >2s | N/A | **Não** |
| 13 — Comparação | **Sim** — seleção (150%) | Cortar silêncio >2s | **Sim** — mostrar resultado aparecendo | Cortar loading >5s (jump cut suave) |
| 14 — Encerramento | **Não** | **Não** — pausas são intencionais | N/A | **Não** |

### Regras Gerais de Ritmo

- **Silêncio máximo permitido**: 3s entre frases (exceto cenas de webcam 01–03 e 14)
- **Loading máximo permitido**: 5s na tela (cortar o excesso com dissolve suave)
- **Digitação**: Acelerar se durar mais de 5s para preencher um campo
- **Scroll**: Acelerar se durar mais de 3s para chegar ao destino
- **Tela parada sem fala**: Máximo 2s (cortar o excesso)

---

## 8. Texto na Tela

### Princípios

- **Discreto**: Texto pequeno, posicionado em local não-obstrutivo
- **Breve**: Máximo 5 palavras por texto
- **Sem animação chamativa**: Fade in/out simples, 0.3s
- **Cor**: Branco com sombra preta sutil (para legibilidade sobre qualquer fundo)
- **Fonte**: Sans-serif (Inter, Helvetica, Arial)
- **Tamanho**: 24–28px equivalente em 1080p

### Textos Recomendados por Cena

| Cena | Texto | Tipo | Posição | Tempo de exibição |
|------|-------|------|---------|-------------------|
| 01 — Abertura | "Legal AI Copilot" | Título | Centro inferior | 00:00–00:05 (5s) |
| 01 — Abertura | "MVP — Análise de Contratos Jurídicos" | Subtítulo | Abaixo do título | 00:00–00:05 (5s) |
| 03 — Arquitetura | "Stack: FastAPI · React · SQLAlchemy · JWT · RBAC" | Lower third | Inferior esquerdo | 00:01:15–00:02:00 (45s) |
| 04 — Login | "Autenticação JWT + RBAC" | Legenda curta | Inferior esquerdo | 00:02:00–00:02:30 (30s) |
| 05 — Dashboard | "Dashboard de Documentos" | Legenda curta | Inferior esquerdo | 00:02:30–00:03:00 (30s) |
| 06 — Upload | "Upload & Processamento" | Legenda curta | Inferior esquerdo | 00:03:00–00:04:00 (60s) |
| 07 — Análise | "Resumo & Extração Estruturada" | Legenda curta | Inferior esquerdo | 00:04:00–00:05:30 (90s) |
| 08 — Chat | "Chat com Agent Router + Guardrails" | Legenda curta | Inferior esquerdo | 00:05:30–00:07:00 (90s) |
| 09 — Riscos | "Análise Heurística de Riscos" | Legenda curta | Inferior esquerdo | 00:07:00–00:08:30 (90s) |
| 10 — Automações | "Pipeline de Automação + Webhook" | Legenda curta | Inferior esquerdo | 00:08:30–00:09:15 (45s) |
| 11 — Revisões | "Revisão Humana — State Machine" | Legenda curta | Inferior esquerdo | 00:09:15–00:10:15 (60s) |
| 12 — Métricas | "Métricas de Impacto" | Legenda curta | Inferior esquerdo | 00:10:15–00:11:00 (45s) |
| 13 — Comparação | "Comparação de Contratos" | Legenda curta | Inferior esquerdo | 00:11:00–00:11:30 (30s) |
| 14 — Encerramento | "Limitações & Próximos Passos" | Legenda curta | Inferior esquerdo | 00:11:30–00:12:30 (60s) |

### Especificações Técnicas dos Textos

#### Título (Cena 01)

| Parâmetro | Valor |
|-----------|-------|
| Texto | "Legal AI Copilot" |
| Fonte | Inter Bold ou Helvetica Bold |
| Tamanho | 48px |
| Cor | #FFFFFF |
| Sombra | 2px offset, 4px blur, #000000 60% |
| Posição | Centro horizontal, 75% vertical |
| Animação | Fade in 0.5s, fade out 0.5s |
| Duração | 5s (00:00–00:05) |

#### Subtítulo (Cena 01)

| Parâmetro | Valor |
|-----------|-------|
| Texto | "MVP — Análise de Contratos Jurídicos" |
| Fonte | Inter Regular ou Helvetica Regular |
| Tamanho | 28px |
| Cor | #E5E7EB (gray-200) |
| Sombra | 1px offset, 3px blur, #000000 60% |
| Posição | Centro horizontal, 82% vertical |
| Animação | Fade in 0.5s (0.3s após título), fade out 0.5s |
| Duração | 5s (00:00–00:05) |

#### Lower Third (Cena 03)

| Parâmetro | Valor |
|-----------|-------|
| Texto | "Stack: FastAPI · React · SQLAlchemy · JWT · RBAC" |
| Fonte | Inter Medium ou Helvetica Medium |
| Tamanho | 24px |
| Cor | #FFFFFF |
| Sombra | 1px offset, 2px blur, #000000 70% |
| Posição | 5% horizontal esquerda, 90% vertical |
| Animação | Fade in 0.3s, fade out 0.3s |
| Duração | 45s (duração total da cena) |

#### Legendas Curtas (Cenas 04–14)

| Parâmetro | Valor |
|-----------|-------|
| Fonte | Inter Medium ou Helvetica Medium |
| Tamanho | 24px |
| Cor | #FFFFFF |
| Sombra | 1px offset, 2px blur, #000000 70% |
| Posição | 5% horizontal esquerda, 90% vertical |
| Animação | Fade in 0.3s, fade out 0.3s |
| Duração | Duração total da cena |

### Quando NÃO Usar Texto na Tela

- **Durante cenas de webcam sem overlay** (Cenas 01–03, 14): Apenas o título/subtítulo da Cena 01 e o lower third da Cena 03. A Cena 02 e a Cena 14 não recebem texto.
- **Sobre elementos da aplicação**: Não sobrepor texto sobre botões, cards ou dados da aplicação
- **Durante transições**: O texto deve aparecer após a transição completar e desaparecer antes da próxima transição iniciar

---

## 9. Tratamento de Áudio

### Pipeline de Tratamento (em ordem)

#### 1. Remoção de Ruído

| Parâmetro | Valor |
|-----------|-------|
| Ferramenta | Noise reduction (DaVinci: Voice Isolation / Premiere: DeNoise / CapCut: Noise Reduction) |
| Intensidade | Baixa a moderada (preservar naturalidade da voz) |
| Frequência alvo | Ruído de fundo constante (ventilador, ar-condicionado) |
| **Evitar** | Redução agressiva que gera artefatos "robóticos" |

#### 2. Compressão

| Parâmetro | Valor |
|-----------|-------|
| Threshold | -20 dB |
| Ratio | 3:1 |
| Attack | 10 ms |
| Release | 100 ms |
| Knee | Soft |
| Makeup gain | +2 dB |

#### 3. Equalização

| Parâmetro | Valor |
|-----------|-------|
| High-pass filter | 80 Hz (remover rumble) |
| Low shelf | -2 dB @ 200 Hz (reduzir boominess) |
| Mid boost | +2 dB @ 3 kHz (melhorar clareza) |
| High shelf | +1 dB @ 8 kHz (brilho suave) |

#### 4. Normalização

| Parâmetro | Valor |
|-----------|-------|
| Target | -16 LUFS integrated |
| True peak | -1.5 dBTP |
| Mode | Loudness normalization (não peak normalization) |

#### 5. De-Essing (se necessário)

| Parâmetro | Valor |
|-----------|-------|
| Frequência | 5–7 kHz |
| Reduction | -3 dB a -5 dB |
| Aplicar apenas se | Sibilância ("sss") estiver evidente |

### Volume de Voz

| Parâmetro | Valor |
|-----------|-------|
| Volume alvo | -16 LUFS |
| True peak máximo | -1.5 dBTP |
| Variação aceitável | ±1 LUFS entre cenas |

### Volume do Sistema

- **Geralmente não há áudio de desktop** (OBS configurado para não capturar áudio do sistema)
- Se houver áudio de desktop capturado acidentalmente: **remover completamente** (mutar a faixa de desktop)
- **Sem trilha sonora de fundo**
- **Sem efeitos sonoros**

### Verificação de Áudio por Cena

| Cena | Verificar |
|------|-----------|
| Todas | Sem clique no início/fim do corte |
| Todas | Sem ruído de fundo aumentando entre cenas |
| 04–13 | Áudio sincronizado com a ação na tela |
| 01–03, 14 | Voz clara e natural (sem processamento excessivo) |
| Transições | Cross dissolve de áudio suave (0.3–0.5s) |
| Cortes secos | Verificar que não há "pop" no corte — usar fade de áudio de 5ms se necessário |

---

## 10. Continuidade

### Garantindo Continuidade entre Cenas

#### Cenas de Webcam (01–03, 14)

| Elemento | Verificar |
|----------|-----------|
| Roupa | Idêntica em todas as cenas de webcam |
| Iluminação | Mesma intensidade e temperatura de cor |
| Posição da câmera | Mesmo enquadramento |
| Fundo | Mesmo cenário |
| Tom de voz | Consistente (mesmo horário de gravação) |

#### Cenas de Tela (04–13)

| Elemento | Verificar |
|----------|-----------|
| Documentos na tela | Mesmos documentos entre cenas que mostram o dashboard |
| Zoom do navegador | 100% em todas as cenas |
| Tema do navegador | Claro em todas as cenas |
| Perfil do navegador | Mesmo perfil em todas as cenas |
| Usuário logado | Mesmo usuário (lawyer@demo.com) em todas as cenas |
| Estado da aplicação | Documentos, conversas e análises consistentes |

### Escondendo Cortes

| Situação | Técnica |
|----------|---------|
| Corte entre cenas de webcam | Cross dissolve 0.5s (sempre) |
| Corte entre cenas de tela com mesma página | Cut seco (se estado idêntico) |
| Corte entre cenas de tela com páginas diferentes | Cut seco (a navegação é a transição) |
| Corte entre webcam e tela | Cross dissolve 0.8s |
| Corte dentro de uma cena (jump cut) | Cross dissolve 0.2s ou speed ramp |
| Corte para remover erro | Cross dissolve 0.3s (esconde a descontinuidade) |

### Sincronização Após Regravação

Se uma cena foi regravada (ver `07_SCENE_RETAKE_GUIDE.md`):

1. **Substituir o arquivo** na timeline
2. **Verificar continuidade visual** com a cena anterior e a seguinte
3. **Verificar continuidade de áudio** — volume e tom consistentes
4. **Ajustar transições** se necessário (dissolve mais longo pode esconder diferenças)
5. **Reproduzir 5s antes e 5s depois** do corte para verificar fluidez

---

## 11. Erros Visuais

### Loading Longo

| Situação | Ação |
|----------|------|
| Loading > 5s | Cortar o meio com cross dissolve 0.2s. Manter 1s no início e 1s no fim. |
| Loading infinito | Cortar e substituir com o resultado de outra tomada. Se não houver, usar speed ramp 300% no loading. |
| Loading com erro | **Não incluir no vídeo**. Regravar a cena. Se impossível, cortar a seção e narrar "o processamento foi concluído". |

### Erro Temporário na Tela

| Situação | Ação |
|----------|------|
| Mensagem de erro transient | Cortar a seção (cross dissolve 0.3s). Se a fala coincide com o erro, regravar a cena. |
| 401 Unauthorized (token expirado) | **Não incluir no vídeo**. Regravar a cena com novo login. |
| Network error | Cortar a seção. Regravar se a fala foi afetada. |
| Console error visível (DevTools aberto) | **Não incluir no vídeo**. Regravar com DevTools fechado. |

### Lag / Drop Frame

| Situação | Ação |
|----------|------|
| Lag < 0.5s | Manter — é imperceptível |
| Lag 0.5–1s | Speed ramp suave para compensar |
| Lag > 1s | Cortar a seção com cross dissolve 0.3s |
| Drop frames consistentes | Re-renderizar o clipe com configuração de OBS ajustada |

### Mouse Errado

| Situação | Ação |
|----------|------|
| Cursor em local errado | Cortar a seção. Se a fala foi afetada, regravar. |
| Clique no botão errado | Cortar a seção. Regravar. |
| Cursor se move durante fala descritiva | Speed ramp para suavizar o movimento. Se muito errático, regravar. |

### Scroll Excessivo

| Situação | Ação |
|----------|------|
| Scroll passou do alvo e voltou | Cortar a seção (cross dissolve 0.2s). Manter o frame final correto. |
| Scroll muito rápido | Speed ramp 50% para desacelerar. |
| Scroll muito lento | Speed ramp 150% para acelerar. |
| Scroll em direção errada | Cortar e regravar. |

### Notificação Apareceu

| Situação | Ação |
|----------|------|
| Notificação do sistema (toast, banner) | Cortar a seção (cross dissolve 0.3s). Se a notificação cobriu conteúdo importante, regravar. |
| Notificação do navegador | Cortar a seção. Regravar. |
| Notificação de app (Slack, Discord) | Cortar a seção. Regravar. Reforçar "Não perturbe". |

---

## 12. Checklist de Pós-Produção

### Antes da Exportação — Visual

- [ ] Todos os 14 clipes na timeline na ordem correta
- [ ] Sem cortes bruscos entre cenas de webcam (todas com cross dissolve)
- [ ] Sem pausas excessivas (silêncio > 3s em cenas de tela, exceto loading intencional)
- [ ] Sem cliques duplicados (mesmo botão clicado duas vezes sem motivo)
- [ ] Sem tela parada sem fala por > 2s (exceto frame final de cada cena)
- [ ] Sem notificações visíveis em nenhuma cena
- [ ] Sem informações pessoais visíveis (email real, nome real, telefone, etc.)
- [ ] Sem DevTools aberta
- [ ] Sem barra de favoritos visível
- [ ] Sem extensões na barra de ferramentas
- [ ] Zoom digital aplicado apenas onde recomendado
- [ ] Textos na tela posicionados corretamente (inferior esquerdo)
- [ ] Textos na tela com fade in/out suave
- [ ] Transições corretas: cross dissolve entre webcam↔tela, cut seco entre telas
- [ ] Fade in from black no início (0.5s)
- [ ] Fade out to black no final (1.0s)

### Antes da Exportação — Áudio

- [ ] Áudio sincronizado com a ação em todas as cenas
- [ ] Remoção de ruído aplicada (sem artefatos robóticos)
- [ ] Compressão aplicada (threshold -20 dB, ratio 3:1)
- [ ] Equalização aplicada (high-pass 80 Hz, clareza +2 dB @ 3 kHz)
- [ ] Normalização para -16 LUFS
- [ ] True peak abaixo de -1.5 dBTP
- [ ] Sem cliques ou "pops" nos cortes (fade de áudio 5ms se necessário)
- [ ] Sem áudio de desktop (apenas voz)
- [ ] Sem trilha sonora
- [ ] Sem efeitos sonoros
- [ ] Volume consistente entre cenas (±1 LUFS)
- [ ] De-essing aplicado se necessário

### Antes da Exportação — Conteúdo

- [ ] O vídeo explica claramente o problema (Cena 02)
- [ ] O vídeo mostra a arquitetura (Cena 03)
- [ ] O vídeo mostra upload (Cena 06)
- [ ] O vídeo mostra análise — resumo e extração (Cena 07)
- [ ] O vídeo mostra chat com guardrails (Cena 08)
- [ ] O vídeo mostra análise de riscos (Cena 09)
- [ ] O vídeo mostra automações (Cena 10)
- [ ] O vídeo mostra revisão humana (Cena 11)
- [ ] O vídeo mostra métricas (Cena 12)
- [ ] O vídeo mostra comparação (Cena 13)
- [ ] O vídeo menciona limitações (Cena 14)
- [ ] O vídeo termina com conclusão (Cena 14)
- [ ] Duração entre 11:00 e 15:00

---

## 13. Checklist de Exportação

### Arquivo

- [ ] Nome: `legal_ai_copilot_demo.mp4`
- [ ] Local: pasta definida pelo editor
- [ ] Tamanho estimado: 750–850 MB

### Codec e Formato

- [ ] Formato: MP4
- [ ] Codec de vídeo: H.264 (x264)
- [ ] Codec de áudio: AAC
- [ ] Container: MP4

### Resolução e FPS

- [ ] Resolução: 1920×1080
- [ ] Aspect ratio: 16:9
- [ ] FPS: 30
- [ ] Scan: Progressive

### Bitrate e Qualidade

- [ ] Bitrate de vídeo: 8 Mbps (CBR)
- [ ] Bitrate de áudio: 192 Kbps
- [ ] Profile: High
- [ ] Level: 4.0
- [ ] Encoding: 2-pass (para qualidade consistente)

### Áudio

- [ ] Sample rate: 48 kHz
- [ ] Canais: Stereo
- [ ] Volume: -16 LUFS integrated
- [ ] True peak: -1.5 dBTP máximo

### Verificação Pós-Exportação

- [ ] Reproduzir o arquivo exportado do início ao fim
- [ ] Verificar áudio em fones de ouvido
- [ ] Verificar áudio em alto-falantes
- [ ] Verificar legibilidade em 720p (reduzir janela para metade)
- [ ] Verificar que não há artefatos de compressão visíveis
- [ ] Verificar que o fade in/out está correto
- [ ] Verificar duração final (11:00–15:00)

---

## 14. Checklist Final

### O vídeo...

- [ ] Explica claramente o problema? (Cena 02 — análise manual é lenta, sujeita a erros, sem rastreabilidade)
- [ ] Mostra arquitetura? (Cena 03 — FastAPI, React, SQLAlchemy, JWT, RBAC, Agent Router, guardrails)
- [ ] Mostra upload? (Cena 06 — PDF upload com processamento automático)
- [ ] Mostra análise? (Cena 07 — resumo + extração estruturada: partes, datas, valores, cláusulas)
- [ ] Mostra guardrails? (Cena 08 — validação de confiança, citações obrigatórias, disclaimer jurídico)
- [ ] Mostra human review? (Cena 11 — state machine, histórico append-only, aprovar/rejeitar/correções)
- [ ] Mostra métricas? (Cena 12 — documentos, análises, tempo poupado, taxa de aprovação, estimativas)
- [ ] Mostra limitações? (Cena 14 — heurística sem LLM, similarity fixo, sem OCR, SQLite, métricas estimadas)
- [ ] Termina com conclusão? (Cena 14 — fluxo completo demonstrado, modo heurístico sem API key)
- [ ] Está dentro do tempo? (11:00–15:00, alvo 12:30–13:30)

### Qualidade Geral

- [ ] Tom técnico e profissional (sem linguagem de marketing)
- [ ] Transições suaves e consistentes
- [ ] Áudio claro e normalizado
- [ ] Sem elementos visuais distraentes
- [ ] Textos na tela discretos e informativos
- [ ] Ritmo adequado (sem pressa, sem enrolação)
- [ ] Limitações mencionadas com transparência
