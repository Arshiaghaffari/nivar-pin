#!/usr/bin/env python3
"""Mirror public, rendered site text; no private source or form submissions."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
import re
import xml.etree.ElementTree as ET

BASE = 'https://abrnivar.ir/'
LIMIT = 2_000_000

class MainText(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
    SKIP = {'script', 'style', 'template', 'svg', 'form', 'nav', 'button', 'noscript'}
    BLOCK = {'p', 'div', 'section', 'article', 'ul', 'ol', 'dl', 'dt', 'dd', 'details', 'summary', 'tr', 'blockquote', 'figure', 'figcaption'}

    def __init__(self, url):
        super().__init__(convert_charrefs=True)
        self.url, self.stack, self.out = url, [], []
        self.found_main = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        parent_skip = self.stack[-1][1] if self.stack else False
        skip = parent_skip or tag in self.SKIP or 'hidden' in a or a.get('aria-hidden') == 'true'
        inside = tag == 'main' or any(t == 'main' for t, _, _ in self.stack)
        self.found_main |= tag == 'main'
        href = None
        if inside and not skip:
            if re.fullmatch(r'h[1-6]', tag):
                self.out.append('\n\n' + '#' * min(int(tag[1]) + 1, 6) + ' ')
            elif tag in self.BLOCK:
                self.out.append('\n\n')
            elif tag == 'li':
                self.out.append('\n- ')
            elif tag == 'br':
                self.out.append('\n')
            elif tag in {'td', 'th'}:
                self.out.append(' | ')
            elif tag == 'a':
                candidate = urljoin(self.url, a.get('href', ''))
                if urlsplit(candidate).scheme in {'https', 'http', 'mailto'}:
                    href = candidate.replace(' ', '%20').replace(')', '%29')
                    self.out.append('[')
        if tag not in self.VOID:
            self.stack.append((tag, skip, href))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for pos in range(len(self.stack) - 1, -1, -1):
            if self.stack[pos][0] == tag:
                inside = any(t == 'main' for t, _, _ in self.stack)
                _, skip, href = self.stack[pos]
                del self.stack[pos:]
                if inside and not skip:
                    if href:
                        self.out.append('](' + href + ')')
                    if tag in self.BLOCK or re.fullmatch(r'h[1-6]', tag):
                        self.out.append('\n\n')
                break

    def handle_data(self, data):
        if self.stack and not self.stack[-1][1] and any(t == 'main' for t, _, _ in self.stack):
            # Collapse source formatting whitespace, preserve meaningful text.
            self.out.append(escape(re.sub(r'\s+', ' ', data), quote=False).replace('[', '\\[').replace(']', '\\]'))

def extract(html, url):
    parser = MainText(url)
    parser.feed(html)
    text = ''.join(parser.out)
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n[ \t]+', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    if not parser.found_main or len(text) < 100:
        raise ValueError('Missing/short main content: ' + url)
    return text + '\n'

def public_url(url):
    parsed = urlsplit(url)
    return (parsed.scheme == 'https' and parsed.netloc == 'abrnivar.ir'
            and not parsed.query and not parsed.fragment
            and (parsed.path.endswith('/') or parsed.path.endswith('.html')))

def fetch(url, kind):
    request = Request(url, headers={'User-Agent': 'Nivar-Public-Docs/1.0', 'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=30) as response:
        final = urlsplit(response.geturl())
        if final.scheme != 'https' or final.netloc != 'abrnivar.ir':
            raise ValueError('Unexpected redirect')
        if kind not in response.headers.get_content_type():
            raise ValueError('Unexpected content type: ' + url)
        data = response.read(LIMIT + 1)
        if len(data) > LIMIT:
            raise ValueError('Response too large')
        return data.decode('utf-8')

def documents(pages):
    texts = {url: extract(html, url) for url, html in sorted(pages.items())}
    if BASE not in texts:
        raise ValueError('Homepage missing')
    files = {}
    links = []
    for url, text in texts.items():
        if url == BASE:
            continue
        path = urlsplit(url).path.strip('/')
        name = re.sub(r'[^a-zA-Z0-9_-]', '-', path.removesuffix('.html')) + '.md'
        if name in files:
            raise ValueError('Duplicate output name')
        files[name] = '# نسخهٔ متنی صفحه\n\nمنبع: ' + url + '\n\n' + text
        links.append('- [' + path + '](pages/' + name + ')')
    header = ('# نیوارپین — معرفی عمومی ویژهٔ FortiGate\n\n'
              'منبع اصلی: https://abrnivar.ir/ — نویان ابر نیوار، ایران\n\n'
              'این نسخه به‌صورت خودکار از متن عمومی صفحات منتشرشدهٔ سایت ساخته می‌شود. '
              'فایل README و پوشهٔ pages را دستی ویرایش نکنید؛ تغییرات را در سایت اصلی منتشر کنید.\n\n'
              '## صفحات سایت\n\n' + '\n'.join(links) + '\n\n'
              '## محتوای صفحهٔ اصلی\n\n')
    result = {'README.md': header + texts[BASE]}
    result.update({'pages/' + name: value for name, value in files.items()})
    return result

def main():
    xml = fetch(BASE + 'sitemap.xml', 'xml')
    urls = sorted({node.text.strip() for node in ET.fromstring(xml).iter()
                   if node.tag.split('}')[-1] == 'loc' and node.text})
    if not urls or len(urls) > 30 or not all(public_url(u) for u in urls):
        raise ValueError('Unexpected sitemap URLs')
    pages = {u: fetch(u, 'html') for u in sorted(set(urls + [BASE]))}
    result = documents(pages)
    # Avoid committing a partial deployment. Fail without altering files.
    if extract(fetch(BASE, 'html'), BASE) != extract(pages[BASE], BASE):
        raise ValueError('Site changed during sync; retry next run')
    for name, text in result.items():
        path = Path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
    for path in Path('pages').glob('*.md'):
        if path.as_posix() not in result:
            path.unlink()
    print('Synced', len(result), 'public pages')

if __name__ == '__main__':
    main()
