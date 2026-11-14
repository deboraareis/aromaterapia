"""Gerador de site estático: renderiza templates/ + content/blog/*.md para dist/.

Uso:
    uv run python build.py
"""

from __future__ import annotations

import datetime as dt
import functools
import http.server
import os
import shutil
import sys
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

RAIZ = Path(__file__).parent
TEMPLATES = RAIZ / "templates"
CONTEUDO_BLOG = RAIZ / "content" / "blog"
ESTATICOS = RAIZ / "static"
SAIDA = RAIZ / "dist"

MESES = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
]

# ---------------------------------------------------------------------------
# Configuração central do site — ajuste aqui números, e-mail e textos globais.
# ---------------------------------------------------------------------------
NUMERO_WHATSAPP = "5521999612728"
MENSAGEM_WHATSAPP = "Olá, Débora! Vim pelo site e gostaria de agendar uma consulta."

# Prefixo de caminho para todos os links internos (/static/..., /blog/...).
# - Domínio próprio ou GitHub Pages "de usuário" (nome.github.io): deixe "".
# - GitHub Pages "de projeto" sem domínio próprio (nome.github.io/repo/): use "/repo".
# Pode ser sobrescrito sem editar o arquivo: BASE_PATH=/repo uv run python build.py
BASE_PATH = os.environ.get("BASE_PATH", "")

SITE = {
    "nome": "Débora Araújo dos Reis",
    "slogan": "aromaterapeuta",
    "titulo": "Débora Araújo dos Reis — Aromaterapeuta | Equilíbrio corpo e mente",
    "descricao": (
        "Aromaterapia individual e personalizada com Débora Araújo dos Reis. "
        "Consultas presenciais e online. Agende pelo WhatsApp."
    ),
    "cor_tema": "#6b7f5e",
    "url": "https://seudominio.com.br",  # TODO: substituir pelo domínio real ao publicar
    "email": "debora.adosreis2@gmail.com",
    "instagram": "https://instagram.com/deboraareis90",
    "whatsapp_numero": NUMERO_WHATSAPP,
    "whatsapp_exibicao": "Agende pelo WhatsApp",
    "whatsapp_link": (
        f"https://wa.me/{NUMERO_WHATSAPP}?text={MENSAGEM_WHATSAPP}".replace(" ", "%20")
    ),
    "data_atualizacao": dt.date.today().strftime("%d/%m/%Y"),
}


def data_exibicao(data: dt.date) -> str:
    return f"{data.day} de {MESES[data.month - 1]} de {data.year}"


def carregar_posts() -> list[dict]:
    posts = []
    if not CONTEUDO_BLOG.exists():
        return posts

    for arquivo in sorted(CONTEUDO_BLOG.glob("*.md")):
        if arquivo.stem.startswith("_"):
            continue  # arquivos de exemplo/rascunho não são publicados

        post = frontmatter.load(arquivo)
        data = post.get("data")
        if isinstance(data, str):
            data = dt.date.fromisoformat(data)
        elif isinstance(data, dt.datetime):
            data = data.date()

        corpo_html = markdown.markdown(post.content, extensions=["extra"])

        posts.append({
            "slug": post.get("slug", arquivo.stem),
            "titulo": post.get("titulo", arquivo.stem),
            "resumo": post.get("resumo", ""),
            "capa": post.get("capa"),
            "data": data,
            "data_exibicao": data_exibicao(data) if data else "",
            "corpo_html": corpo_html,
        })

    posts.sort(key=lambda p: p["data"] or dt.date.min, reverse=True)
    return posts


def preparar_saida(slugs_atuais: set[str]) -> None:
    """Garante dist/ atualizado sem apagar a árvore inteira (evita conflito de
    permissão no Windows quando um servidor local está com dist/ aberto)."""
    SAIDA.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ESTATICOS, SAIDA / "static", dirs_exist_ok=True)

    pasta_blog = SAIDA / "blog"
    if pasta_blog.exists():
        for arquivo in pasta_blog.glob("*.html"):
            if arquivo.stem not in slugs_atuais and arquivo.name != "index.html":
                arquivo.unlink()  # remove artigos renomeados/removidos


def gerar_sitemap(urls: list[str]) -> None:
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        linhas.append(f"  <url><loc>{SITE['url']}{BASE_PATH}{url}</loc></url>")
    linhas.append("</urlset>")
    (SAIDA / "sitemap.xml").write_text("\n".join(linhas), encoding="utf-8")

    robots = f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n"
    (SAIDA / "robots.txt").write_text(robots, encoding="utf-8")


def main() -> None:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    posts = carregar_posts()
    preparar_saida({post["slug"] for post in posts})
    urls_geradas = []

    def renderizar(template_nome: str, destino: Path, canonical: str, **contexto) -> None:
        destino.parent.mkdir(parents=True, exist_ok=True)
        template = env.get_template(template_nome)
        html = template.render(site=SITE, base=BASE_PATH, canonical=canonical, **contexto)
        destino.write_text(html, encoding="utf-8")
        urls_geradas.append(canonical)

    renderizar("index.html", SAIDA / "index.html", "/")
    renderizar("blog_index.html", SAIDA / "blog" / "index.html", "/blog/index.html", posts=posts)
    renderizar("politica_privacidade.html", SAIDA / "politica-privacidade.html", "/politica-privacidade.html")

    for post in posts:
        renderizar(
            "blog_post.html",
            SAIDA / "blog" / f"{post['slug']}.html",
            f"/blog/{post['slug']}.html",
            post=post,
        )

    gerar_sitemap(urls_geradas)

    print(f"Build concluído: {len(urls_geradas)} páginas geradas em {SAIDA}")


def servir(porta: int = 8000) -> None:
    """Builda e serve dist/ em http://localhost:<porta>/ — sempre com a raiz
    correta (evita o erro comum de esquecer o `cd dist` ou abrir o arquivo
    direto no navegador, que quebra os caminhos /static/... e /blog/...)."""
    main()
    if BASE_PATH:
        print(
            f"Aviso: BASE_PATH='{BASE_PATH}' está definido — os links do site "
            f"esperam ficar em http://localhost:{porta}{BASE_PATH}/, não na raiz. "
            f"Para prévia local, rode sem BASE_PATH definido."
        )
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SAIDA))
    print(f"Servindo em http://localhost:{porta}/index.html (Ctrl+C para parar)")
    http.server.ThreadingHTTPServer(("", porta), handler).serve_forever()


if __name__ == "__main__":
    if "--serve" in sys.argv:
        servir()
    else:
        main()
