# Publicação e indexação no domínio principal

Os arquivos de produção foram preparados para **https://topinfobh.com.br**.
A hospedagem privada no endereço chatgpt.site continua sendo apenas uma prévia:
o Google não consegue indexar páginas que exigem autenticação.

## O que está pronto

- Página de suporte remoto com foco em Belo Horizonte: `/suporte-remoto/`.
- Página específica para advocacia, PJe e certificado: `/suporte-para-advogados/`.
- Títulos e descrições próprios, canonical, metadados sociais e links internos.
- Dados estruturados de organização, serviço, navegação e perguntas visíveis.
- `sitemap.xml` com as três URLs canônicas e `robots.txt` permitindo rastreamento.
- Arquivos HTML sem `noindex`, sem repetição artificial de palavras-chave.

## Publicar no servidor correto

Não foram alterados o domínio, o DNS nem a instalação WordPress em produção.
O site atual é WordPress: faça backup antes de integrar estas páginas.

Para uma substituição completa por site estático, publique **o conteúdo de `dist/`**
na raiz pública da hospedagem, preservando a estrutura das pastas. Não apague uma
instalação WordPress existente sem planejar a migração.

Para manter o WordPress, integre as duas páginas ao tema ou à hospedagem e garanta
que `/assets/` sirva os recursos locais referenciados. Um administrador deve
conciliar o sitemap e o robots.txt com os gerados pelos plugins SEO. As três URLs
precisam abrir sem login, com HTTP 200, sem cabeçalhos `X-Robots-Tag: noindex` e sem
redirecionamentos para a cópia privada. Não crie um segundo site público espelhado.

## Depois da publicação

1. Verifique no domínio principal as páginas, `/robots.txt` e `/sitemap.xml`.
2. Verifique a propriedade do domínio no Google Search Console com a conta do responsável.
3. Envie `https://topinfobh.com.br/sitemap.xml` no Search Console.
4. Inspecione as duas URLs novas e solicite a indexação.
5. Acompanhe cobertura e consultas. Cadastro no sitemap não garante indexação nem posição.

O Search Console não foi configurado nem recebeu envio de sitemap nesta tarefa.
Não há garantia de prazo, tráfego ou posição no Google. O suporte prestado é pago
conforme orçamento; a aquisição orgânica de visitantes não exige comprar anúncios.

## Regenerar os arquivos

Edite `remote-content.html` e `lawyers-content.html`, depois execute
`python build-seo.py`. Esse comando regenera as páginas, o sitemap e os metadados
com o domínio correto. Execute-o por último se também atualizar a captura do site.

Referências oficiais:
- https://developers.google.com/search/docs/essentials/spam-policies
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
- https://developers.google.com/search/docs/crawling-indexing/block-indexing
