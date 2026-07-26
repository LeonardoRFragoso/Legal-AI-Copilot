# 🎬 Como Executar a Gravação Automatizada

## ✅ Pré-requisitos

Antes de iniciar a gravação, certifique-se de que:

1. **Backend está rodando** (porta 8000)
   ```bash
   cd backend
   python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Frontend está rodando** (porta 5173)
   ```bash
   cd frontend
   npm run dev -- --host 0.0.0.0 --port 5173
   ```

3. **xdotool está instalado** (para automação de mouse/teclado)
   ```bash
   sudo apt-get install xdotool
   ```

4. **Google Chrome/Chromium está instalado**
   ```bash
   sudo apt-get install google-chrome-stable
   ```

## 🎥 Executar a Gravação

### Opção 1: Teste Simples (Recomendado para começar)

Para testar se a automação está funcionando:

```bash
bash gravacao_teste_simples.sh
```

**O que acontece:**
- Abre o navegador
- Faz login automaticamente
- Mostra se tudo está funcionando

### Opção 2: Gravação Completa (14 Cenas)

Para gravar todas as 14 cenas:

```bash
bash gravacao_automatizada.sh
```

**Importante:**
1. Quando o script pedir, **inicie a gravação de tela** (OBS, ScreenFlow, etc)
2. O script aguardará 10 segundos para sincronização
3. Depois disso, o navegador será controlado automaticamente
4. **NÃO INTERROMPA** o script até que termine

## 📊 O que é Gravado

A gravação automatizada executa **14 cenas** em sequência:

| Cena | Ação | Duração |
|------|------|---------|
| 01-03 | Título, Problema e Arquitetura | 1:45 |
| 04 | Login | 0:30 |
| 05 | Dashboard | 0:30 |
| 06 | Upload de Contrato | 1:00 |
| 07 | Análise | 1:30 |
| 08 | Chat com Agent Router | 1:30 |
| 09 | Análise de Riscos | 1:30 |
| 10 | Automações | 1:00 |
| 11 | Revisão Humana | 1:00 |
| 12 | Métricas de Impacto | 1:00 |
| 13 | Comparação de Contratos | 1:30 |
| 14 | Conclusão | 0:30 |

**Duração Total: ~12 minutos**

## 🔧 Troubleshooting

### Problema: "Navegador não abre"
- Verifique se o Chrome está instalado: `which google-chrome`
- Tente instalar: `sudo apt-get install google-chrome-stable`

### Problema: "xdotool não encontrado"
- Instale: `sudo apt-get install xdotool`

### Problema: "Cliques não funcionam"
- Verifique se o navegador está em foco
- Tente aumentar os delays no script (altere `wait_for_page` de 1 para 2)

### Problema: "Página não carrega"
- Verifique se backend está rodando: `curl http://localhost:8000/api`
- Verifique se frontend está rodando: `curl http://localhost:5173`

## 📝 Personalizando a Gravação

Para modificar a gravação:

1. Abra `gravacao_automatizada.sh`
2. Procure pela cena que deseja modificar (ex: `[CENA 04]`)
3. Ajuste as coordenadas do mouse ou delays
4. Salve e execute novamente

### Coordenadas Comuns:
- **Login "Advogado"**: `530 433`
- **Botão "Entrar"**: `529 364`
- **Navbar items**: `200-970` (eixo Y: 32)
- **Centro da tela**: `960 540`

## ✨ Dicas

- Use `xdotool search --name "Chrome"` para encontrar a janela do Chrome
- Use `xdotool getmouselocation` para descobrir coordenadas do mouse
- Aumente `wait_for_page` se as páginas carregarem lentamente
- Diminua `wait_for_page` se quiser uma gravação mais rápida

## 🎯 Próximas Etapas

Após a gravação:

1. Parar a gravação de tela
2. Exportar vídeo em 1080p
3. Sincronizar áudio com narração
4. Revisar qualidade e transições
5. Fazer upload para plataforma de apresentação

---

**Última atualização:** 25/07/2026
