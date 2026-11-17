"""Build static translations of all three pages, with reciprocal hreflang links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, parse_qs, urlencode
from xml.sax.saxutils import escape
import html, json, re

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
ORIGIN = 'https://topinfobh.com.br'
PATHS = [
    '/',
    '/suporte-remoto/',
    '/suporte-para-advogados/',
    '/onde-atendemos/',
    '/limpeza-de-virus/',
    '/conserto-impressora/',
    '/computador-lento/',
    '/configuracao-email/',
    '/liberar-espaco-disco/',
    '/instalacao-programas/',
    '/instalacao-pacote-office/'
]
LANGUAGES = {
    'pt-BR': ('', 'br', 'Português', 'pt_BR'),
    'en': ('/en', 'us', 'English', 'en_US'),
    'es': ('/es', 'es', 'Español', 'es_ES'),
    'ar': ('/ar', 'sa', 'العربية', 'ar_SA'),
}
sources = json.loads((ROOT/'translation-source.json').read_text(encoding='utf-8'))
translations = {lang:{} for lang in ('en','es','ar')}
for line in (ROOT/'translations.tsv').read_text(encoding='utf-8').splitlines():
    if not line or line.startswith('#'): continue
    row = line.split('|')
    assert len(row)==4, row
    for i,lang in enumerate(translations): translations[lang][sources[int(row[0])]]=row[i+1]
for key, row in json.loads((ROOT/'translations-extra.json').read_text(encoding='utf-8')).items():
    for i,lang in enumerate(translations): translations[lang][key]=row[i]

def normalize(text): return re.sub(r'\s+', ' ', text).strip()
def localized(path, lang): return LANGUAGES[lang][0] + path
def strip_lang(path): return re.sub(r'^/(?:en|es|ar)(?=/|$)', '', path) or '/'
def page_file(path): return DIST/path.strip('/')/'index.html' if path!='/' else DIST/'index.html'
def translate(text, lang):
    if lang=='pt-BR': return text
    core=normalize(text)
    value=translations[lang].get(core)
    if value is None:
        # Composite headings and schema text use the same translations as visible text.
        value=core
        for key in sorted(translations[lang], key=len, reverse=True):
            if key in value: value=value.replace(key,translations[lang][key])
    return (text[:len(text)-len(text.lstrip())] + value + text[len(text.rstrip()):]) if text.strip() else text

def rewrite_url(url,lang):
    if url.startswith(('#','?')): return url
    parts=urlsplit(url)
    if parts.netloc and parts.netloc!='topinfobh.com.br': return url
    path=strip_lang(parts.path)
    if path not in PATHS: return url
    newpath=localized(path,lang)
    prefix=ORIGIN if parts.netloc else ''
    return prefix+newpath+('?' + parts.query if parts.query else '')+('#'+parts.fragment if parts.fragment else '')

def schema(value,lang):
    if isinstance(value,list):return [schema(x,lang) for x in value]
    if isinstance(value,dict):
        return {k: (lang if k=='inLanguage' else schema(v,lang)) for k,v in value.items()}
    if isinstance(value,str):
        if value.startswith(ORIGIN):return rewrite_url(value,lang)
        if value.startswith('http') or value in ('Portuguese','Minas Gerais','Belo Horizonte'):return value
        return translate(value,lang)
    return value

class Localize(HTMLParser):
    def __init__(self,lang,path):
        super().__init__(convert_charrefs=True)
        self.lang=lang;self.path=path;self.output=[];self.raw=None;self.jsonld=False
    def handle_starttag(self,tag,attrs):
        original=self.get_starttag_text()
        values=dict(attrs)
        if tag in ('script','style'):
            self.raw=tag;self.jsonld=values.get('type')=='application/ld+json'
        new=[]
        for key,val in attrs:
            if val is None:new.append((key,val));continue
            if tag=='html' and key=='lang':val=self.lang
            elif key=='dir' and tag=='html':continue
            elif key in ('href','src'):
                if key=='href':val='#content' if val.endswith('#content') else rewrite_url(val,self.lang)
                if self.lang!='pt-BR' and 'api.whatsapp.com/send' in val:
                    msgs = {'en':'Hello! I need IT support.','es':'¡Hola! Necesito soporte técnico de TI.','ar':'مرحباً! أحتاج إلى دعم تقني.'}
                    path_idx = PATHS.index(self.path) if self.path in PATHS else 0
                    if path_idx < 4:
                        message = {
                            'en': ['Hello! I would like a quote for your services.', 'Hello! I need remote IT support.', 'Hello! I need IT support for my law firm, PJe or a digital certificate.', 'Hello! I would like to check service availability for my neighborhood.'],
                            'es': ['¡Hola! Quisiera un presupuesto para sus servicios.', '¡Hola! Necesito soporte remoto de TI.', '¡Hola! Necesito soporte para mi despacho, el PJe o un certificado digital.', '¡Hola! Quisiera consultar la disponibilidad de atención para mi barrio.'],
                            'ar': ['مرحباً! أود طلب عرض سعر لخدماتكم.', 'مرحباً! أحتاج إلى دعم تقني عن بُعد.', 'مرحباً! أحتاج إلى دعم لمكتب المحاماة أو PJe أو شهادة رقمية.', 'مرحباً! أود الاستفسار عن توفر الخدمة في حيي.']
                        }[self.lang][path_idx]
                    else:
                        message = msgs[self.lang]
                    val='https://api.whatsapp.com/send?'+urlencode({'phone':'5531991133939','text':message})
            elif key in ('alt','title','aria-label','data-open-text','data-collapse-text','data-close-locale','data-reply-by-locale','data-only-rating-locale'):val=translate(val,self.lang)
            elif key=='content' and tag=='meta':
                if values.get('property')=='og:locale':val=LANGUAGES[self.lang][3]
                elif values.get('property')=='og:url':val=ORIGIN+localized(self.path,self.lang)
                elif values.get('name') in ('description','twitter:title','twitter:description') or values.get('property') in ('og:title','og:description','og:image:alt'):val=translate(val,self.lang)
            elif key=='data-language':val='pt' if self.lang=='pt-BR' else self.lang
            elif key=='data-time-locale' and self.lang!='pt-BR':
                val={'en':'%d %s ago|today|day|days|week|weeks|month|months|year|years','es':'hace %d %s|hoy|día|días|semana|semanas|mes|meses|año|años','ar':'منذ %d %s|اليوم|يوم|أيام|أسبوع|أسابيع|شهر|أشهر|سنة|سنوات'}[self.lang]
            new.append((key,val))
        if tag=='html':new.append(('dir','rtl' if self.lang=='ar' else 'ltr'))
        if new==attrs:
            self.output.append(original)
        else:
            self.output.append('<'+tag+''.join(' '+k+('="'+html.escape(v,quote=True)+'"' if v is not None else '') for k,v in new)+'>')
    def handle_startendtag(self,t,a):self.handle_starttag(t,a)
    def handle_endtag(self,t):
        self.output.append('</'+t+'>')
        if t==self.raw:self.raw=None;self.jsonld=False
    def handle_data(self,data):
        if self.jsonld:self.output.append(json.dumps(schema(json.loads(data),self.lang),ensure_ascii=False).replace('</','<\\/'))
        elif self.raw:self.output.append(data)
        else:self.output.append(html.escape(translate(html.unescape(data),self.lang),quote=False))
    def handle_entityref(self,name):self.output.append('&'+name+';')
    def handle_charref(self,name):self.output.append('&#'+name+';')
    def handle_comment(self,data):self.output.append('<!--'+data+'-->')
    def handle_decl(self,decl):self.output.append('<!'+decl+'>')

def selector(lang,path):
    _,flag,name,_=LANGUAGES[lang]
    caption={'pt-BR':'Escolher idioma','en':'Choose language','es':'Elegir idioma','ar':'اختر اللغة'}[lang]
    options=[]
    for code,(_,image,label,_) in LANGUAGES.items():
        current=' aria-current="true"' if code==lang else ''
        options.append(f'<li><a href="{localized(path,code)}" lang="{code}" hreflang="{code}" aria-label="{label}"{current}><img src="/assets/flags/{image}.png" alt="" width="22" height="15"><span dir="auto">{label}</span></a></li>')
    return f'<li class="mega-menu-item mega-menu-item-type-custom mega-lang-nav-item" id="mega-menu-item-lang"><details class="language-switcher"><summary class="mega-lang-summary" aria-label="{caption}"><img src="/assets/flags/{flag}.png" alt="{name}" width="22" height="15"><i class="fas fa-chevron-down language-chevron" aria-hidden="true"></i></summary><ul class="language-dropdown" aria-label="{caption}">{"".join(options)}</ul></details></li>'

pages={path:page_file(path).read_text(encoding='utf-8') for path in PATHS}
for path,page in pages.items():
    # Idempotent: always translate Portuguese originals, never a previously translated page.
    page=re.sub(r'<div class="language-bar">.*?</details></div></div>','',page,flags=re.S)
    page=re.sub(r'<li[^>]*id="mega-menu-item-lang"[^>]*>.*?</li>','',page,flags=re.S)
    # Remove any leftover leaked dropdown chunks if present
    page=re.sub(r'(?:<li><a href="[^"]*" lang="(?:en|es|ar)"[^>]*>.*?</li></ul></details></li>)+','',page,flags=re.S)
    page=re.sub(r'<link[^>]+(?:hreflang=|href="/assets/languages.css(?:\?v=[^"]*)?")[^>]*>','',page)
    for lang in LANGUAGES:
        parser=Localize(lang,path);parser.feed(page);parser.close()
        result=''.join(parser.output)
        alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{ORIGIN}{localized(path,code)}">' for code in LANGUAGES)
        alternates+=f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{path}">'
        result=result.replace('</head>',alternates+'<link rel="stylesheet" href="/assets/languages.css?v=12"></head>',1)
        result=re.sub(r'(<li[^>]*id="mega-menu-item-97336"[^>]*>.*?</li>)', r'\1' + selector(lang,path), result, flags=re.S)
        target=page_file(localized(path,lang));target.parent.mkdir(parents=True,exist_ok=True);target.write_text(result,encoding='utf-8')

entries=[]
for path in PATHS:
    for lang in LANGUAGES:
        alternates=''.join(f'<xhtml:link rel="alternate" hreflang="{code}" href="{escape(ORIGIN+localized(path,code))}"/>' for code in LANGUAGES)
        alternates+=f'<xhtml:link rel="alternate" hreflang="x-default" href="{escape(ORIGIN+path)}"/>'
        entries.append('<url><loc>'+escape(ORIGIN+localized(path,lang))+'</loc>'+alternates+'</url>')
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'+'\n'.join(entries)+'\n</urlset>\n',encoding='utf-8')
print('Built 12 pages in Portuguese, English, Spanish and Arabic with language selectors and hreflang.')
