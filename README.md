# TopInfoBH — reprodução

Cópia estática do site público https://topinfobh.com.br/, capturada em 28/10/2026.

## Executar

Execute `npm run dev` e abra http://127.0.0.1:4173/.

O site está em `dist/index.html` e os recursos locais em `dist/assets/`.
Não é necessário instalar dependências. Python precisa estar disponível.

## Conteúdo preservado

HTML original, layout responsivo, fotos, logos, fontes, ícones, estilos, scripts,
seções de serviços, apresentação e depoimentos. Links de WhatsApp, redes sociais
e avaliações mantêm os destinos originais. As avaliações são as da captura;
a integração de atualização do WordPress não faz parte da cópia estática.

`original.html` preserva o HTML recebido. `mirror-report.json` registra cada URL
baixada e eventuais falhas. `mirror.py` permite repetir a captura, com acesso à rede.
Dois recursos decorativos do tema (`bg_home.svg` e `raio.svg`) retornaram erro 500
no servidor original. As fotos principais foram baixadas.

Tags de rastreamento do Google Tag Manager e Hostinger foram removidas da cópia.
Não há painel administrativo ou backend WordPress nesta versão.

## Página de suporte remoto

A landing page fica em `/suporte-remoto/`, com link no menu da página inicial.
Inclui suporte a PJe e certificado digital, impressoras, armazenamento,
desempenho, e-mail e conectividade, explicação do atendimento e perguntas frequentes.
Os botões abrem o WhatsApp com uma mensagem específica para cada serviço.

Para editar: `remote-content.html` contém o conteúdo e
`dist/assets/suporte-remoto.css` contém os estilos. Execute `python build-remote.py`
após alterar o conteúdo para gerar `dist/suporte-remoto/index.html`.

## SEO e advocacia

A página `/suporte-para-advogados/` tem conteúdo próprio para PJe e certificado.
Use `python build-seo.py` como comando final para gerar todas as páginas com
metadados de produção, links internos, `sitemap.xml` e `robots.txt`.
O domínio canônico é `https://topinfobh.com.br`. Consulte `PUBLICACAO-SEO.md`
para publicar na hospedagem principal e solicitar indexação no Search Console.
A prévia do Sites permanece privada e não é indexável pelo Google.
