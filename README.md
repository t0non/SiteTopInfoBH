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
