from pathlib import Path
from urllib.parse import quote
import re, html

root = Path(__file__).parent
home = root / 'dist/index.html'
source = home.read_text(encoding='utf-8')
item = (
    '<li class="mega-menu-item mega-menu-item-type-custom mega-menu-item-object-custom'
    ' mega-menu-item-has-children mega-menu-flyout remote-nav-extra" id="mega-menu-item-remote">'
    '<a class="mega-menu-link" href="/suporte-remoto/">Suporte'
    '<span class="mega-indicator"></span></a>'
    '<ul class="mega-sub-menu">'
    '<li class="mega-menu-item mega-menu-item-type-custom mega-menu-item-object-custom" id="mega-menu-item-remote-sub">'
    '<a class="mega-menu-link" href="/suporte-remoto/">Suporte remoto</a></li>'
    '<li class="mega-menu-item mega-menu-item-type-custom mega-menu-item-object-custom" id="mega-menu-item-lawyers-sub">'
    '<a class="mega-menu-link" href="/suporte-para-advogados/">Para advogados</a></li>'
    '</ul></li>'
)
if 'id="mega-menu-item-remote"' not in source:
    source = source.replace('<li class="mega-call-phone', item + '<li class="mega-call-phone', 1)
    home.write_text(source, encoding='utf-8')

header = source[source.index('<header id="masthead"'):source.index('</header>') + len('</header>')]
for anchor in ('cameras', 'manutencao', 'depoimentos', 'sobre'):
    header = header.replace('href="#' + anchor + '"', 'href="/#' + anchor + '"')
header = header.replace('aria-label=""', 'aria-label="Abrir menu de navegação"')
footer = source[source.index("<div id='footer-area'>"):source.index('</div><!-- #page -->')]
custom = re.search(r'<style id="wp-custom-css">(.*?)</style>', source, re.S).group(1)
styles = []
for key in ('megamenu-css', 'sparkling-bootstrap-css', 'sparkling-style-css', 'font-awesome-free-css', 'elementor-gf-local-roboto-css', 'elementor-gf-local-rajdhani-css'):
    styles.append(re.search(r'<link[^>]+id=[\'"]' + key + r'[\'"][^>]*>',source).group(0))
content = (root / 'remote-content.html').read_text(encoding='utf-8')
def contact(m):
    return m.group(0).replace('href="#atendimento"', 'href="https://api.whatsapp.com/send?phone=5531991133939&amp;text=' + quote(html.unescape(m.group(1))) + '" target="_blank" rel="noopener noreferrer"')
content = re.sub(r'<a[^>]*data-contact="([^"]+)"[^>]*>', contact, content)
scripts = []
for key in ('jquery-core-js', 'jquery-migrate-js', 'hoverIntent-js', 'megamenu-js'):
    tag = re.search(r'<script[^>]+id=[\'"]' + key + r'[\'"][^>]*>.*?</script>', source, re.S)
    if tag: scripts.append(tag.group(0))
page = '''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Suporte Remoto e Help Desk de TI em Belo Horizonte | Top Info BH</title>
<meta name="description" content="Suporte remoto de TI e Help Desk em Belo Horizonte para empresas e home office. Resolva lentidão, PJe, impressoras, rede e e-mails com início imediato. Peça seu orçamento!">
<meta name="robots" content="index,follow"><link rel="icon" href="/assets/598fbf0a1188592a.png">
''' + '\n'.join(styles) + '<style>' + custom + '</style><link rel="stylesheet" href="/assets/suporte-remoto.css?v=7"></head><body><a class="sr-only sr-only-focusable" href="#content">Ir para o conteúdo</a>' + header + content + footer + '''<a class="remote-float" href="https://api.whatsapp.com/send?phone=5531991133939&amp;text=Ol%C3%A1%21%20Preciso%20de%20suporte%20remoto%20de%20TI." target="_blank" rel="noopener noreferrer" aria-label="Solicitar suporte remoto pelo WhatsApp"><img src="/assets/3c88161b62504a20.png" alt="WhatsApp" width="60" height="60"></a>''' + '\n'.join(scripts) + '</body></html>'
out = root / 'dist/suporte-remoto'
out.mkdir(exist_ok=True)
(out / 'index.html').write_text(page, encoding='utf-8')
print('Created dist/suporte-remoto/index.html and updated home navigation.')
