# Video Style Guide — Legal AI Copilot

> Guia de estilo visual para a edição do vídeo de apresentação.
> Define tipografia, animações, transições, posicionamento e safe area.
> Referência: Stripe, Vercel, Supabase, Linear, GitHub, OpenAI.

---

## 1. Tipografia

### Família Tipográfica

| Uso | Fonte | Peso |
|-----|-------|------|
| Títulos (title cards) | Inter | Bold (700) |
| Subtítulos | Inter | Regular (400) |
| Lower thirds | Inter | Medium (500) |
| End credits — título | Inter | Bold (700) |
| End credits — tecnologias | Inter | Medium (500) |
| End credits — obrigado | Inter | Bold (700) |

> **Fonte alternativa**: Se Inter não estiver disponível, usar Helvetica Neue ou SF Pro Display.

### Tamanhos

| Elemento | Tamanho (1080p) |
|----------|-----------------|
| Title card — título | 48px |
| Title card — subtítulo | 28px |
| Title card — título secundário | 42px |
| Lower third | 24px |
| End credit — título | 48px |
| End credit — subtítulo | 24px |
| End credit — tecnologias | 20px |
| End credit — GitHub | 20px |
| End credit — obrigado | 32px |

### Espaçamento

| Elemento | Espaçamento |
|----------|-------------|
| Entre título e subtítulo (title card) | 12px |
| Entre linhas de tecnologias (end credit) | 8px |
| Entre linhas de GitHub (end credit) | 4px |
| Entre blocos (end credit) | 48px |
| Line-height geral | 1.4 |

---

## 2. Cores de Texto

| Elemento | Cor | Hex |
|----------|-----|-----|
| Título principal | Branco | #FFFFFF |
| Subtítulo | Slate-400 | #94A3B8 |
| Lower third | Branco | #FFFFFF |
| Tecnologias | Slate-500 | #64748B |
| GitHub | Blue-500 | #3B82F6 |
| Obrigado | Branco | #FFFFFF |

### Sombra de Texto

| Uso | Offset | Blur | Cor | Opacidade |
|----|--------|------|-----|-----------|
| Títulos | 0px Y, 2px X | 4px | #000000 | 70% |
| Lower thirds | 0px Y, 1px X | 2px | #000000 | 70% |
| End credits | Nenhuma | — | — | — (fundo escuro) |

---

## 3. Animações

### Fade

| Tipo | Duração | Curva | Uso |
|------|---------|-------|-----|
| Fade in from black | 0.5s | Linear | Início do vídeo |
| Fade in from black | 1.0s | Linear | End credits |
| Fade out to black | 1.0s | Linear | Fim do vídeo e end credits |
| Fade in (texto) | 0.5s | Ease out | Title cards |
| Fade out (texto) | 0.5s | Ease in | Title cards |
| Fade in (lower third) | 0.3s | Ease out | Lower thirds |
| Fade out (lower third) | 0.3s | Ease in | Lower thirds |
| Fade in (callout) | 0.3s | Ease out | Retângulos de destaque |
| Fade out (callout) | 0.3s | Ease in | Retângulos de destaque |

### Zoom Digital

| Tipo | Duração in | Duração out | Curva | Uso |
|------|-----------|-------------|-------|-----|
| Zoom 105% | 0.5s | 0.5s | Ease in/out | Destaque suave |
| Zoom 110% | 0.5s | 0.5s | Ease in/out | Destaque moderado |
| Zoom 115% | 0.5s | 0.5s | Ease in/out | Destaque máximo (usar com moderação) |

### Speed Ramp (aceleração de vídeo)

| Tipo | Duração | Uso |
|------|---------|-----|
| 150% speed | Variável | Acelerar digitação ou scroll |
| 200% speed | Variável | Acelerar digitação longa |
| 300% speed | Variável | Acelerar loading longo |

---

## 4. Transições

### Entre Cenas

| Tipo | Duração | Uso |
|------|---------|-----|
| Cut seco | 0s | Entre cenas de tela (a navegação é a transição) |
| Cross dissolve | 0.3s | Cena 07 → 08 (transição via "Iniciar Chat") |
| Cross dissolve | 0.5s | Reservado para transições webcam↔tela (não usado neste vídeo) |
| Fade in from black | 0.5s | Início do vídeo |
| Fade out to black | 1.0s | Fim do vídeo |
| Fade in from black | 1.0s | End credits |

### Dentro de Cenas (jump cuts)

| Tipo | Duração | Uso |
|------|---------|-----|
| Cross dissolve | 0.2s | Esconder jump cut dentro de uma cena |
| Cross dissolve | 0.3s | Cortar erro ou seção problemática |

### Transições Proibidas

- **Wipe** — qualquer direção
- **Slide** — qualquer direção
- **Iris** — abertura ou fechamento
- **Zoom transition** — zoom digital como transição entre cenas
- **Dip to black** entre cenas (apenas no início e fim)
- **Flash** — qualquer flash branco ou de cor
- **Page turn / Page curl**
- **Cube / 3D transitions**

---

## 5. Posição dos Títulos

### Title Cards

| Parâmetro | Valor |
|-----------|-------|
| Alinhamento horizontal | Centro |
| Alinhamento vertical | 15% da altura a partir do topo |
| Margem lateral mínima | 80px (safe area) |
| Largura máxima do texto | 80% da largura da tela (1536px) |

### Lower Thirds

| Parâmetro | Valor |
|-----------|-------|
| Alinhamento horizontal | Esquerda |
| Margem esquerda | 5% (96px) |
| Alinhamento vertical | 90% da altura (972px) |
| Largura máxima do texto | 60% da largura da tela (1152px) |

### End Credits

| Parâmetro | Valor |
|-----------|-------|
| Alinhamento horizontal | Centro |
| Alinhamento vertical | Variável por elemento (ver `04_END_CREDITS.md`) |
| Margem lateral mínima | 80px (safe area) |

---

## 6. Safe Area

### Definição

A safe area é a região da tela onde texto e elementos visuais overlaid devem permanecer para garantir legibilidade em qualquer contexto de exibição.

### Safe Area para 1920×1080

```
┌────────────────────────────────────────────────┐
│  80px                                    80px  │
│  ┌──────────────────────────────────────────┐  │
│  │                                          │  │
│  │           SAFE AREA (1760 × 920)         │  │
│  │                                          │  │
│  └──────────────────────────────────────────┘  │
│  80px                                    80px  │
└────────────────────────────────────────────────┘
```

| Margem | Valor |
|--------|-------|
| Superior | 80px |
| Inferior | 80px |
| Esquerda | 80px |
| Direita | 80px |

### Elementos dentro da Safe Area

- Todos os title cards
- Todos os lower thirds
- Todos os callouts (retângulos de destaque)
- End credits

### Elementos FORA da Safe Area (não controlados pelo editor)

- Conteúdo da aplicação (navbar, cards, botões, texto)
- Cursor do mouse

> **Nota**: O conteúdo da aplicação pode aparecer fora da safe area. Isso é aceitável — a safe area se aplica apenas aos elementos overlaid adicionados na edição.

---

## 7. Margens e Espaçamento

### Title Cards

| Elemento | Margem |
|----------|--------|
| Título → Subtítulo | 12px |
| Subtítulo → Base do bloco | 0px |
| Bloco → Topo da tela | 15% (162px) |

### Lower Thirds

| Elemento | Margem |
|----------|--------|
| Texto → Borda esquerda | 96px (5%) |
| Texto → Base da tela | 108px (10%) |

### End Credits

| Elemento | Margem |
|----------|--------|
| Título → Subtítulo | 12px |
| Subtítulo → Tecnologias | 96px |
| Tecnologias → GitHub | 96px |
| GitHub → Obrigado | 96px |

---

## 8. Renderização e Exportação

### Configuração de Timeline

| Parâmetro | Valor |
|-----------|-------|
| Resolução | 1920×1080 |
| FPS | 30 |
| Color space | Rec.709 |
| Color depth | 8-bit |
| Aspect ratio | 16:9 |

### Exportação Final

| Parâmetro | Valor |
|-----------|-------|
| Formato | MP4 |
| Codec de vídeo | H.264 (x264) |
| Codec de áudio | AAC |
| Bitrate de vídeo | 8 Mbps (CBR) |
| Bitrate de áudio | 192 Kbps |
| Profile | High |
| Level | 4.0 |
| Encoding | 2-pass |
| Sample rate | 48 kHz |
| Canais | Stereo |
| Volume alvo | -16 LUFS |
| True peak | -1.5 dBTP |

---

## 9. Grid de Alinhamento

### Grid de 12 Colunas (para posicionamento de overlays)

```
1920px / 12 = 160px por coluna

Coluna 1: 0–160px
Coluna 2: 160–320px
Coluna 3: 320–480px
Coluna 4: 480–640px
Coluna 5: 640–800px
Coluna 6: 800–960px (centro)
Coluna 7: 960–1120px
Coluna 8: 1120–1280px
Coluna 9: 1280–1440px
Coluna 10: 1440–1600px
Coluna 11: 1600–1760px
Coluna 12: 1760–1920px
```

### Posicionamento por Grid

| Elemento | Colunas | Alinhamento |
|----------|---------|-------------|
| Title card | 4–9 (centro) | Centralizado |
| Lower third | 1–7 (esquerda) | Alinhado à esquerda |
| End credits | 3–10 (centro) | Centralizado |
| Callout — retângulo | Variável | Sobre o elemento |
