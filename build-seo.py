"""Generate production-ready pages and discovery files for topinfobh.com.br."""
from pathlib import Path
from urllib.parse import quote
import html, json, re, subprocess, sys
from xml.sax.saxutils import escape

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
ORIGIN = 'https://topinfobh.com.br'

home = DIST / 'index.html'
source = home.read_text(encoding='utf-8')
if '<h1' not in source:
    source = source.replace('<p>Instalação de Câmeras, Alarmes.</p><p>Manutenção de Notebook e Computadores.</p>', '<h1 style="font:inherit;color:inherit;line-height:inherit;margin:0"><span style="display:block;margin-bottom:20px">Instalação de Câmeras, Alarmes.</span><span style="display:block;margin-bottom:20px">Manutenção de Notebook e Computadores.</span></h1>', 1)
lawyer_item = '<li class="mega-menu-item mega-menu-item-type-custom mega-menu-item-object-custom" id="mega-menu-item-lawyers"><a class="mega-menu-link" href="/suporte-para-advogados/">Suporte</a></li>'
if 'id="mega-menu-item-lawyers"' not in source:
    source = source.replace('<li class="mega-call-phone', lawyer_item + '<li class="mega-call-phone', 1)
source = source.replace('href="#cameras">Instalação de Câmeras</a>', 'href="#cameras">Câmeras</a>').replace('href="#manutencao">Manutenção Computadores</a>', 'href="#manutencao">Computadores</a>')
source = source.replace('<a class="mega-menu-link" href="#depoimentos">Depoimentos</a>', '<a class="mega-menu-link" href="#depoimentos">Avaliações</a>')
home.write_text(source, encoding='utf-8')
subprocess.run([sys.executable, str(ROOT / 'build-remote.py')], check=True)

remote = (DIST / 'suporte-remoto/index.html').read_text(encoding='utf-8')
lawyer_content = (ROOT / 'lawyers-content.html').read_text(encoding='utf-8')
def contact(m):
    return m.group(0).replace('href="#atendimento"', 'href="https://api.whatsapp.com/send?phone=5531991133939&amp;text=' + quote(html.unescape(m.group(1))) + '" target="_blank" rel="noopener noreferrer"')
lawyer_content = re.sub(r'<a[^>]*data-contact="([^"]+)"[^>]*>', contact, lawyer_content)
lawyer = re.sub(r'<main\b.*?</main>', lambda _: lawyer_content, remote, count=1, flags=re.S)
(DIST / 'suporte-para-advogados').mkdir(exist_ok=True)
(DIST / 'suporte-para-advogados/index.html').write_text(lawyer, encoding='utf-8')

PAGES = [
    ('/', 'Top Info BH | Informática e suporte de TI em Belo Horizonte', 'Assistência de informática em Belo Horizonte: computadores, notebooks, suporte remoto de TI e instalação de câmeras. Fale com a Top Info BH.', None),
    ('/suporte-remoto/', 'Suporte Remoto em Belo Horizonte | Top Info BH', 'Suporte remoto de TI em Belo Horizonte para computador lento, falta de espaço, impressoras, e-mail e programas. Peça seu orçamento à Top Info BH.', 'Suporte remoto de TI em Belo Horizonte'),
    ('/suporte-para-advogados/', 'Suporte para Advogados em BH: PJe e Certificado | Top Info BH', 'Suporte técnico para advogados em Belo Horizonte: PJe, PJeOffice, certificado digital, token e configuração do computador. Atendimento remoto com orçamento.', 'Suporte de TI para advogados em Belo Horizonte'),
]

def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', s))).strip()

business = {'@type':'Organization','@id':ORIGIN+'/#organization','name':'Top Info BH','url':ORIGIN+'/',
    'logo':ORIGIN+'/assets/75c233edaf0044c6.png','telephone':'+55-31-99113-3939',
    'areaServed':{'@type':'City','name':'Belo Horizonte','containedInPlace':{'@type':'State','name':'Minas Gerais'}},
    'sameAs':['https://www.instagram.com/topinfobh/','https://www.facebook.com/topinfobh/']}

for path, title, desc, service_name in PAGES:
    file = DIST / path.strip('/') / 'index.html' if path != '/' else home
    page = file.read_text(encoding='utf-8')
    # Replace all conflicting metadata, including the imported WordPress graph.
    page = re.sub(r'<title>.*?</title>', '', page, flags=re.S|re.I)
    page = re.sub(r'<meta\b[^>]*(?:name|property)=["\'](?:description|robots|googlebot|twitter:[^"\']+|og:[^"\']+|article:[^"\']+)["\'][^>]*>', '', page, flags=re.I)
    page = re.sub(r'<link\b[^>]*rel=["\'](?:canonical|shortlink)["\'][^>]*>', '', page, flags=re.I)
    page = re.sub(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>', '', page, flags=re.S|re.I)
    url = ORIGIN + path
    graph = [business, {'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN+'/', 'name':'Top Info BH','inLanguage':'pt-BR','publisher':{'@id':business['@id']}},
        {'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':'pt-BR','isPartOf':{'@id':ORIGIN+'/#website'},'about':{'@id':business['@id']}}]
    if service_name:
        graph.append({'@type':'Service','@id':url+'#service','name':service_name,'serviceType':service_name,'url':url,'provider':{'@id':business['@id']},'areaServed':business['areaServed'],'availableChannel':{'@type':'ServiceChannel','serviceUrl':url,'servicePhone':{'@type':'ContactPoint','telephone':business['telephone'],'contactType':'suporte técnico','availableLanguage':'Portuguese'}}})
        crumbs = [{'@type':'ListItem','position':1,'name':'Início','item':ORIGIN+'/'}]
        if 'advogados' in path: crumbs.append({'@type':'ListItem','position':2,'name':'Suporte remoto','item':ORIGIN+'/suporte-remoto/'})
        crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':service_name,'item':url})
        graph.append({'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':crumbs})
        questions = []
        for q, a in re.findall(r'<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>',page,re.S):
            questions.append({'@type':'Question','name':plain(q),'acceptedAnswer':{'@type':'Answer','text':plain(a)}})
        if questions: graph.append({'@type':'FAQPage','@id':url+'#faq','mainEntity':questions})
    metadata = f'''<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc,quote=True)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:locale" content="pt_BR"><meta property="og:type" content="website">
<meta property="og:site_name" content="Top Info BH"><meta property="og:title" content="{html.escape(title,quote=True)}">
<meta property="og:description" content="{html.escape(desc,quote=True)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{ORIGIN}/assets/1cb48ea26eeb4630.png"><meta property="og:image:alt" content="Top Info BH — informática em Belo Horizonte">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{html.escape(title,quote=True)}"><meta name="twitter:description" content="{html.escape(desc,quote=True)}">
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')}</script>
'''
    page = page.replace('</head>', metadata + '</head>', 1)
    if path == '/suporte-remoto/' and 'class="breadcrumbs' not in page:
        page = page.replace('<main id="content" class="remote">','<main id="content" class="remote"><nav class="breadcrumbs remote-container" aria-label="Você está em"><a href="/">Início</a><span aria-hidden="true"> / </span><span>Suporte remoto em Belo Horizonte</span></nav>',1)
    # Useful page links remain visible in the common footer.
    page = re.sub(r'<nav class="seo-footer-links".*?</nav>', '', page, flags=re.S)
    links = '<nav class="seo-footer-links" aria-label="Serviços de informática"><a href="/suporte-remoto/">Suporte remoto em Belo Horizonte</a><a href="/suporte-para-advogados/">Suporte para advogados e PJe</a><a href="/sitemap.xml">Mapa do site</a></nav>'
    page = page.replace('<div class="copy">', links + '<div class="copy">',1)
    if '/assets/seo-layout.css' not in page: page = page.replace('</head>','<link rel="stylesheet" href="/assets/seo-layout.css"></head>',1)
    file.write_text(page,encoding='utf-8')

urls = '\n'.join('  <url><loc>'+escape(ORIGIN+path)+'</loc></url>' for path,*_ in PAGES)
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'\n</urlset>\n',encoding='utf-8')
(DIST/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+ORIGIN+'/sitemap.xml\n',encoding='utf-8')
print('SEO generated for 3 pages; production origin: '+ORIGIN)
