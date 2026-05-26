#!/usr/bin/env python3
"""Generate English blog posts from blog/*.html and add hreflang to German posts."""

import glob
import json
import os
import re
import time

import requests
from bs4 import BeautifulSoup, Comment

from generate_multilingual import (
    CACHE_FILE,
    HEADERS,
    normalize_html_output,
    should_translate,
    split_outer_whitespace,
    translate_text,
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BLOG_DIR = os.path.join(ROOT, 'blog')
EN_BLOG_DIR = os.path.join(ROOT, 'en', 'blog')

SKIP_TEXT_PARENTS = {'script', 'style', 'noscript'}
ATTRS_TO_TRANSLATE = {'title', 'alt', 'placeholder', 'aria-label'}
META_TRANSLATE_NAMES = {'description', 'keywords', 'twitter:title', 'twitter:description'}
META_TRANSLATE_PROPERTIES = {'og:title', 'og:description'}


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def update_seo_links(soup, filename, en_mode):
    de_url = f'https://clawgency.de/blog/{filename}'
    en_url = f'https://clawgency.de/en/blog/{filename}'

    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical is not None:
        canonical['href'] = en_url if en_mode else de_url

    for tag in soup.find_all('link', attrs={'rel': 'alternate'}):
        hreflang = (tag.get('hreflang') or '').lower()
        if hreflang in {'de', 'en', 'x-default'}:
            tag.decompose()

    if not soup.head:
        return

    for link in [
        soup.new_tag('link', rel='alternate', hreflang='de', href=de_url),
        soup.new_tag('link', rel='alternate', hreflang='en', href=en_url),
        soup.new_tag('link', rel='alternate', hreflang='x-default', href=de_url),
    ]:
        soup.head.append('\n')
        soup.head.append(link)


def ensure_language_switcher(soup, en_mode):
    src = '../../language-switcher.js' if en_mode else '../language-switcher.js'
    for script in soup.find_all('script'):
        existing = script.get('src')
        if isinstance(existing, str) and existing.endswith('language-switcher.js'):
            script['src'] = src
            return
    if soup.body:
        node = soup.new_tag('script')
        node['src'] = src
        soup.body.append('\n')
        soup.body.append(node)


def rewrite_urls_for_en_blog(soup):
    """Adjust relative paths for pages living in en/blog/."""
    replacements = {
        '../index.html': '../index.html',
        '../blog.html': '../blog.html',
        '../case-studies.html': '../case-studies.html',
        '../glossar.html': '../glossar.html',
        '../styles.min.css': '../../styles.min.css',
        '../blog-article.css': '../../blog-article.css',
        '../assets/': '../../assets/',
        '../openclaw-': '../openclaw-',
        '../case-study-': '../case-study-',
        '../impressum.html': '../impressum.html',
        '../datenschutz.html': '../datenschutz.html',
    }

    for tag in soup.find_all(True):
        for attr in ('href', 'src'):
            val = tag.get(attr)
            if not isinstance(val, str):
                continue
            v = val.strip()
            if not v or v.startswith(('mailto:', 'tel:', 'javascript:', 'data:', 'http', '#')):
                continue
            for old, new in replacements.items():
                if v.startswith(old):
                    tag[attr] = new + v[len(old):]
                    break


def ensure_hreflang_de(soup, filename):
    update_seo_links(soup, filename, en_mode=False)
    ensure_language_switcher(soup, en_mode=False)


def translate_nodes_and_attrs(soup, session, cache):
    nodes = list(soup.find_all(string=True))
    for node in nodes:
        if isinstance(node, Comment):
            continue
        parent = node.parent.name.lower() if node.parent and node.parent.name else ''
        if parent in SKIP_TEXT_PARENTS:
            continue
        original = str(node)
        if not should_translate(original):
            continue
        if 'Joshua Heller' in original:
            continue
        left, core, right = split_outer_whitespace(original)
        if not core:
            continue
        try:
            translated = translate_text(session, cache, core)
            node.replace_with(f'{left}{translated}{right}')
        except Exception:
            continue

    for tag in soup.find_all(True):
        for attr in ATTRS_TO_TRANSLATE:
            val = tag.get(attr)
            if isinstance(val, str) and should_translate(val):
                left, core, right = split_outer_whitespace(val)
                if core:
                    try:
                        tag[attr] = f'{left}{translate_text(session, cache, core)}{right}'
                    except Exception:
                        pass

    for meta in soup.find_all('meta'):
        content = meta.get('content')
        if not isinstance(content, str) or not should_translate(content):
            continue
        name = (meta.get('name') or '').strip().lower()
        prop = (meta.get('property') or '').strip().lower()
        if name in META_TRANSLATE_NAMES or prop in META_TRANSLATE_PROPERTIES:
            try:
                meta['content'] = translate_text(session, cache, content)
            except Exception:
                pass

    for script in soup.find_all('script', attrs={'type': 'application/ld+json'}):
        if not script.string:
            continue
        try:
            data = json.loads(script.string)
        except json.JSONDecodeError:
            continue
        text = json.dumps(data, ensure_ascii=False)
        if should_translate(text):
            try:
                translated = translate_text(session, cache, text)
                script.string = translated
            except Exception:
                pass


def fix_en_nav_labels(soup):
    replacements = {
        'Leistungen': 'Services',
        'Erstgespraech buchen': 'Book an initial consultation',
        'Menue oeffnen': 'Open menu',
        'Menue schliessen': 'Close menu',
        'Zurueck zum Content-Hub': 'Back to content hub',
        'Startseite': 'Home',
        'Autor:': 'Author:',
        'Veroeffentlicht:': 'Published:',
        'Lesezeit:': 'Reading time:',
        'Kategorie:': 'Category:',
    }
    html = str(soup)
    for old, new in replacements.items():
        html = html.replace(old, new)
    return BeautifulSoup(html, 'html.parser')


def process_blog_file(path, session, cache):
    filename = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    original = original.replace('Clawgency Redaktion', 'Joshua Heller')

    de_soup = BeautifulSoup(original, 'html.parser')
    if de_soup.html:
        de_soup.html['lang'] = 'de'
    ensure_hreflang_de(de_soup, filename)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(normalize_html_output(de_soup))

    en_soup = BeautifulSoup(original, 'html.parser')
    if en_soup.html:
        en_soup.html['lang'] = 'en'

    translate_nodes_and_attrs(en_soup, session, cache)
    rewrite_urls_for_en_blog(en_soup)
    en_soup = fix_en_nav_labels(en_soup)
    update_seo_links(en_soup, filename, en_mode=True)
    ensure_language_switcher(en_soup, en_mode=True)

    html = normalize_html_output(en_soup)
    html = html.replace('Clawgency Redaktion', 'Joshua Heller')
    html = html.replace('>Autor:<', '>Author:<')
    html = html.replace('>Veroeffentlicht:<', '>Published:<')
    html = html.replace('>Lesezeit:<', '>Reading time:<')
    html = html.replace('>Kategorie:<', '>Category:<')

    os.makedirs(EN_BLOG_DIR, exist_ok=True)
    out = os.path.join(EN_BLOG_DIR, filename)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    os.makedirs(EN_BLOG_DIR, exist_ok=True)
    cache = load_cache()
    files = sorted(glob.glob(os.path.join(BLOG_DIR, '*.html')))

    with requests.Session() as session:
        for i, path in enumerate(files, start=1):
            print(f'[{i}/{len(files)}] {os.path.basename(path)}', flush=True)
            process_blog_file(path, session, cache)
            save_cache(cache)
            time.sleep(0.1)

    print('Done', flush=True)


if __name__ == '__main__':
    main()
