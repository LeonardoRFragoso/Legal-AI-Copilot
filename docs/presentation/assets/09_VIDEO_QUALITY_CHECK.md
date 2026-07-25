# Video Quality Check — Legal AI Copilot

> Checklist final de qualidade para o vídeo de apresentação.
> Cobre ortografia, cortes, áudio, qualidade visual, cursor, scroll, tempos, render e exportação.
> Referência cruzada com toda a documentação existente.

---

## 1. Ortografia e Texto

### Títulos e Subtítulos (Title Cards)

- [ ] "Legal AI Copilot" — sem erros de ortografia
- [ ] "AI-powered Legal Document Analysis" — sem erros
- [ ] "O Problema" — sem erros
- [ ] "Por que contratos complexos precisam de apoio de IA" — sem erros
- [ ] "Arquitetura" — sem erros
- [ ] "Pipeline completo de processamento" — sem erros
- [ ] "Demonstração" — sem erros
- [ ] "Fluxo completo no navegador" — sem erros
- [ ] "Limitações & Próximos Passos" — sem erros
- [ ] "MVP funcional com transparência" — sem erros

### Lower Thirds

- [ ] "Autenticação JWT + RBAC" — sem erros
- [ ] "Dashboard de Documentos" — sem erros
- [ ] "Upload & Processamento" — sem erros
- [ ] "Resumo & Extração Estruturada" — sem erros
- [ ] "Chat com Agent Router + Guardrails" — sem erros
- [ ] "Análise Heurística de Riscos" — sem erros
- [ ] "Pipeline de Automação + Webhook" — sem erros
- [ ] "Human Review — Approval Workflow" — sem erros
- [ ] "Business Insights & Analytics" — sem erros
- [ ] "Document Comparison" — sem erros
- [ ] "Limitações & Conclusão" — sem erros

### End Credits

- [ ] "Legal AI Copilot" — sem erros
- [ ] "AI-powered Legal Document Analysis" — sem erros
- [ ] "FastAPI · React · TypeScript" — sem erros, separadores corretos
- [ ] "SQLAlchemy · SQLite · JWT · RBAC" — sem erros
- [ ] "github.com/LeonardoRFragoso" — URL correta
- [ ] "/Legal-AI-Copilot" — path correto
- [ ] "Obrigado." — sem erros

### Texto na Aplicação (não controlado pelo editor, mas verificar)

- [ ] Nenhum texto cortado na gravação
- [ ] Nenhum texto sobreposto por overlay
- [ ] Lower thirds não cobrem conteúdo crítico
- [ ] Title cards não cobrem botões ou campos

---

## 2. Cortes e Transições

### Transições entre Cenas

- [ ] Cena 01 → 02: Cut seco (mesma tela)
- [ ] Cena 02 → 03: Cut seco (mesma tela)
- [ ] Cena 03 → 04: Cut seco (mesma tela)
- [ ] Cena 04 → 05: Cut seco (dashboard já visível)
- [ ] Cena 05 → 06: Cut seco (navegação para /upload)
- [ ] Cena 06 → 07: Cut seco (navegação para /analysis)
- [ ] Cena 07 → 08: Cross dissolve 0.3s (transição via "Iniciar Chat")
- [ ] Cena 08 → 09: Cut seco (navegação para /risks)
- [ ] Cena 09 → 10: Cut seco (navegação para /automations)
- [ ] Cena 10 → 11: Cut seco (navegação para /reviews)
- [ ] Cena 11 → 12: Cut seco (navegação para /insights)
- [ ] Cena 12 → 13: Cut seco (navegação para /comparison)
- [ ] Cena 13 → 14: Cut seco (navegação para /dashboard)
- [ ] Início do vídeo: Fade in from black 0.5s
- [ ] Fim do vídeo: Fade out to black 1.0s
- [ ] End credits: Fade in from black 1.0s, fade out to black 1.0s

### Cortes Internos (jump cuts)

- [ ] Nenhum jump cut visível (todos escondidos com cross dissolve 0.2s)
- [ ] Nenhum corte que cause "pop" de áudio (fade de áudio 5ms aplicado)
- [ ] Silêncios > 3s em cenas de tela foram cortados (exceto loading intencional)
- [ ] Digitação acelerada sem corte visível (speed ramp suave)

### Continuidade

- [ ] Estado do dashboard consistente entre cenas que o mostram
- [ ] Mesmo usuário logado em todas as cenas (lawyer@demo.com)
- [ ] Mesmos documentos visíveis entre cenas
- [ ] Zoom do navegador em 100% em todas as cenas
- [ ] Tema claro em todas as cenas
- [ ] Sem mudanças de janela ou resolução entre cenas

---

## 3. Áudio

### Voz (Narração em Off)

- [ ] Remoção de ruído aplicada (sem artefatos robóticos)
- [ ] Compressão aplicada (threshold -20 dB, ratio 3:1)
- [ ] Equalização aplicada (high-pass 80 Hz, clareza +2 dB @ 3 kHz)
- [ ] Normalização para -16 LUFS integrated
- [ ] True peak abaixo de -1.5 dBTP
- [ ] Volume consistente entre cenas (±1 LUFS)
- [ ] De-essing aplicado se necessário (5–7 kHz, -3 a -5 dB)
- [ ] Sem cliques ou "pops" nos cortes
- [ ] Sem áudio de desktop (apenas voz)
- [ ] Sem trilha sonora
- [ ] Sem efeitos sonoros
- [ ] Voz clara e natural (sem processamento excessivo)

### Sincronização Áudio-Vídeo

- [ ] Áudio sincronizado com a ação em todas as cenas
- [ ] Fala alinhada com movimento do cursor
- [ ] Fala alinhada com cliques
- [ ] Fala alinhada com mudanças de página
- [ ] Fala alinhada com scroll
- [ ] Pausas na fala correspondem a momentos visuais (loading, leitura)
- [ ] Narração não se sobrepõe a transições (fade in/out de áudio)

---

## 4. Qualidade Visual

### Resolução e Codec

- [ ] Resolução: 1920×1080
- [ ] FPS: 30
- [ ] Codec de edição: ProRes 422 ou DNxHR
- [ ] Color space: Rec.709
- [ ] Scan: Progressive

### Qualidade da Imagem

- [ ] Sem artefatos de compressão visíveis
- [ ] Sem drop frames
- [ ] Sem lag ou stutter
- [ ] Sem screen tearing
- [ ] Cores fiéis à aplicação (sem grading agressivo)
- [ ] White balance correto (se webcam usada para narração — não aparece no vídeo)
- [ ] Exposição correta (tela não muito escura nem muito clara)
- [ ] Texto da aplicação legível em 1080p
- [ ] Texto da aplicação legível em 720p (teste em janela reduzida)

### Elementos Overlaid

- [ ] Title cards com fade in/out suave (0.5s)
- [ ] Lower thirds com fade in/out suave (0.3s)
- [ ] Callouts com fade in/out suave (0.3s)
- [ ] End credits com fade in/out suave (1.0s)
- [ ] Nenhum overlay cobre conteúdo crítico da aplicação
- [ ] Nenhum overlay permanece na tela por tempo excessivo
- [ ] Fonte Inter (ou Helvetica) aplicada consistentemente
- [ ] Tamanhos de fonte corretos (ver `05_VIDEO_STYLE_GUIDE.md`)
- [ ] Cores de texto corretas (ver `06_COLOR_REFERENCE.md`)
- [ ] Sombras de texto aplicadas para legibilidade

---

## 5. Cursor

### Visibilidade

- [ ] Cursor visível em todas as 14 cenas
- [ ] Cursor nunca oculto por overlays
- [ ] Cursor nunca oculto por elementos da aplicação

### Movimento

- [ ] Todos os movimentos suaves e lineares
- [ ] Nenhum movimento brusco ou "salto"
- [ ] Nenhum movimento circular desnecessário
- [ ] Nenhum zig-zag entre elementos
- [ ] Velocidade máxima: ~250px/s
- [ ] Velocidade ao apontar: ~100–200px/s
- [ ] Velocidade ao navegar para navbar: ~300px/s

### Paradas

- [ ] 500ms parado antes de cada clique
- [ ] 500ms parado após cada clique
- [ ] 2–3s parado sobre elementos sendo narrados
- [ ] Cursor parado durante todos os carregamentos
- [ ] Cursor em posição neutra (x:1700, y:950) quando não está apontando

### Cliques

- [ ] Nenhum clique duplo desnecessário
- [ ] Nenhum clique errado visível
- [ ] Nenhum clique em elemento errado
- [ ] Todos os cliques resultam em ação visível

---

## 6. Scroll

### Movimento

- [ ] Todos os scrolls suaves e constantes (~200–300px/s)
- [ ] Nenhum scroll muito rápido (parece errático)
- [ ] Nenhum scroll muito lento (parece travado)
- [ ] Nenhum scroll de ida e volta (exceto Cena 07 — voltar para "Iniciar Chat")
- [ ] Direção correta (para baixo, exceto retorno na Cena 07)

### Paradas após Scroll

- [ ] 2s de pausa após cada scroll antes de mover o cursor
- [ ] Conteúdo alvo visível após scroll
- [ ] Nenhum scroll passou do alvo e voltou

### Quantidade por Cena

- [ ] Cena 07: 2 scrolls (baixo ~400px, cima ~600px)
- [ ] Cena 08: 1 scroll (baixo ~200px, se necessário)
- [ ] Cena 09: 1 scroll (baixo ~300px)
- [ ] Cena 10: 1 scroll (baixo ~300px, se necessário)
- [ ] Cena 11: 1 scroll (baixo ~300px)
- [ ] Cena 12: 2 scrolls (baixo ~300px + baixo ~300px)
- [ ] Todas as outras cenas: 0 scrolls

---

## 7. Tempos

### Duração Total

- [ ] Duração entre 11:00 e 15:00
- [ ] Duração alvo: 12:30–13:30
- [ ] Tolerância: ±30s em relação ao alvo

### Duração por Cena

| Cena | Duração esperada | Verificar |
|------|-----------------|-----------|
| 01 | 30s | [ ] |
| 02 | 45s | [ ] |
| 03 | 45s | [ ] |
| 04 | 30s | [ ] |
| 05 | 30s | [ ] |
| 06 | 60s | [ ] |
| 07 | 90s | [ ] |
| 08 | 90s | [ ] |
| 09 | 90s | [ ] |
| 10 | 45s | [ ] |
| 11 | 60s | [ ] |
| 12 | 45s | [ ] |
| 13 | 30s | [ ] |
| 14 | 60s | [ ] |

### Tempos de Exibição de Overlays

- [ ] Title card 01: 00:00–00:05 (5s)
- [ ] Title card 02: 00:30–00:35 (5s)
- [ ] Title card 03: 01:15–01:20 (5s)
- [ ] Title card 04: 02:00–02:04 (4s)
- [ ] Title card 05: 11:30–11:36 (6s)
- [ ] Lower thirds: duração total de cada cena (ver `02_LOWER_THIRDS.md`)
- [ ] Callouts: 2–3s cada (ver `03_SCREEN_CALLOUTS.md`)
- [ ] End credits: 12:30–12:39 (8s + 1s fade)

### Tempos de Loading

- [ ] Loading > 5s acelerado na edição (speed ramp ou cross dissolve 0.2s)
- [ ] Loading < 3s mantido integralmente
- [ ] Nenhum loading completamente removido (sempre 1s no início e 1s no fim)

---

## 8. Render

### Antes de Renderizar

- [ ] Timeline completa com todas as 14 cenas
- [ ] Todas as transições aplicadas
- [ ] Todos os overlays posicionados
- [ ] Todos os callouts aplicados
- [ ] Áudio tratado e normalizado
- [ ] Sem clipes offline ou faltando
- [ ] Sem marcadores ou anotações temporais na timeline
- [ ] Preview renderizado sem erros

### Renderização

- [ ] Render em qualidade máxima (não proxy)
- [ ] 2-pass encoding
- [ ] Sem limitação de bitrate durante render
- [ ] Render completo sem interrupções
- [ ] Arquivo de saída: `legal_ai_copilot_demo.mp4`

---

## 9. Exportação

### Arquivo Final

- [ ] Nome: `legal_ai_copilot_demo.mp4`
- [ ] Formato: MP4
- [ ] Codec de vídeo: H.264 (x264)
- [ ] Codec de áudio: AAC
- [ ] Resolução: 1920×1080
- [ ] FPS: 30
- [ ] Bitrate de vídeo: 8 Mbps (CBR)
- [ ] Bitrate de áudio: 192 Kbps
- [ ] Profile: High
- [ ] Level: 4.0
- [ ] Sample rate: 48 kHz
- [ ] Canais: Stereo
- [ ] Volume: -16 LUFS integrated
- [ ] True peak: -1.5 dBTP máximo
- [ ] Encoding: 2-pass
- [ ] Tamanho estimado: 750–850 MB

### Verificação Pós-Exportação

- [ ] Reproduzir o arquivo do início ao fim sem interrupções
- [ ] Verificar áudio em fones de ouvido (clareza, volume, sem ruído)
- [ ] Verificar áudio em alto-falantes (clareza, volume)
- [ ] Verificar legibilidade em 720p (janela em 50% do tamanho)
- [ ] Verificar que não há artefatos de compressão visíveis
- [ ] Verificar fade in do início (0.5s)
- [ ] Verificar fade out do fim (1.0s)
- [ ] Verificar end credits (8s com fade in/out)
- [ ] Verificar duração total (11:00–15:00)
- [ ] Verificar que o arquivo abre em múltiplos players (VLC, QuickTime, Chrome)

---

## 10. Conteúdo — Checklist Funcional

### O vídeo demonstra...

- [ ] O problema (análise manual é lenta, sujeita a erros, sem rastreabilidade)
- [ ] A arquitetura (FastAPI, React, SQLAlchemy, JWT, RBAC, Agent Router, guardrails)
- [ ] Login com credenciais demo (perfil Advogado)
- [ ] Dashboard com lista de documentos
- [ ] Navbar com 9 funcionalidades
- [ ] Upload de PDF com processamento automático
- [ ] Análise: resumo automático
- [ ] Análise: extração estruturada (Partes, Datas, Valores, Cláusulas)
- [ ] Análise: badges de risco por cláusula
- [ ] Chat: digitação de pergunta
- [ ] Chat: resposta estruturada do agent router
- [ ] Chat: citações com page number e similarity
- [ ] Chat: disclaimer jurídico
- [ ] Riscos: overall risk card com confidence score
- [ ] Riscos: risk cards com severidade, categoria, descrição, recomendação
- [ ] Riscos: sources expansíveis com excerpt
- [ ] Riscos: disclaimer sobre heurística
- [ ] Automações: lista de runs com status
- [ ] Automações: barra de progresso
- [ ] Automações: webhook status
- [ ] Automações: links para documento e riscos
- [ ] Revisões: lista de análises com filtros
- [ ] Revisões: painel de detalhe
- [ ] Revisões: histórico append-only
- [ ] Revisões: aprovação com comentário
- [ ] Revisões: histórico atualizado
- [ ] Métricas: 4 cards superiores (documentos, análises, tempo, aprovação)
- [ ] Métricas: grid 2x2 (análises por tipo, status, riscos, automações)
- [ ] Métricas: estimativa de produtividade
- [ ] Métricas: aviso de estimativas
- [ ] Comparação: seleção de 2 documentos
- [ ] Comparação: resultado formatado
- [ ] Encerramento: limitações (heurística, sem LLM, sem OCR, SQLite, estimadas)
- [ ] Encerramento: conclusão sobre fluxo completo

---

## 11. Checklist Final — Aprovação

### Antes de Publicar

- [ ] Todas as seções acima verificadas
- [ ] Vídeo reproduzido integralmente pelo menos 2 vezes
- [ ] Outra pessoa revisou o vídeo (se possível)
- [ ] Nenhuma informação pessoal visível (email real, nome real, telefone)
- [ ] Nenhuma notificação apareceu em nenhuma cena
- [ ] Nenhuma extensão visível na barra do navegador
- [ ] Barra de favoritos oculta em todas as cenas
- [ ] DevTools fechada em todas as cenas
- [ ] Sem erros 401/403/500 visíveis em nenhuma cena
- [ ] Sem console errors visíveis
- [ ] Tom técnico e profissional mantido do início ao fim
- [ ] Limitações mencionadas com transparência
- [ ] Duração dentro do limite (11:00–15:00)

### Compatibilidade com Documentação

- [ ] Consistente com `02_DEMO_TIMELINE.md` (14 cenas, mesmos tempos)
- [ ] Consistente com `03_SCREEN_NAVIGATION_SCRIPT.md` (URLs, botões, ações)
- [ ] Consistente com `04_VIDEO_SPEECH_SCRIPT.md` (fala, pausas, sincronização)
- [ ] Consistente com `10_VIDEO_EDITING_SCRIPT.md` (transições, cortes, áudio)
- [ ] Consistente com `11_SCREEN_RECORDING_SHOTLIST.md` (cursor, cliques, scroll)
- [ ] Consistente com `01_TITLE_CARDS.md` (títulos e subtítulos)
- [ ] Consistente com `02_LOWER_THIRDS.md` (legendas por cena)
- [ ] Consistente com `03_SCREEN_CALLOUTS.md` (destaques visuais)
- [ ] Consistente com `04_END_CREDITS.md` (tela final)
- [ ] Consistente com `05_VIDEO_STYLE_GUIDE.md` (tipografia, cores, safe area)
- [ ] Consistente com `06_COLOR_REFERENCE.md` (paleta de cores)
- [ ] Consistente com `07_ICON_REFERENCE.md` (ícones destacados)
- [ ] Consistente com `08_NARRATION_PACING.md` (sincronização fala-cursor)

### Arquivo Final

- [ ] Nome: `legal_ai_copilot_demo.mp4`
- [ ] Backup criado em local secundário
- [ ] Pronto para publicação
