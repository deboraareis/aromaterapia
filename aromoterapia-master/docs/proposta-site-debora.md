# Proposta de Site — Débora Araújo dos Reis | Aromaterapia

> Documento de arquitetura, design e conteúdo para o site institucional estático de Débora Araújo dos Reis, aromaterapeuta.
> Stack: **Python (build/geração) + HTML5 + CSS3 + JavaScript vanilla**, saída 100% estática.

---

## Sumário

1. [Resumo executivo](#1-resumo-executivo)
2. [Estudo de mercado (benchmarking)](#2-estudo-de-mercado-benchmarking)
3. [Persona](#3-persona)
4. [Arquitetura de informação: página única vs. multi-página](#4-arquitetura-de-informação-página-única-vs-multi-página)
5. [Identidade visual](#5-identidade-visual)
6. [Tipografia](#6-tipografia)
7. [Wireframes (mobile, tablet, desktop)](#7-wireframes-mobile-tablet-desktop)
8. [Responsividade — estratégia mobile-first](#8-responsividade--estratégia-mobile-first)
9. [UX e conversão](#9-ux-e-conversão)
10. [Conteúdo seção a seção](#10-conteúdo-seção-a-seção)
11. [Fotografia](#11-fotografia)
12. [SEO](#12-seo)
13. [Acessibilidade (WCAG)](#13-acessibilidade-wcag)
14. [LGPD e aviso legal](#14-lgpd-e-aviso-legal)
15. [Blog — pauta editorial](#15-blog--pauta-editorial)
16. [Arquitetura técnica (Python + estrutura de pastas)](#16-arquitetura-técnica-python--estrutura-de-pastas)
17. [Performance](#17-performance)
18. [Cronograma](#18-cronograma)
19. [Checklist final de lançamento](#19-checklist-final-de-lançamento)
20. [Próximos passos](#20-próximos-passos)

---

## 1. Resumo executivo

O site da Débora precisa cumprir um único objetivo comercial: **transformar uma pessoa ansiosa, curiosa ou cética em alguém que manda mensagem no WhatsApp para agendar uma consulta.** Tudo neste documento — cor, fonte, estrutura de pastas — está subordinado a esse objetivo.

Decisões centrais desta proposta:

- **Não** vamos fazer um site de "clínica corporativa". Vamos fazer um site de **boutique de bem-estar**: elegante, quente, pessoal, com a Débora como rosto e voz — não um catálogo de serviços genérico.
- Estrutura em **página única (one-page) institucional**, com seções por âncora, complementada por **páginas reais separadas** para Blog (SEO) e Política de Privacidade/LGPD (exigência legal). Justificativa na seção 4.
- Paleta baseada em **verde sálvia + off-white quente + bege + toque de lavanda e dourado** — a combinação mais consistentemente usada por marcas de aromaterapia e bem-estar validadas na pesquisa (seção 2 e 5).
- Tipografia: serifada elegante para títulos (**Fraunces**) + sans-serif limpa para corpo de texto (**Inter** ou **Work Sans**) — tendência 2026 para marcas de bem-estar (seção 6).
- Tecnicamente, replicamos o **mesmo padrão de qualidade** já usado em `C:\w\p\meu_site_pessoal` (CSS com custom properties, mobile-first, tema claro/escuro, `clamp()` para tipografia fluida, zero frameworks pesados) — só que com paleta, tom de voz e conteúdo completamente diferentes. Isso garante um site rápido, sem dependências, fácil de manter sozinho.
- Python entra como **gerador de site estático** (Jinja2), não como servidor: o resultado final publicado é HTML/CSS/JS puro, hospedável de graça (GitHub Pages, Netlify, Cloudflare Pages).

Este documento prioriza **decisões acionáveis e justificadas** em vez de volume de páginas — cada seção diz o quê, o porquê e como implementar.

---

## 2. Estudo de mercado (benchmarking)

### 2.1 O que foi analisado

Pesquisa dirigida (2026) sobre padrões de design em três categorias sobrepostas ao nicho da Débora:

1. **Sites de terapeutas/aromaterapeutas individuais** (autônomos, não clínicas)
2. **Marcas de aromaterapia e óleos essenciais** (Neal's Yard Remedies, Aromatherapy Associates, linhas de produto)
3. **Wellness/spa websites** — tendências de UX e conversão para 2026

### 2.2 Padrões que se repetem (o que vamos adotar)

| Padrão observado | Por que funciona | Como aplicamos aqui |
|---|---|---|
| Muito espaço em branco, layout desobstruído | Comunica calma antes mesmo de ler o texto — é a "sala de espera" digital | Seções com padding generoso, nunca mais de 3 colunas, respiro entre blocos |
| Paleta **quieta e opaca**, nunca cores primárias saturadas | Cores vivas geram alerta/estímulo — o oposto do que a aromaterapia promete | Verde sálvia, bege, off-white (seção 5) |
| Cabeçalho fixo (sticky), enxuto, com CTA sempre visível | Em mobile, o CTA precisa estar a um toque de distância o tempo todo | Header sticky com botão "Agendar" sempre visível |
| Fio narrativo pessoal (a terapeuta é o produto) | Diferente de clínica: aqui a confiança é 1:1 com a pessoa | Seção "Sobre" robusta, com foto, voz em primeira pessoa, formação |
| Botão de WhatsApp flutuante e persistente | +75% do tráfego de bem-estar vem do celular via redes sociais/WhatsApp; cada toque a mais custa conversão | Botão flutuante fixo no canto inferior direito em todas as páginas |
| Prova social acima da dobra ou logo após o hero | Depoimentos/credenciais reduzem ceticismo rápido | Seção de depoimentos com destaque, formação/certificações visíveis |
| FAQ em acordeão | Tira objeções ("substitui tratamento médico?") sem poluir a página | Seção FAQ com JS leve (seção 9) |
| Fontes serifadas elegantes em títulos + sans-serif no corpo | Combinação lida como "premium" sem parecer corporativo | Fraunces + Inter/Work Sans (seção 6) |
| Site "conta uma história", não só lista serviços | Wellness em 2026 se afasta do formato "menu de procedimentos" | Fluxo Hero → Sobre → O que é Aromaterapia → Benefícios → Serviços → Prova social → FAQ → Contato |

### 2.3 O que vamos evitar deliberadamente

- **Excesso de informação técnica/clínica na home** (linguagem de bula) — isso pertence ao blog, não à página principal.
- **Carrosséis automáticos** grandes no hero — prejudicam performance e Core Web Vitals, e o conteúdo "por trás" nunca é visto.
- **Formulários de contato longos** — um clique para WhatsApp converte mais que um formulário de 8 campos para uma prática solo.
- **Frameworks CSS pesados (Bootstrap etc.)** — desnecessários para um site de poucas páginas; custam performance sem ganho real.
- **Prometer efeito clínico/médico** nos textos (ex.: "cura", "trata") — além de eticamente incorreto, gera risco regulatório (ver seção 14).

### Fontes consultadas

- [21 Best Therapist Websites (Examples) 2026 — Colorlib](https://colorlib.com/wp/therapist-websites/)
- [Aromatherapy Website Design — HealthHosts](https://www.healthhosts.com/website-design/aromatherapy/)
- [Top therapist websites: 21 examples — Wild Berry Studio](https://www.wildberry.studio/blog/top-therapist-websites-design-inspiration)
- [2026 Web Design Trends for Wellness Brands — SMPLY Studio](https://smply.studio/2026-web-design-trends-wellness/)
- [Best Google Fonts for Web Design in 2026 — Jade Agard Design](https://jadeagarddesign.com/best-google-fonts-for-web-design/)
- [Choosing Colors and Fonts for Health & Wellness Websites — Wellness Hive Design Studio](https://www.wellnesshivedesign.com/blog/choosing-the-right-colors-and-fonts-for-your-health-and-wellness-website)
- [Med Spa Websites in 2026: Conversion System — Unicorn Platform](https://unicornplatform.com/blog/med-spa-websites-in-2026/)
- [LGPD na Saúde — cartilha OAB/DF](https://oabdf.org.br/wp-content/uploads/2022/01/Cartilha-LGPD-na-Saude.pdf)

Além da pesquisa acima, as duas propostas fornecidas por você (ChatGPT e Gemini) foram usadas como insumo — convergem no essencial (paleta terrosa, tipografia serifada+sans, mobile-first, WhatsApp como CTA principal, FAQ em acordeão). Este documento herda esses consensos e resolve os pontos onde elas divergiam (ex.: estrutura one-page vs. multi-página — decidido na seção 4).

---

## 3. Persona

**Nome fictício:** Marina
**Idade:** 38–50 anos
**Perfil:** Profissional liberal ou executiva, rotina intensa, sente estresse/ansiedade/insônia no corpo, já tentou outras abordagens (terapia, academia) e busca algo complementar.
**Comportamento digital:** Descobre a Débora via indicação ou Instagram. Acessa o site **pelo celular**, no intervalo do trabalho ou à noite. Lê rápido, decide rápido. Se não achar o essencial (quem é, o que oferece, quanto custa/como agendar) em poucos segundos, sai.
**O que ela precisa ver, nesta ordem:** (1) isso é para mim? (2) quem é essa profissional, ela é confiável? (3) como funciona na prática? (4) outras pessoas confiaram? (5) como eu agendo agora?
**Objeção mais comum:** "isso substitui remédio/terapia?" → precisa de resposta clara e honesta no FAQ.

**Persona secundária:** José, 60+, indicado por familiar, prefere ligação/WhatsApp de voz a formulário, valoriza clareza de preço e credenciais.

---

## 4. Arquitetura de informação: página única vs. multi-página

As duas propostas anteriores convergiam em quase tudo, exceto aqui: o documento do ChatGPT sugeria multi-página completa (`index.html`, `sobre.html`, `servicos.html`...); o do Gemini sugeria one-page. **Decisão: híbrido**, pelos motivos abaixo.

### Decisão

- **Home em página única (one-page)** com as seções institucionais (Hero, Sobre, Aromaterapia, Serviços, Depoimentos, FAQ, Contato), navegáveis por âncora com scroll suave — exatamente como em `meu_site_pessoal/index.html`, que já valida esse padrão para o mesmo tom "portfólio pessoal elegante".
- **Blog em páginas reais separadas** (`blog/index.html` + uma página por artigo) — obrigatório para SEO: cada artigo precisa de URL própria, `<title>` e meta description próprios, para rankear individualmente no Google.
- **Política de Privacidade em página própria** (`politica-privacidade.html`) — exigência prática de LGPD/transparência; não faz sentido misturado à home.

### Por que não 100% one-page

Uma home one-page pura mistura tudo num único `<title>`/URL — ótimo para navegação, péssimo para SEO de conteúdo (o blog nunca rankearia bem) e para compartilhar links diretos de um artigo no Instagram/WhatsApp.

### Por que não 100% multi-página

Multi-página completa (uma página HTML por seção institucional) obriga a visitante a recarregar a página para ir de "Sobre" a "Serviços" — fricção desnecessária num site pequeno, e pior em mobile (mais requisições, mais tempo de carregamento percebido).

### Mapa do site

```
/ (index.html)                     → Home one-page com âncoras:
  #inicio      Hero
  #sobre       Sobre a Débora
  #aromaterapia O que é Aromaterapia + benefícios
  #servicos    Serviços / modalidades de atendimento
  #depoimentos Prova social
  #faq         Perguntas frequentes
  #contato     Contato + CTA final

/blog/                             → Índice do blog (cards de artigos)
/blog/<slug-do-artigo>.html        → Página individual de artigo

/politica-privacidade.html         → LGPD, aviso legal, cookies
```

Navegação principal do header aponta para as âncoras da home + link "Blog". O footer replica os links + política de privacidade.

---

## 5. Identidade visual

### 5.1 Paleta de cores

Critério: nada saturado, tudo "respirável". Verde sálvia como cor de marca (natureza, cura, crescimento), off-white/bege como base (calma, clareza), lavanda como acento emocional (o próprio óleo mais associado a aromaterapia), dourado suave como detalhe de "boutique" (não de luxo ostentador, mas de cuidado refinado).

**Modo claro (padrão)**

| Token | Uso | HEX |
|---|---|---|
| `--bg` | Fundo geral da página | `#FBF8F2` |
| `--surface` | Cards, header | `#FFFFFF` |
| `--surface-2` | Seções alternadas | `#F3EEE1` |
| `--text` | Texto principal | `#2B2A25` |
| `--muted` | Texto secundário | `#71695C` |
| `--border` | Bordas, divisores | `#E6DFCE` |
| `--accent` (verde sálvia) | Marca, links, ícones, CTA secundário | `#6B7F5E` |
| `--accent-ink` | Texto sobre `--accent` | `#FFFFFF` |
| `--accent-soft` | Fundo suave de destaque (chips, badges) | `#E9EEE3` |
| `--accent-2` (lavanda) | Detalhes emocionais, hover, ícones de "benefícios" | `#8E7FA3` |
| `--gold` (dourado suave) | Selos, divisores decorativos, aspas de depoimento | `#C9A467` |
| `--whatsapp` | Botão flutuante | `#25D366` |

**Modo escuro** (mesma lógica de `meu_site_pessoal`, via `prefers-color-scheme` + atributo `data-tema`)

| Token | HEX |
|---|---|
| `--bg` | `#1B1D18` |
| `--surface` | `#232620` |
| `--surface-2` | `#2B2E26` |
| `--text` | `#EDEAE0` |
| `--muted` | `#A8A190` |
| `--border` | `#383B31` |
| `--accent` | `#9BB08A` |
| `--accent-ink` | `#12140F` |
| `--accent-soft` | `#2C3226` |
| `--accent-2` | `#B3A2C4` |
| `--gold` | `#D8BC85` |

> Contraste verificado para atender **WCAG AA** (texto normal ≥ 4.5:1) nas combinações texto/fundo de ambos os temas — validar com Lighthouse antes do lançamento (checklist seção 19).

### 5.2 Aplicação da cor (regra prática)

- Fundo geral sempre `--bg`/`--surface` — **nunca** aplicar `--accent` como fundo de seção inteira (cansa e reduz legibilidade).
- `--accent` é para: logotipo, links, ícones de benefício, CTA primário.
- `--accent-2` (lavanda) é para: destaques pontuais — ex. palavra-chave em citação, ícone de "equilíbrio emocional".
- `--gold` é para: aspas de depoimento, selo de certificação, divisor decorativo entre seções — **com moderação**, é o tempero, não o prato principal.
- WhatsApp verde (`#25D366`) **só** no botão flutuante e CTAs de agendamento — reconhecimento imediato do ícone.

---

## 6. Tipografia

| Papel | Fonte | Fallback | Peso |
|---|---|---|---|
| Títulos (H1–H3, logotipo) | **Fraunces** (Google Fonts) — serifada contemporânea, curvas suaves, aparência editorial/boutique, muito usada em marcas de wellness em 2026 | Georgia, serif | 600 (semibold), itálico para destaques pontuais |
| Corpo de texto, botões, navegação | **Inter** ou **Work Sans** (Google Fonts) — alta legibilidade em telas pequenas, neutra e "amigável" | system-ui, sans-serif | 400 regular / 600 para ênfase |

**Por quê Fraunces em vez de Playfair Display/Cormorant (sugeridas nas propostas anteriores):** Playfair e Cormorant são ótimas, mas já saturadas visualmente no nicho (praticamente todo site de terapeuta usa uma das duas). Fraunces entrega a mesma sensação "elegante e humana", tem eixos variáveis (permite ajustar "softness"/optical size sem carregar múltiplos arquivos de fonte) e ainda é pouco comum no nicho brasileiro de bem-estar — diferenciação visual real.

**Regras de implementação:**
- Carregar via `<link rel="preconnect">` + `font-display: swap` — nunca bloquear a renderização por causa de fonte (seção 17).
- Tamanhos com `clamp()` (mesma técnica do site de referência), nunca `px` fixo — títulos escalam de ~1.6rem (mobile) a ~2.8rem (desktop) fluidamente.
- Máximo 2 famílias de fonte no projeto inteiro. Hierarquia vem de peso e tamanho, não de mais fontes.

---

## 7. Wireframes (mobile, tablet, desktop)

### 7.1 Mobile (< 768px) — coluna única, thumb-friendly

```
┌───────────────────────────┐
│ ☰   Débora Araújo   [Agendar] │  ← header sticky, CTA sempre visível
├───────────────────────────┤
│                           │
│   [foto Débora – hero]    │
│                           │
│  Restabeleça seu          │
│  equilíbrio com           │
│  aromaterapia              │
│                           │
│  [ Agendar no WhatsApp ]  │  ← CTA primário, largura quase total
│  [ Conhecer os serviços ] │  ← CTA secundário
│                           │
├───────────────────────────┤
│  Sobre a Débora           │
│  [foto menor] + bio curta │
├───────────────────────────┤
│  O que é aromaterapia     │
│  [ícone] benefício 1      │
│  [ícone] benefício 2      │
│  [ícone] benefício 3      │  ← empilhado, 1 coluna
├───────────────────────────┤
│  Serviços                 │
│  [card 1 – full width]    │
│  [card 2 – full width]    │
│  [card 3 – full width]    │
├───────────────────────────┤
│  Depoimentos (swipe)      │
│  " ...depoimento... "     │
├───────────────────────────┤
│  FAQ (acordeão)           │
│  ▸ pergunta 1             │
│  ▸ pergunta 2             │
├───────────────────────────┤
│  Contato                  │
│  [ Agendar no WhatsApp ]  │
├───────────────────────────┤
│  Rodapé                   │
└───────────────────────────┘
        [WhatsApp ●] ← flutuante, fixo, sempre visível
```

### 7.2 Tablet (768–1024px) — 2 colunas nos blocos de card

```
┌─────────────────────────────────────────┐
│ Logotipo        Sobre Serviços FAQ  [Agendar] │
├─────────────────────────────────────────┤
│   [foto hero]        Restabeleça seu      │
│                       equilíbrio...       │
│                       [Agendar] [Serviços]│
├─────────────────────────────────────────┤
│  Benefícios: [ícone 1] [ícone 2]          │
│              [ícone 3] [ícone 4]          │  ← grid 2 col
├─────────────────────────────────────────┤
│  Serviços: [card 1]  [card 2]             │
│            [card 3]  [card 4]             │  ← grid 2 col
├─────────────────────────────────────────┤
│  Depoimentos: [dep 1]     [dep 2]         │
└─────────────────────────────────────────┘
```

### 7.3 Desktop / notebook (> 1024px) — até 3 colunas, hero lado a lado

```
┌───────────────────────────────────────────────────────────┐
│ Logotipo     Sobre  Aromaterapia  Serviços  FAQ  Contato  [Agendar] │
├───────────────────────────────────────────────────────────┤
│  Restabeleça seu equilíbrio         │                     │
│  físico e emocional através da      │   [foto hero        │
│  aromaterapia.                      │    grande, à        │
│  [Agendar no WhatsApp] [Serviços]   │    direita]         │
├───────────────────────────────────────────────────────────┤
│  Sobre a Débora     │  [foto + bio + credenciais em chips] │
├───────────────────────────────────────────────────────────┤
│  [ícone] benefício 1  [ícone] benefício 2  [ícone] benefício 3 │
├───────────────────────────────────────────────────────────┤
│  [card serviço 1]   [card serviço 2]   [card serviço 3]    │
├───────────────────────────────────────────────────────────┤
│  [depoimento 1]      [depoimento 2]      [depoimento 3]    │
├───────────────────────────────────────────────────────────┤
│  FAQ em 2 colunas (perguntas à esq., respostas expandem)   │
├───────────────────────────────────────────────────────────┤
│  Contato — card centralizado, max-width 700px              │
├───────────────────────────────────────────────────────────┤
│  Rodapé — links à esquerda, redes sociais à direita        │
└───────────────────────────────────────────────────────────┘
```

Container central com `max-width: 1180px` (mesmo valor de `meu_site_pessoal`), evitando linhas de texto excessivamente longas em monitores grandes/ultrawide.

---

## 8. Responsividade — estratégia mobile-first

Mesma técnica comprovada em `meu_site_pessoal/css/estilos.css`: **CSS mobile-first** (estilo base = mobile, `@media (min-width: ...)` adiciona complexidade progressivamente), `clamp()` para tipografia e espaçamento fluidos, grid `auto-fill`/`minmax()` para cards que se reorganizam sozinhos sem precisar de breakpoint dedicado por componente.

| Breakpoint | Largura | O que muda |
|---|---|---|
| Base (mobile) | até 47.9rem (~767px) | 1 coluna, nav escondida atrás do menu hambúrguer, botões full-width, hero empilhado (texto acima, imagem abaixo ou só texto) |
| `min-width: 48rem` (tablet) | 768px+ | Grids passam a 2 colunas, nav principal ainda pode ficar oculta ou compacta dependendo do espaço |
| `min-width: 64rem` (notebook/desktop) | 1024px+ | Nav completa visível no header, hero em 2 colunas lado a lado, grids em 3 colunas |
| `min-width: 90rem` (desktop grande/TV) | 1440px+ | `max-width` do container passa a limitar o crescimento — layout não "estica", apenas ganha respiro nas margens |

Regras não negociáveis:
- Nenhuma unidade de fonte em `px` fixo — sempre `rem`/`clamp()`.
- Área de toque mínima de **44×44px** em todos os botões/links em mobile (diretriz de acessibilidade e a mesma usada em apps).
- Testar sempre em: iPhone SE (tela pequena real), Android médio, iPad, notebook 13", desktop 24"+.
- `overflow-x: hidden` no `body` para blindar contra qualquer elemento que vaze a largura da viewport.

---

## 9. UX e conversão

- **CTA primário único e consistente**: "Agendar no WhatsApp" (ou "Falar com a Débora"). Aparece: no header, no fim do hero, no fim de cada bloco de serviço, no contato final e no botão flutuante. Nunca dois CTAs primários competindo na mesma tela.
- **Botão flutuante do WhatsApp**: fixo, canto inferior direito, visível em toda navegação (inclusive blog), com `aria-label` claro e leve animação de "pulso" sutil na primeira visita (respeitando `prefers-reduced-motion`).
- **FAQ em acordeão** (JS vanilla, sem dependência): resolve objeções sem exigir rolagem infinita. Perguntas mínimas obrigatórias:
  - Como funciona uma consulta de aromaterapia?
  - A aromaterapia substitui tratamento médico ou psicológico? *(resposta honesta: não substitui — complementa)*
  - Atende presencial, online, ou os dois?
  - Preciso de indicação médica?
  - Quanto custa / como agendar?
- **Prova social visível cedo**: pelo menos um depoimento ou credencial (formação/certificação) já na dobra abaixo do hero — não deixar só para o fim da página.
- **Sem formulário longo**: contato principal é o link direto de WhatsApp (`https://wa.me/55XXXXXXXXXXX?text=...`) com mensagem pré-preenchida educada ("Olá, Débora! Vim pelo site e gostaria de agendar uma consulta."). E-mail como alternativa secundária, igual ao padrão já usado em `meu_site_pessoal` (botão "copiar e-mail").
- **Scroll suave** entre âncoras (`scroll-behavior: smooth` + `scroll-padding-top` para não esconder o título atrás do header sticky).

---

## 10. Conteúdo seção a seção

Tom de voz: **acolhedor, honesto, seguro — nunca "vendedor" ou espiritualista demais.** Primeira pessoa da Débora sempre que possível ("Eu acredito que...", "No meu atendimento..."). Evitar jargão técnico sem explicação e evitar promessas terapêuticas absolutas.

### Hero
- **Título:** "Equilíbrio para o corpo e a mente, com o poder dos óleos essenciais"
- **Subtítulo:** "Atendimento individual e personalizado com Débora Araújo dos Reis, aromaterapeuta."
- **CTAs:** `Agendar no WhatsApp` (primário) · `Conhecer os serviços` (secundário)

### Sobre a Débora
- História pessoal + o que a levou à aromaterapia, formação/certificações em chips (visual idêntico ao componente `.sobre__chips` de `meu_site_pessoal`), filosofia de atendimento em 2–3 parágrafos curtos.

### O que é aromaterapia (+ benefícios)
- Explicação simples em 1 parágrafo (o que é, sem jargão) + 3–4 benefícios em cards com ícone: alívio do estresse, qualidade do sono, equilíbrio emocional, bem-estar físico. Sempre com nota de responsabilidade ("prática complementar, não substitui acompanhamento médico").

### Serviços / modalidades
- Cards: **Consulta individual** (presencial/online), **Blend/sinergia personalizada**, **Atendimentos especiais** (gestantes, idosos, se aplicável). Cada card: o que é, para quem, duração aproximada — sem necessariamente publicar preço fixo se ela preferir "sob consulta".

### Depoimentos
- 3 a 6 depoimentos reais (com nome e, se possível, foto ou iniciais), aspas estilizadas em `--gold`. Nunca inventar depoimento.

### FAQ
- Ver lista da seção 9.

### Contato
- Card único e centralizado: WhatsApp (botão grande), e-mail (secundário), Instagram, aviso de horário de atendimento.

---

## 11. Fotografia

- **Foto de perfil da Débora**: retrato natural, luz suave e natural (não flash direto), fundo neutro ou ambiente de atendimento, expressão acolhedora — mesmo padrão de qualidade do avatar em `meu_site_pessoal` (circular, nítido, bem enquadrado).
- **Fotos de ambiente/produto**: óleos essenciais, plantas, mãos aplicando óleo — luz natural, tons terrosos, sem excesso de still-life genérico de banco de imagens (evitar clichê de "pedras e velas" saturado).
- **Formato técnico**: exportar sempre em **WebP** (fallback JPEG só se necessário), largura máxima real de exibição (não subir imagem de 4000px para um espaço de 400px), compressão a ~75–80% de qualidade.
- **Evitar**: bancos de imagem genéricos e reconhecíveis (reduz autenticidade/confiança — o rosto real da Débora é o maior ativo de conversão do site).

---

## 12. SEO

### 12.1 SEO técnico
- HTML semântico (`<header>`, `<main>`, `<nav>`, `<section>`, `<footer>`) — já é o padrão usado em `meu_site_pessoal`.
- Um único `<h1>` por página (o título do Hero na home; o título do artigo no blog).
- `sitemap.xml` e `robots.txt` na raiz, gerados junto com o build Python.
- URLs amigáveis: `/blog/oleos-essenciais-para-ansiedade.html` (não `/blog/post?id=12`).

### 12.2 Meta tags essenciais (exemplo para a home)

```html
<title>Débora Araújo dos Reis — Aromaterapeuta | Equilíbrio corpo e mente</title>
<meta name="description" content="Aromaterapia individual e personalizada com Débora Araújo dos Reis. Consultas presenciais e online. Agende pelo WhatsApp.">
<meta name="theme-color" content="#6B7F5E">
<link rel="canonical" href="https://seudominio.com.br/">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="Débora Araújo dos Reis — Aromaterapeuta">
<meta property="og:description" content="Equilíbrio para o corpo e a mente com o poder dos óleos essenciais.">
<meta property="og:image" content="https://seudominio.com.br/static/img/og-cover.jpg">
<meta property="og:locale" content="pt_BR">
```

### 12.3 Schema.org (dados estruturados)

Marcar a página como `LocalBusiness` / `HealthAndBeautyBusiness` (ou o tipo mais próximo disponível) para elegibilidade a rich snippets e Google Meu Negócio:

```json
{
  "@context": "https://schema.org",
  "@type": "HealthAndBeautyBusiness",
  "name": "Débora Araújo dos Reis — Aromaterapia",
  "image": "https://seudominio.com.br/static/img/og-cover.jpg",
  "telephone": "+55XXXXXXXXXXX",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Cidade",
    "addressRegion": "UF",
    "addressCountry": "BR"
  }
}
```

### 12.4 SEO local
- Cadastro no **Google Meu Negócio** (Perfil da Empresa) com mesma foto/nome/telefone do site (consistência NAP — Name, Address, Phone).
- Palavras-chave locais nos textos: "aromaterapeuta em [cidade]", "aromaterapia [bairro/cidade]".

---

## 13. Acessibilidade (WCAG)

- Contraste mínimo **AA** (4.5:1 texto normal, 3:1 texto grande) — validado na paleta da seção 5.
- Link "Pular para o conteúdo" (`skip link`), igual ao `.pular` já implementado em `meu_site_pessoal`.
- Foco visível (`:focus-visible`) em todos os elementos interativos — nunca `outline: none` sem substituto.
- Todo ícone decorativo com `aria-hidden="true"`; todo ícone funcional (WhatsApp flutuante, botão de tema, hambúrguer) com `aria-label` descritivo.
- Navegação 100% operável por teclado (Tab/Enter/Espaço), incluindo o menu mobile e o acordeão de FAQ.
- Respeitar `prefers-reduced-motion` — desativar animações não essenciais para quem configurou o SO para isso.
- Texto alternativo (`alt`) descritivo em todas as imagens (não decorativo genérico tipo "imagem1.jpg").

---

## 14. LGPD e aviso legal

Como o site trata, ainda que minimamente, de contexto relacionado a bem-estar/saúde, dois pontos são obrigatórios:

1. **Aviso legal visível** (rodapé + FAQ): *"A aromaterapia é uma prática integrativa e complementar. Não substitui diagnóstico, tratamento médico ou psicológico."* — protege eticamente e reduz risco regulatório.
2. **Página de Política de Privacidade** cobrindo:
   - Quais dados são coletados (ex.: nome/telefone/e-mail se houver formulário; nenhum dado de saúde é coletado *pelo site em si* se o contato é só via WhatsApp externo — deixar isso explícito).
   - Finalidade do uso (responder contato, agendar consulta).
   - Que não há venda/compartilhamento de dados com terceiros.
   - Direitos do titular (acesso, correção, exclusão) e um e-mail de contato para exercê-los.
   - Uso de cookies, se houver analytics (ex.: Google Analytics) — nesse caso, mencionar e linkar a política do serviço terceiro.
3. Se o formulário de contato (caso exista, além do WhatsApp) coletar qualquer dado, incluir um checkbox de consentimento vinculado à política.

---

## 15. Blog — pauta editorial

Sugestão de **30 pautas iniciais** (crescer gradualmente é melhor que publicar 150 de uma vez sem consistência editorial), organizadas por funil:

**Topo de funil (dúvidas gerais, atraem tráfego de busca)**
1. O que é aromaterapia e como ela funciona
2. Óleos essenciais para ansiedade: quais e como usar
3. Aromaterapia ajuda a dormir melhor? O que diz a prática
4. Diferença entre óleo essencial e óleo perfumado
5. Como usar difusor de óleos essenciais em casa
6. Aromaterapia é segura para gestantes?
7. Aromaterapia para crianças: cuidados importantes
8. Óleos essenciais e animais de estimação: o que evitar
9. Lavanda: o óleo mais estudado da aromaterapia
10. Óleo de hortelã-pimenta: usos e benefícios

**Meio de funil (aprofundamento, começam a considerar consulta)**
11. Como é uma primeira consulta de aromaterapia
12. Blend personalizado: o que é e por que faz diferença
13. Aromaterapia como complemento à terapia/psicoterapia
14. Aromaterapia no ambiente de trabalho: reduzindo o estresse do dia a dia
15. Rotina noturna com aromaterapia para melhorar o sono
16. Aromaterapia para enxaqueca: o que a prática pode oferecer
17. Óleos essenciais e menopausa
18. Aromaterapia para burnout: um olhar complementar
19. Como escolher óleos essenciais de qualidade (o que checar no rótulo)
20. Aromaterapia e Ayurveda: relação e diferenças

**Fundo de funil (prova social, autoridade, decisão)**
21. Perguntas que meus pacientes mais fazem antes da primeira consulta
22. Minha trajetória: por que me tornei aromaterapeuta
23. Estudo de caso (anonimizado): acompanhamento de um caso de ansiedade
24. O que levar/esperar na sua primeira sessão comigo
25. Atendimento online x presencial: qual escolher

**Sazonais / sempre-verdes**
26. Aromaterapia para o inverno: imunidade e conforto respiratório
27. Óleos essenciais para relaxar nas festas de fim de ano
28. Aromaterapia para a volta às aulas: ansiedade dos filhos
29. Autocuidado no Dia das Mães com aromaterapia
30. Como montar um kit básico de aromaterapia em casa

**Uso de IA (ChatGPT/Claude) para produção de conteúdo:** usar como *assistente de rascunho e revisão*, nunca publicar sem revisão da própria Débora — autenticidade e precisão técnica (evitar alegações de saúde incorretas) são o diferencial de confiança do blog.

---

## 16. Arquitetura técnica (Python + estrutura de pastas)

### 16.1 Abordagem

Python entra como **gerador de site estático** via [Jinja2](https://jinja.palletsprojects.com/): um script (`build.py`) lê templates HTML + conteúdo (blog em Markdown/front-matter) e compila tudo em arquivos `.html` puros dentro de `dist/`. O que vai para o ar é **só HTML/CSS/JS estático** — sem servidor Python rodando em produção, sem risco, sem custo de hospedagem.

Isso resolve o problema de duplicar header/footer/CTA-flutuante em várias páginas (Home, Blog index, cada artigo, Política de Privacidade) sem copiar e colar HTML manualmente — o que o site puramente estático de `meu_site_pessoal` não precisa resolver por ter só uma página, mas que este projeto precisa por ter blog.

### 16.2 Estrutura de pastas

```
aromoterapia/
├── pyproject.toml
├── uv.lock
├── build.py                      # script Python: renderiza templates -> dist/
├── content/
│   └── blog/
│       ├── oleos-essenciais-para-ansiedade.md   # front-matter: título, data, resumo, capa
│       └── ...
├── templates/
│   ├── base.html                 # layout comum: <head>, header, footer, whatsapp float
│   ├── index.html                # home one-page (estende base.html)
│   ├── blog_index.html           # listagem de artigos
│   ├── blog_post.html            # template de artigo individual
│   └── politica_privacidade.html
├── static/
│   ├── css/
│   │   ├── tokens.css            # variáveis de cor/tipografia (seção 5 e 6)
│   │   ├── estilos.css           # layout, componentes
│   │   └── faq.css
│   ├── js/
│   │   ├── app.js                # tema claro/escuro, ano do rodapé
│   │   ├── menu.js                # menu hambúrguer mobile
│   │   └── faq.js                 # acordeão
│   ├── img/
│   └── icons/
├── dist/                          # saída gerada — publicável direto (GitHub Pages/Netlify)
├── robots.txt
└── sitemap.xml                    # gerado pelo build.py a partir das páginas em dist/
```

### 16.3 Dependências (via uv)

```powershell
uv add jinja2 markdown python-frontmatter
```

- `jinja2` — motor de templates.
- `markdown` + `python-frontmatter` — permite escrever artigos do blog em `.md` com metadados no topo (título, data, resumo, imagem de capa), sem tocar em HTML para cada post novo.

### 16.4 Fluxo de trabalho

1. Editar conteúdo institucional direto nos `templates/*.html` (muda pouco).
2. Escrever novo artigo de blog como um arquivo `.md` em `content/blog/`.
3. Rodar `uv run python build.py` → gera/atualiza tudo em `dist/`.
4. Publicar `dist/` (deploy estático).

Essa é a mesma filosofia "sem build tool pesado" de `meu_site_pessoal`, levada só até o ponto necessário para não repetir HTML manualmente — sem introduzir um framework de frontend (React/Vue) que seria overengineering para um site estático solo.

---

## 17. Performance

- **Core Web Vitals como meta**, não como checklist pós-fato: LCP < 2.5s, CLS ≈ 0, INP < 200ms.
- Imagens: WebP, `loading="lazy"` em tudo abaixo da dobra, `width`/`height` explícitos (evita layout shift).
- Fontes: `font-display: swap`, subsetting (carregar só os pesos usados: 400/600 do corpo, 500/600 do título), `preconnect` para `fonts.googleapis.com`/`fonts.gstatic.com`.
- CSS/JS: um único arquivo de CSS e um único de JS por página (sem múltiplas requisições fragmentadas), minificados no build.
- Zero dependências de frameworks JS pesados — JS vanilla cobre 100% das necessidades (menu, tema, acordeão, botão flutuante).
- Testar com **Google Lighthouse** antes de cada publicação (ver checklist).

---

## 18. Cronograma

| Etapa | Conteúdo | Estimativa |
|---|---|---|
| 1. Fundação técnica | Estrutura de pastas, `build.py`, tokens de design (CSS), tipografia | 2–3 dias |
| 2. Home (HTML/CSS) | Hero → Sobre → Aromaterapia → Serviços → Depoimentos → FAQ → Contato, responsivo nos 3 breakpoints | 4–6 dias |
| 3. Conteúdo real | Textos definitivos da Débora, fotos profissionais, depoimentos reais | paralelo, depende da Débora |
| 4. Blog | Template de artigo + índice + 3–5 primeiros artigos publicados | 2–3 dias |
| 5. Política de Privacidade + SEO técnico | Meta tags, schema.org, sitemap, Google Meu Negócio | 1 dia |
| 6. Acessibilidade + performance | Auditoria Lighthouse, contraste, teclado, `alt`s | 1 dia |
| 7. QA em dispositivos reais | iPhone, Android, tablet, notebook, desktop | 1 dia |
| 8. Publicação | Deploy (GitHub Pages/Netlify/Cloudflare Pages) + domínio próprio | 0.5 dia |

---

## 19. Checklist final de lançamento

**Conteúdo**
- [ ] Todos os textos revisados pela Débora (nenhum texto placeholder/lorem ipsum)
- [ ] Fotos profissionais reais publicadas (nada de banco de imagem genérico no hero)
- [ ] Depoimentos reais, com autorização da pessoa
- [ ] Aviso legal presente (rodapé + FAQ)

**Visual/responsivo**
- [ ] Testado em mobile real (não só DevTools) — iOS e Android
- [ ] Testado em tablet
- [ ] Testado em notebook 13"–15"
- [ ] Testado em desktop grande (1440px+)
- [ ] Modo claro e escuro revisados
- [ ] Nenhum scroll horizontal indesejado em nenhuma largura

**SEO**
- [ ] `<title>` e `<meta description>` únicos por página
- [ ] Open Graph configurado (testar preview no WhatsApp/Instagram)
- [ ] Schema.org validado (Rich Results Test do Google)
- [ ] `sitemap.xml` e `robots.txt` no ar
- [ ] Google Search Console configurado
- [ ] Google Meu Negócio criado/atualizado

**Acessibilidade**
- [ ] Contraste AA validado (Lighthouse/axe)
- [ ] Navegação 100% por teclado
- [ ] `alt` em todas as imagens
- [ ] Skip link funcional

**Performance**
- [ ] Lighthouse ≥ 90 em Performance, Acessibilidade, SEO, Boas Práticas (mobile)
- [ ] Imagens em WebP e comprimidas
- [ ] Fontes com `font-display: swap`

**Legal**
- [ ] Página de Política de Privacidade publicada e linkada no rodapé
- [ ] Consentimento de cookies/analytics, se aplicável

**Técnico**
- [ ] `build.py` roda sem erro do zero (`uv run python build.py`)
- [ ] Link do WhatsApp testado com número real e mensagem pré-preenchida correta
- [ ] Domínio próprio + SSL ativo

---

## 20. Próximos passos

1. Você aprova (ou ajusta) as decisões desta proposta — especialmente paleta, tipografia e a divisão one-page + blog.
2. Débora fornece: textos reais (ou aprova os rascunhos que eu puder gerar a partir do tom de voz definido), fotos, depoimentos, número de WhatsApp comercial.
3. Eu monto a fundação técnica (`build.py`, tokens de CSS, estrutura de pastas) dentro deste mesmo projeto `aromoterapia`.
4. Construímos a Home seção por seção, testando responsividade a cada bloco.
5. Deixamos o Blog e a Política de Privacidade por último, já que dependem menos de decisão visual e mais de conteúdo.
