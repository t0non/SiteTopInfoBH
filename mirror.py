import concurrent.futures, hashlib, html, json, re, subprocess
from pathlib import Path
from urllib.parse import urljoin, urlsplit, quote

ROOT = Path(__file__).parent
OUT = ROOT / 'dist'
ASSETS = OUT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
BASE = 'https://topinfobh.com.br/'
source = (ROOT / 'original.html').read_text(encoding='utf-8')
mapping, contents, failures = {}, {}, {}

def urls(text, base, css=False):
    found = re.findall(r'''(?:src|href|data-src|data-lazy-src|poster)=["']([^"']+)["']''', text)
    found += re.findall(r'''https?://[^\s<>"'\\)]+''', text)
    found += re.findall(r'''url\(\s*["']?([^\s)'";]+)''', text)
    for raw in found:
        raw = html.unescape(raw).rstrip(',;')
        u = urljoin(base, raw)
        p = urlsplit(u)
        if p.scheme not in ('http','https'): continue
        ext = Path(p.path).suffix.lower()
        if ext in ('.css','.js','.png','.jpg','.jpeg','.gif','.svg','.webp','.woff','.woff2','.ttf','.eot','.ico') or p.netloc in ('fonts.googleapis.com','lh3.googleusercontent.com'):
            if 'googletagmanager' not in u and 'cdn-reach' not in u:
                yield u.split('#')[0]

def download(u):
    p = urlsplit(u)
    ext = Path(p.path).suffix.lower()
    if p.netloc == 'fonts.googleapis.com': ext = '.css'
    if p.netloc == 'lh3.googleusercontent.com': ext = '.jpg'
    name = hashlib.sha256(u.encode()).hexdigest()[:16] + ext
    target = ASSETS / name
    encoded = quote(u, safe=':/?=&%+@,;~!$*()-')
    result = subprocess.run(['curl.exe','-f','-sS','-L','--max-time','45','--retry','1',encoded,'-o',str(target)],capture_output=True)
    if result.returncode:
        return u, None, result.stderr.decode(errors='replace')
    return u, name, None

pending = set(urls(source, BASE))
seen = set()
for depth in range(5):
    batch = pending - seen
    if not batch: break
    seen.update(batch)
    print(f'Pass {depth + 1}: downloading {len(batch)} files', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for u, name, error in pool.map(download, sorted(batch)):
            if error:
                failures[u] = error
                continue
            mapping[u] = '/assets/' + name
            if name.endswith(('.css','.js')):
                contents[u] = (ASSETS / name).read_text(encoding='utf-8', errors='replace')
                if name.endswith('.css'):
                    pending.update(urls(contents[u], u, True))

def rewrite(text, base):
    # Replace longest URLs first, including HTML-escaped and protocol-relative forms.
    for u in sorted(mapping, key=len, reverse=True):
        local = mapping[u]
        for variant in (u, u.replace('&','&#038;'), u.replace('&','&amp;'), u.replace('https:','',1)):
            text = text.replace(variant, local)
    def css_url(m):
        raw = m.group(2)
        absolute = urljoin(base, html.unescape(raw)).split('#')[0]
        return 'url(' + m.group(1) + mapping.get(absolute, raw) + m.group(1) + ')'
    return re.sub(r'''url\(\s*(["']?)([^)'"\s]+)\1\s*\)''',css_url,text)

for u, data in contents.items():
    (OUT / mapping[u].lstrip('/')).write_text(rewrite(data, u), encoding='utf-8')

page = rewrite(source, BASE)
page = page.replace('href="https://topinfobh.com.br/"', 'href="/"')
page = re.sub(r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->', '', page, flags=re.S)
page = re.sub(r'<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->', '', page, flags=re.S)
page = re.sub(r'<script[^>]+src=["\'][^"\']*cdn-reach[^"\']*["\'][^>]*>.*?</script>', '', page, flags=re.S)
page = page.replace('</head>', '<meta name="robots" content="noindex,nofollow">\n</head>')
(OUT / 'index.html').write_text(page, encoding='utf-8')
(ROOT / 'mirror-report.json').write_text(json.dumps({'source':BASE,'downloaded':len(mapping),'assets':mapping,'failures':failures}, ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'downloaded':len(mapping),'failures':failures},ensure_ascii=True),flush=True)
