# Guia de Gravação de Tela — Legal AI Copilot

> Configurações técnicas para captura de tela profissional do vídeo de apresentação do case técnico.

---

## 1. Resolução e Janela

| Item | Valor recomendado |
|------|-------------------|
| Resolução do monitor | 1920×1080 (Full HD) |
| Resolução de captura | 1920×1080 |
| Janela do navegador | Maximizada (1280×720 mínimo) |
| Zoom do navegador | 100% (Ctrl+0) |
| DPI/Escala | 100% (sem scaling) |

---

## 2. Navegador

- **Navegador recomendado**: Google Chrome (versão estável mais recente)
- **Perfil**: Criar um perfil limpo exclusivo para a gravação ("Demo Profile")
- **Tema**: Claro (Light mode) — a aplicação utiliza fundo claro (`bg-gray-50`)
- **Favoritos**: Limpar todos os favoritos
- **Barra de favoritos**: Ocultar (Ctrl+Shift+B)
- **Extensões**: Desabilitar todas, exceto as essenciais

---

## 3. Limpeza do Ambiente

### Desktop
- Remover todos os ícones da área de trabalho (mover para uma pasta temporária)
- Definir papel de parede sólido e neutro (cinza escuro `#333333` ou azul escuro)
- Ocultar dock/barra de tarefas (auto-ocultar)

### Navegador
- Limpar histórico: `chrome://settings/clearBrowserData` → "Todas as datas"
- Limpar cookies e cache
- Limpar dados de preenchimento automático
- Desabilitar preenchimento automático de senhas
- Remover todas as extensões visíveis na barra de ferramentas

### Notificações
- Ativar "Não perturbe" no sistema operacional
- Desabilitar notificações do Chrome: `chrome://settings/content/notifications`
- Desabilitar notificações de apps (Slack, Discord, Email, etc.)
- Silenciar telefone

---

## 4. Tamanho de Fonte e Legibilidade

| Elemento | Recomendação |
|----------|-------------|
| Fonte do navegador | 100% (padrão) |
| Tamanho mínimo visível | 14px equivalente na gravação |
| Contraste | Verificar se textos cinza-claro são legíveis |
| Distância de leitura | Textos devem ser legíveis em 1080p sem zoom do espectador |

> **Teste**: Grave 10 segundos da tela do Dashboard e reproduza em 720p. Se algum texto não for legível, aumentar zoom do navegador para 110%.

---

## 5. Velocidade da Demonstração

- **Pausa entre cliques**: 1–2 segundos para o espectador processar a ação
- **Pausa entre telas**: 2–3 segundos ao trocar de página
- **Tempo de leitura**: Permitir 3–5 segundos para textos longos (resumos, análises)
- **Animações de loading**: Deixar completar naturalmente, não cortar
- **Scroll**: Suave e lento, nunca abrupto

---

## 6. Configurações do OBS Studio

### Captura de Tela

| Parâmetro | Valor |
|-----------|-------|
| Fonte | Display Capture (ou Window Capture do Chrome) |
| Resolução base (Canvas) | 1920×1080 |
| Resolução de saída (Output) | 1920×1080 |
| Scale | Bicubic |

### Vídeo

| Parâmetro | Valor |
|-----------|-------|
| FPS | 30 |
| Formato de gravação | MKV |
| Encoder | x264 (CPU) ou NVENC (GPU se disponível) |
| Rate control | CBR |
| Bitrate | 6000 Kbps |
| Keyframe interval | 2 segundos |
| Preset (x264) | veryfast |
| Profile | high |

### Áudio

| Parâmetro | Valor |
|-----------|-------|
| Sample rate | 48 kHz |
| Canais | Mono (se microfone mono) ou Stereo |
| Bitrate de áudio | 160 Kbps |
| Formato | AAC |
| Dispositivo de entrada | Microfone USB dedicado (não notebook embutido) |
| Filtro de ruído | Noise Suppression (RNNoise) |
| Filtro de gate | Noise Gate (-40 dB threshold) |
| Filtro de compressor | Compressor (ratio 3:1, threshold -18 dB) |
| Ganho | +3 dB a +6 dB se necessário |

### Cenas do OBS

| Cena | Conteúdo |
|------|----------|
| Tela Cheia | Display Capture (aplicação) |
| Apresentador | Webcam + overlay (opcional, para introdução/encerramento) |
| Transição | Cena vazia para fade suave |

---

## 7. Configuração do Microfone

| Item | Recomendação |
|----|--------------|
| Tipo | Headset USB ou microfone de mesa cardioide |
| Distância | 10–15 cm da boca |
| Pop filter | Recomendado para evitar plosivos |
| Ambiente | Sala silenciosa, sem eco (usar materiais absorventes se possível) |
| Nível de entrada | Pico entre -12 dB e -6 dB (não clipar) |
| Monitoramento | Usar fones de ouvido para monitorar áudio em tempo real |

### Filtros recomendados no OBS (em ordem)
1. **Noise Gate** — Threshold: -40 dB, Attack: 5 ms, Hold: 200 ms, Release: 150 ms
2. **Noise Suppression** — Método: RNNoise
3. **Compressor** — Ratio: 3:1, Threshold: -18 dB, Attack: 6 ms, Release: 60 ms
4. **Gain** — +3 dB (ajustar conforme necessário)

---

## 8. Recomendações Gerais de Gravação

- **Gravar em clipes por cena**: Facilita regravações e edição
- **Identificar cada clipe**: Nomear como `cena_01_login.mp4`, `cena_02_dashboard.mp4`, etc.
- **Pausa inicial e final**: Deixar 3 segundos de silêncio e tela estática no início e fim de cada clipe
- **Não gravar com fome/cansaço**: A voz reflete o estado físico
- **Hidratação**: Manter água à disposição, mas não beber durante a gravação
- **Roupas**: Evitar estampas listradas ou muito chamativas (se aparecer em webcam)
- **Iluminação**: Se usar webcam, garantir luz frontal suave, sem contraluz
- **Backup**: Gravar áudio separado em um segundo dispositivo (celular com app gravador) como fallback

---

## 9. Checklist Pré-Gravação (Resumo)

- [ ] Monitor em 1920×1080
- [ ] Escala/DPI em 100%
- [ ] Navegador Chrome com perfil limpo
- [ ] Tema claro, zoom 100%
- [ ] Barra de favoritos oculta
- [ ] Histórico e cache limpos
- [ ] Desktop limpo, papel de parede neutro
- [ ] Notificações desabilitadas (sistema e navegador)
- [ ] "Não perturbe" ativado
- [ ] OBS configurado: 1920×1080, 30 FPS, 6000 Kbps
- [ ] Microfone testado: pico -12 dB a -6 dB
- [ ] Filtros de áudio aplicados (gate, suppression, compressor)
- [ ] Fones de ouvido conectados para monitoramento
- [ ] Água disponível
- [ ] Roteiro impresso ou em segundo monitor
