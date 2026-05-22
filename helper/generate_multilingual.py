#!/usr/bin/env python3
import glob
import json
import os
import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Comment

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EN_DIR = os.path.join(ROOT, 'en')
CACHE_FILE = os.path.join(ROOT, 'helper', '.translation_cache_en.json')

SKIP_TEXT_PARENTS = {'script', 'style', 'noscript'}
ATTRS_TO_TRANSLATE = {'title', 'alt', 'placeholder', 'aria-label'}
URL_ATTRS = {'href', 'src', 'poster', 'data-src'}

META_TRANSLATE_NAMES = {'description', 'keywords', 'twitter:title', 'twitter:description'}
META_TRANSLATE_PROPERTIES = {'og:title', 'og:description'}

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; ClawgencyI18nBot/1.0)'}


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def should_translate(text):
    return bool(text and text.strip() and re.search(r'[A-Za-zÄÖÜäöüß]', text))


def split_outer_whitespace(s):
    left = re.match(r'^\s*', s).group(0)
    right = re.search(r'\s*$', s).group(0)
    core = s[len(left):len(s) - len(right) if right else len(s)]
    return left, core, right


def call_translate(session, text):
    r = session.get(
        'https://translate.googleapis.com/translate_a/single',
        params={
            'client': 'gtx',
            'sl': 'de',
            'tl': 'en',
            'dt': 't',
            'q': text,
        },
        timeout=20,
        headers=HEADERS,
    )
    r.raise_for_status()
    data = r.json()
    return ''.join(part[0] for part in data[0])


def translate_text(session, cache, text):
    if text in cache:
        return cache[text]

    if len(text) > 3500:
        parts = []
        start = 0
        while start < len(text):
            end = min(len(text), start + 2500)
            piece = text[start:end]
            if end < len(text):
                split_at = max(piece.rfind('\n'), piece.rfind('. '), piece.rfind('; '))
                if split_at > 200:
                    end = start + split_at + 1
                    piece = text[start:end]
            piece = piece.strip()
            if piece:
                parts.append(translate_text(session, cache, piece))
            start = end
        out = ' '.join(parts)
    else:
        out = call_translate(session, text)

    cache[text] = out
    return out


def normalize_html_output(soup):
    rendered = str(soup)
    rendered = re.sub(r'^\s*<!DOCTYPE[^>]*>\s*', '', rendered, flags=re.IGNORECASE)
    rendered = re.sub(r'^\s*html\s*(?:\r?\n)+(?=<html)', '', rendered, flags=re.IGNORECASE)
    return '<!DOCTYPE html>\n' + rendered


def to_english_url(url):
    if not url:
        return url
    parsed = urlparse(url)
    if parsed.scheme or url.startswith('//') or url.startswith('#'):
        return url
    path_only = re.split(r'[?#]', url, maxsplit=1)[0]

    if url.startswith('/'):
        if url == '/':
            return '/en/'
        if url.startswith('/en/'):
            return url
        if path_only.endswith('.html'):
            return '/en' + url
        return url
    if path_only.endswith('.html'):
        return url
    if url.startswith('../'):
        return url
    return '../' + url


def rewrite_urls_for_en(soup):
    for tag in soup.find_all(True):
        for attr in URL_ATTRS:
            val = tag.get(attr)
            if not isinstance(val, str):
                continue
            v = val.strip()
            if not v or v.startswith(('mailto:', 'tel:', 'javascript:', 'data:')):
                continue
            tag[attr] = to_english_url(v)


def ensure_language_switcher(soup, en_mode):
    src = '../language-switcher.js' if en_mode else 'language-switcher.js'
    for script in soup.find_all('script'):
        existing = script.get('src')
        if isinstance(existing, str) and existing.endswith('language-switcher.js'):
            script['src'] = src
            return

    node = soup.new_tag('script')
    node['src'] = src
    if soup.body:
        soup.body.append('\n')
        soup.body.append(node)


def fix_inline_nav_script_for_en(soup):
    for script in soup.find_all('script'):
        if script.get('src'):
            continue
        content = script.string
        if not isinstance(content, str):
            continue
        if 'mobile-open' in content and 'Menue schliessen' in content:
            script.string = content.replace('Menue schliessen', 'Close menu').replace('Menue oeffnen', 'Open menu')


def update_seo_links(soup, filename, en_mode):
    rel_path = '' if filename == 'index.html' else filename
    de_url = 'https://clawgency.de/' + rel_path
    en_url = 'https://clawgency.de/en/' + ('index.html' if filename == 'index.html' else filename)

    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical is not None:
        canonical['href'] = en_url if en_mode else de_url

    for tag in soup.find_all('link', attrs={'rel': 'alternate'}):
        hreflang = (tag.get('hreflang') or '').lower()
        if hreflang in {'de', 'en', 'x-default'}:
            tag.decompose()

    if not soup.head:
        return

    links = [
        soup.new_tag('link', rel='alternate', hreflang='de', href=de_url),
        soup.new_tag('link', rel='alternate', hreflang='en', href=en_url),
        soup.new_tag('link', rel='alternate', hreflang='x-default', href=de_url),
    ]
    for link in links:
        soup.head.append('\n')
        soup.head.append(link)


def force_index_to_main_script(soup, en_mode):
    for script in soup.find_all('script'):
        src = script.get('src')
        if src == 'script.min.js':
            script['src'] = 'script.js'
        if en_mode and src == '../script.min.js':
            script['src'] = '../script.js'


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


def process_file(path, session, cache):
    filename = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    # Update German page: keep content, add switcher + hreflang + lang attr.
    de_soup = BeautifulSoup(original, 'html.parser')
    if de_soup.html:
        de_soup.html['lang'] = 'de'
    ensure_language_switcher(de_soup, en_mode=False)
    update_seo_links(de_soup, filename, en_mode=False)
    force_index_to_main_script(de_soup, en_mode=False)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(normalize_html_output(de_soup))

    # Generate English page.
    en_soup = BeautifulSoup(original, 'html.parser')
    if en_soup.html:
        en_soup.html['lang'] = 'en'

    translate_nodes_and_attrs(en_soup, session, cache)
    rewrite_urls_for_en(en_soup)
    ensure_language_switcher(en_soup, en_mode=True)
    update_seo_links(en_soup, filename, en_mode=True)
    force_index_to_main_script(en_soup, en_mode=True)
    fix_inline_nav_script_for_en(en_soup)

    out = os.path.join(EN_DIR, filename)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(normalize_html_output(en_soup))


def main():
    os.makedirs(EN_DIR, exist_ok=True)
    cache = load_cache()
    html_files = sorted(glob.glob(os.path.join(ROOT, '*.html')))

    with requests.Session() as session:
        for i, path in enumerate(html_files, start=1):
            print(f'[{i}/{len(html_files)}] {os.path.basename(path)}', flush=True)
            process_file(path, session, cache)
            save_cache(cache)
            time.sleep(0.05)

    print('Done', flush=True)


if __name__ == '__main__':
    main()
