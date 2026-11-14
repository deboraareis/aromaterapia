# Aromoterapia — Débora Araújo dos Reis

Site institucional estático da aromaterapeuta Débora Araújo dos Reis.

- **Site no ar:** https://wilsonreis.github.io/aromoterapia/
- **Proposta de design e conteúdo:** [docs/proposta-site-debora.md](docs/proposta-site-debora.md)
- **Guia para desenvolvimento (Claude Code):** [CLAUDE.md](CLAUDE.md)

## Stack

Python (Jinja2, só como gerador estático — não roda em produção) + HTML5 + CSS3 + JavaScript vanilla. Saída 100% estática, sem framework, sem build tool de frontend.

## Como rodar

```powershell
uv sync
uv run python build.py --serve
```

Isso builda o site e já sobe um servidor local em http://localhost:8000/index.html — abra esse link no navegador.

**Não abra `dist/index.html` clicando duas vezes** (nem sirva a partir da pasta raiz do projeto): os links internos (`/static/...`, `/blog/...`) são absolutos a partir da raiz do site e só resolvem certo quando `dist/` é a raiz servida por HTTP — por isso o `--serve` existe, ele já cuida disso sozinho. Se preferir os passos manuais:

```powershell
uv run python build.py
cd dist
uv run python -m http.server 8000
```

Se a página abrir sem nenhum CSS, o motivo quase sempre é um desses dois: abriu o arquivo direto (`file://`) em vez de por `http://localhost:8000`, ou rodou o build com a variável `BASE_PATH` ainda definida de uma sessão anterior (ver seção Deploy abaixo) — nesse caso rode `Remove-Item Env:BASE_PATH` e builde de novo.

## Estrutura

```
templates/     páginas e componentes Jinja2 (base, home, blog, política de privacidade)
static/        css, js e imagens
content/blog/  artigos do blog em Markdown (front-matter + corpo)
build.py       gerador estático — também concentra a configuração do site
                (nome, WhatsApp, e-mail, Instagram, domínio, BASE_PATH)
docs/          proposta de design/conteúdo original do projeto
dist/          saída gerada (não versionada — recriada a cada build)
```

## Deploy

O site publicado vem da branch `gh-pages` (histórico próprio, contém só o conteúdo de `dist/`), separada do código-fonte em `master`. Como é um GitHub Pages "de projeto" (`wilsonreis.github.io/aromoterapia/`), o build de publicação precisa do prefixo de caminho correto:

```powershell
$env:BASE_PATH = "/aromoterapia"
uv run python build.py
Remove-Item Env:BASE_PATH   # importante: sem isso, os próximos builds da sessão saem com o prefixo errado
```

Detalhes completos do fluxo de deploy estão no `CLAUDE.md`.

## Status

Fase inicial — depoimentos são placeholders (marcados no código), e alguns dados de contato/domínio ainda podem mudar conforme a Débora revisa o site.
