#!/usr/bin/env python3
"""Transform blog content templates into Clawgency-styled blog pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"

CLASS_MAP = [
    ("article-body", "blog-body"),
    ("article-cta", "blog-article-cta"),
    ("toc-title", "blog-toc-title"),
    ("toc-head", "blog-toc-title"),
    ("toc", "blog-toc"),
    ("callout-icon", "blog-callout-icon"),
    ("callout-title", "blog-callout-title"),
    ("callout-hl", "blog-callout-hl"),
    ("callout-label", "blog-callout-hl"),
    ("callout", "blog-callout"),
    ("pull-quote", "blog-pull-quote"),
    ("stats-row", "blog-stats"),
    ("stat-bar", "blog-stats"),
    ("fact-strip", "blog-stats"),
    ("stat-cell", "blog-stat-cell"),
    ("sb-cell", "blog-stat-cell"),
    ("fs-cell", "blog-stat-cell"),
    ("stat-num", "blog-stat-num"),
    ("sb-num", "blog-stat-num"),
    ("fs-num", "blog-stat-num"),
    ("stat-label", "blog-stat-label"),
    ("sb-label", "blog-stat-label"),
    ("fs-unit", "blog-stat-label"),
    ("name-cards", "blog-name-cards"),
    ("name-card", "blog-name-card"),
    ("nc-emoji", "blog-nc-emoji"),
    ("nc-name", "blog-nc-name"),
    ("nc-date", "blog-nc-date"),
    ("nc-reason", "blog-nc-reason"),
    ("nc-badge", "blog-nc-badge"),
    ("timeline", "blog-timeline"),
    ("tl-item", "blog-tl-item"),
    ("tl-date", "blog-tl-date"),
    ("tl-dot", "blog-tl-dot"),
    ("tl-content", "blog-tl-content"),
    ("tl-name", "blog-tl-name"),
    ("tl-headline", "blog-tl-headline"),
    ("tl-text", "blog-tl-text"),
    ("tl-stat", "blog-tl-stat"),
    ("data-table", "blog-table"),
    ("feat-table", "blog-table"),
    ("offers", "blog-table"),
    ("faq-item", "blog-faq-item"),
    ("faq-q", "blog-faq-q"),
    ("faq-a", "blog-faq-a"),
    ("faq", "blog-faq"),
    ("cta-eyebrow", "blog-cta-eyebrow"),
    ("cta-ey", "blog-cta-eyebrow"),
    ("cta-kicker", "blog-cta-eyebrow"),
    ("related-card", "blog-related-card"),
    ("related-title", "blog-related-title"),
    ("related-label", "blog-related-title"),
    ("related-hl", "blog-related-title"),
    ("related-grid", "blog-related-grid"),
    ("related", "blog-related"),
    ("section-sep", "blog-sep"),
    ("rc-type", "blog-rc-type"),
    ("rc-title", "blog-rc-title"),
    ("chapter-nav", "blog-chapter-nav"),
    ("ch-item", "blog-ch-item"),
    ("ch-num", "blog-ch-num"),
    ("ch-label", "blog-ch-label"),
    ("chapter-block", "blog-chapter-block"),
    ("chapter-num-large", "blog-chapter-num"),
    ("compact-tl", "blog-compact-tl"),
    ("ctl-item", "blog-ctl-item"),
    ("ctl-date", "blog-ctl-date"),
    ("ctl-body", "blog-ctl-body"),
    ("ctl-title", "blog-ctl-title"),
    ("ctl-text", "blog-ctl-text"),
    ("milestone-cards", "blog-milestone-cards"),
    ("quote-grid", "blog-quote-grid"),
    ("quote-card", "blog-quote-card"),
    ("qc-text", "blog-qc-text"),
    ("qc-source", "blog-qc-source"),
    ("evo-item", "blog-evo-item"),
    ("evo-dot", "blog-evo-dot"),
    ("evo-phase", "blog-evo-phase"),
    ("evo-title", "blog-evo-title"),
    ("evo-text", "blog-evo-text"),
    ("evo-chips", "blog-evo-chips"),
    ("evo", "blog-evo"),
    ("chip", "blog-chip"),
    ("arch-header", "blog-arch-header"),
    ("arch-body", "blog-arch-body"),
    ("arch-layer", "blog-arch-layer"),
    ("arch-tag", "blog-arch-tag"),
    ("arch-content", "blog-arch-content"),
    ("arch-title", "blog-arch-title"),
    ("arch-desc", "blog-arch-desc"),
    ("arch-box", "blog-arch-box"),
    ("feat-grid", "blog-feat-grid"),
    ("feat-card", "blog-feat-card"),
    ("fc-icon", "blog-fc-icon"),
    ("fc-title", "blog-fc-title"),
    ("fc-text", "blog-fc-text"),
    ("platform-grid", "blog-platform-grid"),
    ("plat", "blog-plat"),
    ("pq", "blog-pq"),
    ("related", "blog-related"),
    ("sep", "blog-sep"),
    ("check", "blog-check"),
    ("cross", "blog-cross"),
    ("part", "blog-part"),
    ("badge", "blog-badge"),
    ("milestone-cards", "blog-milestone-cards"),
    ("mc-icon", "blog-mc-icon"),
    ("mc-label", "blog-mc-label"),
    ("mc-value", "blog-mc-value"),
    ("mc-desc", "blog-mc-desc"),
    ("mc", "blog-mc"),
]

POSTS = [
    {
        "source": Path("/Users/joshua/Downloads/blog-openclaw-naming-history.html"),
        "output": "openclaw-naming-history.html",
        "breadcrumb": "Von Clawdbot zu OpenClaw",
        "kicker": "OpenClaw · Geschichte &amp; Hintergrund",
        "title_html": 'Von <em>Clawdbot</em> zu <em>Moltbot</em> zu <em>OpenClaw:</em><br>Die vollstaendige Geschichte der Umbenennungen',
        "deck": "OpenClaw hieß nicht immer so. Wie aus einem WhatsApp-Experiment von Peter Steinberger in weniger als 70 Tagen drei Namen, ein Markenrechtstreit mit Anthropic, ein Krypto-Scam und 247.000 GitHub-Stars entstanden.",
        "meta_category": "OpenClaw Hintergrund",
        "read_time": "12 Min.",
    },
    {
        "source": Path("/Users/joshua/Downloads/blog-peter-steinberger-story.html"),
        "output": "peter-steinberger-story.html",
        "breadcrumb": "Peter Steinberger – Die Story",
        "kicker": "OpenClaw · Personen &amp; Hintergruende",
        "title_html": '<span class="accent">Peter Steinberger:</span><br>Von PSPDFKit ueber Burnout<br>zu OpenAI',
        "deck": "Wie ein oesterreichischer Entwickler ein PDF-SDK auf einer Milliarde Geraeten baute, nach 13 Jahren ausbrannte, drei Jahre lang keine Zeile Code schrieb – und dann mit einem WhatsApp-Experiment die KI-Welt erschuettterte.",
        "meta_category": "Personen &amp; Hintergrund",
        "read_time": "14 Min.",
    },
    {
        "source": Path("/Users/joshua/Downloads/blog-wie-openclaw-entstand.html"),
        "output": "wie-openclaw-entstand.html",
        "breadcrumb": "Wie OpenClaw entstand",
        "kicker": "Produktgeschichte · Deep Dive",
        "title_html": 'Wie <span class="accent">OpenClaw</span> entstand:<br>Von einer Stunde Code<br>zu 247.000 GitHub-Stars',
        "deck": (
            "Eine Stunde. Eine WhatsApp-Verbindung. Eine Claude-API. Und die Frage: "
            "Warum gibt es das noch nicht? Das war der Anfang von OpenClaw - dem "
            "Open-Source-KI-Agenten, der die Entwickler-Community 2026 erschuettterte."
        ),
        "meta_category": "Produkt &amp; Technologie",
        "read_time": "16 Min.",
    },
]


def extract_between(text: str, start: str, end: str) -> str:
    i = text.find(start)
    if i == -1:
        return ""
    i += len(start)
    j = text.find(end, i)
    return text[i:j] if j != -1 else text[i:]


def extract_head_block(html: str, tag: str) -> str:
    m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.DOTALL | re.IGNORECASE)
    return m.group(0) if m else ""


def remap_classes(content: str) -> str:
    mapping = sorted(CLASS_MAP, key=lambda x: -len(x[0]))

    def replace_in_class(match: re.Match) -> str:
        classes = match.group(1)
        for old, new in mapping:
            classes = re.sub(rf"(?<![\\w-]){re.escape(old)}(?![\\w-])", new, classes)
        return f'class="{classes}"'

    return re.sub(r'class="([^"]*)"', replace_in_class, content)


def fix_urls(content: str) -> str:
    content = content.replace("https://clawgency.de/blog/", "")
    content = content.replace("https://clawgency.de/#kontakt", "../index.html#kontakt")
    content = content.replace("https://clawgency.de/blog.html", "../blog.html")
    content = content.replace("https://clawgency.de/glossar.html", "../glossar.html")
    content = content.replace("https://clawgency.de/impressum.html", "../impressum.html")
    content = content.replace("https://clawgency.de/datenschutz.html", "../datenschutz.html")
    content = content.replace("https://clawgency.de/", "../")
    content = re.sub(r'href="../([^"]+\.html)"', r'href="../\1"', content)
    content = content.replace('class="btn"', 'class="btn btn--primary"')
    content = content.replace('class="btn-primary"', 'class="btn btn--primary"')
    content = content.replace('class="btn-cta"', 'class="btn btn--primary"')
    return content


def extract_article_body(html: str) -> str:
    # naming history & product story use <article class="article-body">
    body = extract_between(html, '<article class="article-body">', '</article>')
    if not body:
        # peter story: content starts after chapter-nav until footer
        start = html.find('<article class="article-body">')
        if start == -1:
            start = html.find('<nav class="chapter-nav"')
            if start != -1:
                end = html.find("<!-- Footer -->")
                chunk = html[start:end]
                # remove chapter-nav from body for peter - actually keep it inside article
                body = extract_between(html, '<article class="article-body">', '</article>')
        if not body:
            # wie-openclaw: article-body wraps everything
            body = extract_between(html, '<article class="article-body">', '</article>')

    # For peter story, chapter-nav is BEFORE article-body - include stats from after article start
    if "chapter-nav" in html and "blog-chapter-nav" not in body:
        chapter_nav = extract_between(html, '<nav class="chapter-nav', '</nav>')
        if chapter_nav:
            chapter_nav = '<nav class="chapter-nav' + chapter_nav + '</nav>'
            body = chapter_nav + body

    # For wie-openclaw, fact-strip is before article - prepend if missing
    if "fact-strip" in html and "blog-stats" not in body[:500]:
        strip = extract_between(html, '<div class="fact-strip">', '</div>')
        if strip:
            body = '<div class="fact-strip">' + strip + '</div>\n' + body

    return body


def extract_meta(html: str) -> dict:
    title = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    desc = re.search(r'<meta name="description" content="(.*?)"', html, re.DOTALL)
    canonical = re.search(r'<link rel="canonical" href="(.*?)"', html)
    schemas = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.DOTALL)
    og_title = re.search(r'<meta property="og:title" content="(.*?)"', html)
    return {
        "title": title.group(1).strip() if title else "",
        "description": desc.group(1).strip() if desc else "",
        "canonical": canonical.group(1).strip() if canonical else "",
        "schemas": schemas,
        "og_title": og_title.group(1).strip() if og_title else "",
    }


NAV = """  <nav class="nav scrolled" id="nav">
    <div class="nav__inner">
      <a href="../index.html" class="nav__logo">
        <img src="../assets/logo-crab.webp" alt="Clawgency Crab" class="nav__logo-img" width="64" height="64" />
        <span class="nav__logo-text">Clawgency</span>
      </a>
      <ul class="nav__links">
        <li><a href="../index.html#openclaw" class="nav__link">Leistungen</a></li>
        <li><a href="../blog.html" class="nav__link">Blog</a></li>
        <li><a href="../case-studies.html" class="nav__link">Case Studies</a></li>
        <li><a href="../glossar.html" class="nav__link">Glossar</a></li>
      </ul>
      <a href="../index.html#kontakt" class="btn btn--nav">Erstgespraech buchen</a>
      <button class="nav__burger" id="navBurger" aria-label="Menue oeffnen">
        <span></span><span></span><span></span>
      </button>
    </div>
    <div class="nav__mobile" id="navMobile">
      <ul>
        <li><a href="../index.html#openclaw" class="nav__link">Leistungen</a></li>
        <li><a href="../blog.html" class="nav__link">Blog</a></li>
        <li><a href="../case-studies.html" class="nav__link">Case Studies</a></li>
        <li><a href="../glossar.html" class="nav__link">Glossar</a></li>
        <li><a href="../index.html#kontakt" class="btn btn--primary" style="display:inline-block;margin-top:1rem;">Erstgespraech buchen</a></li>
      </ul>
    </div>
  </nav>"""

FOOTER = """  <footer class="footer">
    <div class="container">
      <div class="footer__bottom">
        <p>&copy; 2026 Clawgency · <a href="mailto:clawgency@theaisoftwarecompany.com">clawgency@theaisoftwarecompany.com</a></p>
        <p class="footer__credit">Ein Service von <a href="https://theaisoftwarecompany.com" target="_blank" rel="noopener">The AI Software Company</a></p>
      </div>
    </div>
  </footer>

  <script>
    (function () {
      var nav = document.getElementById('nav');
      var burger = document.getElementById('navBurger');
      burger && burger.addEventListener('click', function () {
        nav.classList.toggle('mobile-open');
        burger.setAttribute('aria-label', nav.classList.contains('mobile-open') ? 'Menue schliessen' : 'Menue oeffnen');
      });
    })();
  </script>"""


def build_post(post: dict) -> str:
    html = post["source"].read_text(encoding="utf-8")
    meta = extract_meta(html)
    body = extract_article_body(html)
    body = remap_classes(body)
    body = fix_urls(body)

    schema_blocks = "\n".join(
        f'  <script type="application/ld+json">\n  {s.strip()}\n  </script>'
        for s in meta["schemas"]
    )

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{meta['title']}</title>
  <meta name="description" content="{meta['description']}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{meta['canonical']}" />

  <meta property="og:type" content="article" />
  <meta property="og:url" content="{meta['canonical']}" />
  <meta property="og:title" content="{meta['og_title'] or meta['title']}" />
  <meta property="og:description" content="{meta['description']}" />
  <meta property="og:image" content="https://clawgency.de/assets/og-image.jpg" />
  <meta property="og:locale" content="de_DE" />
  <meta property="og:site_name" content="Clawgency" />
  <meta name="twitter:card" content="summary_large_image" />

{schema_blocks}

  <link rel="icon" type="image/x-icon" href="../assets/favicon.ico" />
  <link rel="icon" type="image/png" sizes="48x48" href="../assets/favicon-crab-48.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@400;600;700;800&display=swap" />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <noscript><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet" /></noscript>
  <link rel="stylesheet" href="../styles.min.css" />
  <link rel="stylesheet" href="../blog-article.css" />
  <script defer data-domain="clawgency.de" src="https://analytics.taisc.de/js/script.js"></script>
</head>
<body>
{NAV}

  <main class="blog-article-page">
    <div class="container">
      <a href="../blog.html" class="blog-back">← Zurueck zum Content-Hub</a>

      <nav class="blog-breadcrumb" aria-label="Breadcrumb">
        <a href="../index.html">Startseite</a>
        <span aria-hidden="true">›</span>
        <a href="../blog.html">Blog</a>
        <span aria-hidden="true">›</span>
        {post['breadcrumb']}
      </nav>

      <header class="blog-header">
        <span class="section-tag">{post['kicker']}</span>
        <h1>{post['title_html']}</h1>
        <p class="blog-deck">{post['deck']}</p>
        <div class="blog-meta">
          <div><strong>Autor:</strong> Joshua Heller</div>
          <div><strong>Veroeffentlicht:</strong> April 2026</div>
          <div><strong>Lesezeit:</strong> ca. {post['read_time']}</div>
          <div><strong>Kategorie:</strong> {post['meta_category']}</div>
        </div>
      </header>

      <article class="blog-body">
{body}
      </article>
    </div>
  </main>

{FOOTER}
</body>
</html>
"""


def main():
    BLOG_DIR.mkdir(exist_ok=True)
    for post in POSTS:
        out = BLOG_DIR / post["output"]
        out.write_text(build_post(post), encoding="utf-8")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
