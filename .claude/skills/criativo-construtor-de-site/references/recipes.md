# Receitas concretas

Comandos por etapa. Exemplos em Windows/PowerShell (adapte em outros SOs). Nunca cole tokens/credenciais reais aqui.

## 1. Scaffold + dev server (loop de iteração)

```bash
npm create vite@latest <nome-do-site> -- --template react-ts
cd <nome-do-site>
npm i
npm i -D tailwindcss@3 postcss autoprefixer && npx tailwindcss init -p
npm i react-router-dom motion lucide-react
npm run dev            # ITERE contra isto (HMR, reload em segundos)
```
- **Iteração = `npm run dev`** (HMR). Não use `build`+`preview` pra iterar — é lento e dispara o estouro de memória do rolldown. `build`+`preview` só no **final** (recipe 9).
- **Rotas (multipágina):** `App.tsx` com `<BrowserRouter>`/`<Routes>`/`<Route>` p/ as páginas aprovadas no GATE. `<Navigate>` p/ redirecionar rotas antigas.
- **Framer Motion:** `import { motion } from 'motion/react'`; reveal: `initial`/`whileInView`/`viewport={{ once: true }}`; respeite `useReducedMotion`.

## 2. Arquivos de contexto do projeto (dê as regras uma vez)

Crie no projeto do cliente, e mantenha **enxutos**:
- **`dados-reais.md`** — todo o conteúdo real consolidado (textos, números, depoimentos, contatos, lista de assets). Fonte da verdade pro conteúdo.
- **`design-system.md`** — tokens (OKLCH), par de fontes, e os padrões de seção/componente decididos com a `ui-ux-pro-max`.
- **`CLAUDE.md`** (~100 linhas, no root do site) — convenções: stack, onde ficam as coisas, regras (conteúdo real, WebP, a11y), e ponteiros pros dois acima.

Construa **lendo esses arquivos** em vez de re-perguntar design a cada seção. Lean de propósito: arquivo grande causa "context rot".

## 3. Mapear + raspar o site atual (Firecrawl) — seletivo

`firecrawl_map` → lista de URLs. Depois `firecrawl_scrape` **só** nas páginas que (a) definem a arquitetura e (b) têm assets — **não raspe tudo** (infla contexto e queima créditos). `formats:["json"]` com schema pedindo textos/listas/URLs de imagem. Sites antigos servem imagens reduzidas — pra original, baixe a URL base de mídia (sem o transform) ou peça um transform grande. Baixe com User-Agent de navegador:
```powershell
Invoke-WebRequest -Uri $url -OutFile $out -Headers @{ "User-Agent"="Mozilla/5.0 ... Chrome/124" }
```
Se o Firecrawl estiver fora, peça o conteúdo/fotos ao usuário (não trave).

## 4. Converter imagens → WebP (batch é o padrão)

Pra mais de ~3 fotos, use um **`build-assets.py`** no projeto (um processo, não um por imagem):
```python
# build-assets.py — rode com: PYTHONUTF8=1 python build-assets.py
from PIL import Image, ImageOps
import os
JOBS = {
  'assets-raw/hero.jpg': 'public/images/hero.webp',
  'assets-raw/servico-1.jpg': 'public/images/servico-1.webp',
  # ...
}
for src, dst in JOBS.items():
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    w, h = im.size; r = min(1.0, 1600 / max(w, h))
    if r < 1: im = im.resize((int(w*r), int(h*r)))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, 'WEBP', quality=82, method=6); print('ok', dst, im.size)
```
Uma foto só → o one-liner `python -c "..."` resolve.

## 5. Folha de contato (curar fotos)
Lote de fotos sem nome → monte uma contact sheet pra identificar antes de plotar:
```bash
PYTHONUTF8=1 python -c "
from PIL import Image, ImageOps, ImageDraw
import glob, os
files=sorted(glob.glob('assets-raw/*'))[:24]
cols=3; t=460; p=12; rows=(len(files)+cols-1)//cols
W=cols*t+(cols+1)*p; H=rows*t+(rows+1)*p
sheet=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
    try: im=ImageOps.exif_transpose(Image.open(f)).convert('RGB')
    except: continue
    im.thumbnail((t,t)); x=p+(i%cols)*(t+p); y=p+(i//cols)*(t+p)
    sheet.paste(im,(x,y)); d.text((x+4,y+4), os.path.basename(f), fill='red')
sheet.save('contact-sheet.jpg', quality=80); print('ok', sheet.size)
"
```

## 6. Pesquisa de nicho/local (WebSearch / firecrawl_search)
Material raso → pesquise fatos **reais** do nicho/local e **cite a fonte** (atrações de uma cidade, normas técnicas de um setor, o que o público procura). Pesquisa fundamenta, não substitui o dado do cliente. Liste as fontes.

## 7. Screenshot de validação (Playwright) — cirúrgico
Screenshot **só a página/seção que mudou** (imagem = caro em contexto). Varredura completa (1440 + 375) só num marco de review. Antes de capturar, desligue animação e dispare reveals:
```js
const s=document.createElement('style');
s.textContent='*{animation:none !important;transition:none !important}';
document.head.appendChild(s);
document.querySelectorAll('img').forEach(i=>i.loading='eager');
const h=document.body.scrollHeight;
for(let y=0;y<h;y+=600){ window.scrollTo(0,y); await new Promise(r=>setTimeout(r,50)); }
window.scrollTo(0,0); await new Promise(r=>setTimeout(r,250));
```
Audite: mocks, botão sem handler, contraste, hover-only, imagem quebrada, menu mobile. Playwright fora → peça pro usuário olhar.

## 8. Tokens OKLCH
`:root` com canais OKLCH + helper no Tailwind (`oklch(var(--x) / <alpha-value>)`). Valores escolhidos com a `ui-ux-pro-max` e gravados no `design-system.md`. Ex.: `--primary: 0.646 0.222 41;` (laranja-segurança). *Por quê OKLCH:* luminosidade perceptual → contraste previsível.

## 9. Build / preview — só no final (Windows-aware)
```bash
npm run build
npm run preview -- --port 4174 --host   # --host libera na rede local
```
- Porta livre por cliente (4174 pode estar ocupada por outro preview).
- Build falhou com "WebAssembly.Memory.grow(): Unable to grow" → é pressão de memória (não erro de código): mate o preview/dev pra liberar RAM e rebuilde.
- Matar porta no Windows: `Get-NetTCPConnection -LocalPort <porta> -State Listen` → `Stop-Process -Id <pid> -Force`.
- Rede local: outro PC na mesma Wi-Fi abre `http://<IP>:<porta>/`; pode precisar de regra de firewall (admin/UAC).

## 10. Deploy (opcional)
SPA precisa de fallback. `vercel.json`: `{ "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }] }`. `.vercelignore` com `dist` + imagens-fonte + temporários. Preview por padrão; produção só se pedirem. Cuidado com o "Vercel Authentication" (Deployment Protection) que exige login por padrão — desligue no painel se o link precisa ser público.
