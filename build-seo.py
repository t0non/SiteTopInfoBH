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
lawyer_item = '<li class="mega-menu-item mega-menu-item-type-custom mega-menu-item-object-custom" id="mega-menu-item-lawyers"><a class="mega-menu-link" href="/suporte-para-advogados/">Advogados</a></li>'
coverage_item = '<li class="mega-menu-item mega-menu-item-type-custom mega-menu-item-object-custom" id="mega-menu-item-coverage"><a class="mega-menu-link" href="/onde-atendemos/">Onde atendemos</a></li>'
if 'id="mega-menu-item-lawyers"' not in source:
    source = source.replace('<li class="mega-call-phone', lawyer_item + '<li class="mega-call-phone', 1)
if 'id="mega-menu-item-coverage"' not in source:
    source = source.replace('<li class="mega-call-phone', coverage_item + '<li class="mega-call-phone', 1)
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

onde_content = (ROOT / 'onde-atendemos-content.html').read_text(encoding='utf-8')
onde_content = re.sub(r'<a[^>]*data-contact="([^"]+)"[^>]*>', contact, onde_content)
onde = re.sub(r'<main\b.*?</main>', lambda _: onde_content, remote, count=1, flags=re.S)
(DIST / 'onde-atendemos').mkdir(exist_ok=True)
(DIST / 'onde-atendemos/index.html').write_text(onde, encoding='utf-8')

PAGES = [
    ('/', 'Top Info BH | Informática e suporte de TI em Belo Horizonte', 'Assistência de informática em Belo Horizonte: computadores, notebooks, suporte remoto de TI e instalação de câmeras. Fale com a Top Info BH.', None),
    ('/suporte-remoto/', 'Suporte Remoto e Help Desk em Belo Horizonte | Top Info BH', 'Suporte remoto de TI e Help Desk em Belo Horizonte para empresas e home office. Resolva lentidão, PJe, impressoras, rede e e-mails com início imediato. Fale conosco!', 'Suporte remoto de TI e Help Desk em Belo Horizonte'),
    ('/suporte-para-advogados/', 'Suporte para Advogados em BH: PJe e Certificado | Top Info BH', 'Suporte técnico para advogados em Belo Horizonte: PJe, PJeOffice, certificado digital, token e configuração do computador. Atendimento remoto com orçamento.', 'Suporte de TI para advogados em Belo Horizonte'),
    ('/onde-atendemos/', 'Onde Atendemos em Belo Horizonte e Região | Top Info BH', 'Confira as regiões e bairros atendidos em Belo Horizonte e Grande BH para suporte remoto de TI, computadores e instalação de câmeras de segurança e alarmes.', 'Atendimento de TI e Câmeras em Belo Horizonte e Região'),
    ('/limpeza-de-virus/', 'Remoção de Vírus e Malware em BH | Suporte Remoto Top Info BH', 'Livre-se de vírus, spywares, janelas de anúncios e pop-ups no seu computador sem sair de casa. Atendimento seguro por suporte remoto em Belo Horizonte.', 'Remoção de Vírus e Malwares em Belo Horizonte'),
    ('/conserto-impressora/', 'Configuração e Instalação de Impressora em BH | Top Info BH', 'Impressora offline, erro de spooler ou não conecta no Wi-Fi? Configuramos impressoras HP, Epson, Canon e Brother por acesso remoto em Belo Horizonte.', 'Suporte Técnico de Impressoras em Belo Horizonte'),
    ('/computador-lento/', 'Computador Lento e Travando em BH | Otimização Remota Top Info BH', 'Acelere seu computador e acabe com travamentos. Limpeza de inicialização, eliminação de arquivos temporários e otimização do Windows em BH.', 'Otimização e Aceleração de Computadores em BH'),
    ('/configuracao-email/', 'Suporte Outlook e Configuração de E-mails em BH | Top Info BH', 'Correção de erros no Outlook, falha de envio/recebimento, erro de senha e configuração de e-mails corporativos e pessoais por suporte remoto em BH.', 'Configuração de E-mails e Outlook em BH'),
    ('/liberar-espaco-disco/', 'Liberar Espaço no Disco C: em BH | Limpeza Segura Top Info BH', 'Disco C cheio ou memória insuficiente? Limpeza avançada de dados temporários e lixo do Windows sem perder seus arquivos em Belo Horizonte.', 'Limpeza de Disco e Memória em Belo Horizonte'),
    ('/instalacao-programas/', 'Instalação de Programas e Softwares em BH | Top Info BH', 'Instalação de Office, antivírus, leitores de PDF e softwares essenciais com segurança e garantia de download oficial em Belo Horizonte.', 'Instalação Segura de Programas em BH'),
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
        elif 'onde-atendemos' in path: crumbs.append({'@type':'ListItem','position':2,'name':'Onde atendemos','item':url})
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
    # Useful page links remain visible in the common footer.
    page = re.sub(r'<nav class="seo-footer-links".*?</nav>', '', page, flags=re.S)
    links = '<nav class="seo-footer-links" aria-label="Serviços de informática"><a href="/suporte-remoto/">Suporte remoto em Belo Horizonte</a><a href="/limpeza-de-virus/">Remoção de vírus</a><a href="/conserto-impressora/">Conserto de impressoras</a><a href="/computador-lento/">Computador lento</a><a href="/configuracao-email/">Configurar e-mail</a><a href="/liberar-espaco-disco/">Liberar espaço</a><a href="/instalacao-programas/">Instalar programas</a><a href="/suporte-para-advogados/">Suporte para advogados</a><a href="/onde-atendemos/">Onde atendemos</a><a href="/sitemap.xml">Mapa do site</a></nav>'
    page = page.replace('<div class="copy">', links + '<div class="copy">',1)
    if '/assets/seo-layout.css' not in page: page = page.replace('</head>','<link rel="stylesheet" href="/assets/seo-layout.css"></head>',1)
    top_marketing_credit = '<a href="https://topmarketingbh.com.br/" target="_blank" rel="noopener noreferrer" class="text-center topmarketing-credit" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;color:#fff;text-decoration:none;font-weight:600;"><img src="/assets/topmarketinglogo.png" alt="Top Marketing BH" style="height:22px;width:auto;vertical-align:middle;border-radius:3px;"> Desenvolvido por Top Marketing BH</a>'
    page = re.sub(r'<a href="https://helpecommerce\.com\.br/".*?</a>', top_marketing_credit, page)
    file.write_text(page,encoding='utf-8')

urls = '\n'.join('  <url><loc>'+escape(ORIGIN+path)+'</loc></url>' for path,*_ in PAGES)
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'\n</urlset>\n',encoding='utf-8')
(DIST/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+ORIGIN+'/sitemap.xml\n',encoding='utf-8')
print(f'SEO generated for {len(PAGES)} pages; production origin: '+ORIGIN)
subprocess.run([sys.executable, str(ROOT / 'build-languages.py')], check=True)
