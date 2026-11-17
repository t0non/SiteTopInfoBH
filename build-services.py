"""
Script to generate dedicated high-conversion, local SEO landing pages for each IT service.
"""
from pathlib import Path
from urllib.parse import quote
import html, json, re

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
ORIGIN = 'https://topinfobh.com.br'

SERVICES = [
    {
        'slug': 'limpeza-de-virus',
        'nav_title': 'Limpeza de Vírus e Pop-ups',
        'eyebrow': 'REMOÇÃO DE VÍRUS E MALWARES EM BELO HORIZONTE',
        'h1': 'Computador com vírus, anúncios ou travando?<br><span>Limpamos e blindamos seu PC à distância.</span>',
        'desc': 'Elimine vírus, trojans, adwares e janelas chatas pulando na tela sem sair de casa. Suporte remoto rápido, seguro e sem formatar.',
        'icon': 'virus', # custom svg
        'whatsapp_msg': 'Olá! Meu computador está com vírus e janelas de propaganda abrindo sozinhas. Preciso de ajuda pelo suporte remoto.',
        'cta_btn': 'ELIMINAR VÍRUS DO MEU COMPUTADOR',
        'problems': [
            ('Janelinhas pulando na tela', 'Pop-ups com anúncios indesejados abrindo toda hora no navegador ou na área de trabalho.'),
            ('Avisos vermelhos falsos', 'Mensagens assustadoras fingindo que o computador foi bloqueado ou infectado pedindo para ligar para um número.'),
            ('Navegador modificado', 'O Google abre com outro buscador estranho (Yahoo, Bing estranho, buscadores desconhecidos).'),
            ('Lentidão extrema e travamento', 'O computador demora minutos para responder cliques e o cooler fica girando alto sem motivo.'),
            ('Arquivos sumiram ou atalhos criados', 'Pen drives com arquivos transformados em atalho e pastas ocultas por vírus.'),
            ('Antivírus desativado à força', 'Programas de proteção que não abrem ou dão erro ao tentar fazer varredura.')
        ],
        'how_it_works': 'Conectamos com segurança via AnyDesk, localizamos e neutralizamos os programas maliciosos em tempo real na sua frente, limpamos extensões nocivas e instalamos proteção definitiva sem você perder seus arquivos pessoais.',
        'faqs': [
            ('Preciso formatar o computador para tirar o vírus?', 'Na grande maioria dos casos, não! Conseguimos identificar a raiz do vírus e removê-lo completamente mantendo todos os seus documentos, fotos e programas intactos.'),
            ('O técnico consegue ver minhas fotos ou senhas?', 'Não. Você acompanha cada movimento do mouse ao vivo na tela. Nosso foco é 100% no sistema operacional e nos arquivos de inicialização do Windows.'),
            ('Quanto tempo demora a limpeza de vírus?', 'Geralmente entre 30 e 50 minutos, dependendo da gravidade e da quantidade de malwares instalados.'),
            ('Vocês instalam um antivírus confiável?', 'Sim! Além da limpeza completa, orientamos e instalamos soluções de segurança eficientes e leves para seu computador não voltar a pegar pragas.')
        ]
    },
    {
        'slug': 'conserto-impressora',
        'nav_title': 'Configuração de Impressoras',
        'eyebrow': 'SUPORTE TÉCNICO DE IMPRESSORAS EM BELO HORIZONTE',
        'h1': 'A impressora parou de funcionar?<br><span>Resolvemos conexão Wi-Fi, spooler e drivers na hora.</span>',
        'desc': 'Impressora offline, documento preso na fila ou erro de conexão? Configuramos HP, Epson, Canon, Brother e impressoras em rede por suporte remoto.',
        'icon': 'fas fa-print',
        'whatsapp_msg': 'Olá! Minha impressora parou de imprimir e está dando erro. Preciso de suporte remoto para configurar.',
        'cta_btn': 'CONSERTAR MINHA IMPRESSORA AGORA',
        'problems': [
            ('Impressora fica Offline', 'O cabo ou o Wi-Fi estão ligados, mas o Windows insiste em dizer que o equipamento está desconectado.'),
            ('Documento preso na fila', 'Você manda imprimir e o documento fica "imprimindo" para sempre sem sair da fila de impressão.'),
            ('Erro de Driver ou Spooler', 'Aviso de "O serviço de spooler de impressão não está em execução" ou driver incompatível.'),
            ('Perda do Wi-Fi após troca de modem', 'Você trocou de provedor de internet e a impressora não se conecta mais aos computadores da casa.'),
            ('Scanner não digitaliza', 'A impressora imprime, mas o scanner não abre ou diz que não há dispositivo conectado.'),
            ('Impressora não aparece nos outros PCs', 'Computador principal imprime, mas os outros aparelhos da rede da empresa não acham a impressora.')
        ],
        'how_it_works': 'Identificamos se o erro é no serviço do Windows, no driver ou no IP da rede, reiniciamos o spooler, instalamos os pacotes oficiais corretos e fazemos um teste de impressão com você acompanhando ao vivo.',
        'faqs': [
            ('Vocês consertam qualquer marca de impressora?', 'Sim! HP, Epson (EcoTank), Canon (MegaTank), Brother, Samsung, Xerox, Lexmark e impressoras térmicas (cupom fiscal/não fiscal).'),
            ('Dá para resolver se o problema for no Wi-Fi?', 'Sim. Reconfiguramos a porta TCP/IP e conectamos a impressora diretamente aos computadores pela rede local.'),
            ('E se o problema for mecânico (papel atolado ou quebrado)?', 'Se identificarmos que é defeito físico de peças ou rolete, informamos com total transparência para que você não gaste à toa.')
        ]
    },
    {
        'slug': 'computador-lento',
        'nav_title': 'Otimização de Computador Lento',
        'eyebrow': 'OTIMIZAÇÃO E ACELERAÇÃO DE COMPUTADORES EM BH',
        'h1': 'Computador lento demais e travando?<br><span>Turbinamos a velocidade do seu PC pela internet.</span>',
        'desc': 'Ligue o PC em segundos e abra programas sem engasgos. Limpeza profunda de inicialização, arquivos temporários, erros de registro e otimização do Windows.',
        'icon': 'fas fa-hourglass-half',
        'whatsapp_msg': 'Olá! Meu computador está muito lento e travando. Gostaria de fazer uma otimização e limpeza pelo suporte remoto.',
        'cta_btn': 'DEIXAR MEU COMPUTADOR RÁPIDO',
        'problems': [
            ('Demora minutos para ligar', 'Você aperta o botão de ligar e tem tempo de tomar um café antes do Windows ficar utilizável.'),
            ('Mouse girando e tela congelando', 'Qualquer programa que você abre trava e aparece "(Não respondendo)".'),
            ('Disco em 100% no Gerenciador', 'A luz do HD fica acesa direto e o sistema operacional fica completamente engasgado.'),
            ('Programas desnecessários ao iniciar', 'Dezenas de programas abrindo sozinhos e consumindo toda a memória RAM.'),
            ('Navegador pesado com muitas abas', 'Abrir o Chrome ou Edge faz o computador chiar e travar tudo.'),
            ('Aquecimento e barulho excessivo', 'Processos fantasmas rodando em segundo plano e fritando o processador.')
        ],
        'how_it_works': 'Desativamos programas parasitas que sobrecarregam o boot, otimizamos os serviços do Windows, limpamos gigabytes de lixo do sistema e ajustamos a memória virtual para seu computador voar de novo.',
        'faqs': [
            ('O computador realmente fica mais rápido sem trocar peças?', 'Sim! A maioria dos computadores perde até 70% de velocidade apenas com acúmulo de lixo digital e processos em segundo plano.'),
            ('Vale a pena colocar um SSD?', 'Se o seu equipamento ainda usa disco rígido antigo (HD mecânico), orientamos a melhor opção de SSD em BH para multiplicar a velocidade por 10x.'),
            ('Vou perder meus programas instalados?', 'Não. A otimização preserva todas as suas configurações, arquivos, fotos e programas.')
        ]
    },
    {
        'slug': 'configuracao-email',
        'nav_title': 'Configuração de E-mails e Outlook',
        'eyebrow': 'SUPORTE PARA E-MAILS E OUTLOOK EM BELO HORIZONTE',
        'h1': 'Não consegue abrir ou enviar e-mails?<br><span>Corrigimos Outlook, erro de senha e sincronização.</span>',
        'desc': 'Outlook pedindo senha sem parar, mensagens paradas na Caixa de Saída ou e-mails sumindo? Resolvemos contas POP, IMAP, Exchange e Google Workspace.',
        'icon': 'fas fa-envelope',
        'whatsapp_msg': 'Olá! Estou com problemas no meu e-mail / Outlook no computador. Preciso de suporte remoto para resolver.',
        'cta_btn': 'CONSERTAR MEU E-MAIL AGORA',
        'problems': [
            ('Outlook pedindo senha em loop', 'Você digita a senha certa, mas a janelinha de credenciais volta a aparecer o tempo todo.'),
            ('E-mails não saem da Caixa de Saída', 'As mensagens ficam presas e seus clientes ou parceiros não recebem nada.'),
            ('Erro de envio/recebimento (0x800...)', 'Erros criptografados de porta SSL/TLS ou servidor SMTP indisponível.'),
            ('Arquivo PST/OST corrompido ou cheio', 'O arquivo de dados atingiu o limite de tamanho e o Outlook trava ao abrir.'),
            ('Migração de conta corporativa', 'Precisa configurar o e-mail da sua empresa no computador novo com assinatura e pastas.'),
            ('E-mails não sincronizam com o celular', 'Você lê uma mensagem no computador e ela continua como não lida no celular.')
        ],
        'how_it_works': 'Ajustamos as portas seguras de entrada e saída (IMAP/SMTP), corrigimos arquivos de dados danificados, reconfiguramos o perfil e garantimos o fluxo de mensagens com privacidade absoluta.',
        'faqs': [
            ('O técnico vai ler meus e-mails?', 'Jamais! O trabalho é restrito às telas de configuração de conta, portas e teste de conexão. Você assiste tudo na tela em tempo real.'),
            ('Vocês configuram e-mail profissional de empresa?', 'Sim, configuramos domínio próprio (@suaempresa.com.br), Microsoft 365, Google Workspace, Locaweb, HostGator, Hostinger e cPanel.')
        ]
    },
    {
        'slug': 'liberar-espaco-disco',
        'nav_title': 'Liberar Espaço no Disco C:',
        'eyebrow': 'LIMPEZA DE DISCO E MEMÓRIA EM BELO HORIZONTE',
        'h1': 'Disco C vermelho e sem espaço?<br><span>Liberamos gigabytes com total segurança para seus arquivos.</span>',
        'desc': 'Computador avisando que a memória está cheia? Fazemos uma varredura profunda eliminando arquivos temporários, logs antigos e caches ocultos sem apagar seus dados.',
        'icon': 'fas fa-hdd',
        'whatsapp_msg': 'Olá! Meu computador está com o disco C cheio e sem espaço. Gostaria de liberar espaço com suporte remoto.',
        'cta_btn': 'LIBERAR ESPAÇO NO MEU COMPUTADOR',
        'problems': [
            ('Barra do Disco C vermelha', 'O Windows avisa diariamente que o espaço em disco é insuficiente.'),
            ('Não consegue baixar arquivos nem atualizar', 'Downloads cancelados no meio e Windows Update travando por falta de espaço.'),
            ('Lixo oculto acumulado por anos', 'Gigabytes de arquivos temporários do Windows, instaladores antigos e cache do navegador.'),
            ('Medo de apagar algo importante', 'Você não sabe o que pode excluir sem quebrar o sistema operacional.'),
            ('Pastas duplicadas e downloads esquecidos', 'Acúmulo de arquivos repetidos pesando desnecessariamente no disco.')
        ],
        'how_it_works': 'Usamos ferramentas especializadas de análise forense de disco para identificar onde estão os maiores blocos de dados inúteis e limpamos tudo de forma cirúrgica.',
        'faqs': [
            ('Existe perigo de apagar fotos ou documentos meus?', 'Zero perigo. Nós só limpamos arquivos temporários e caches de sistema. Caso haja arquivos pesados seus para organizar, você decide na hora.'),
            ('Quanto espaço costuma liberar?', 'Geralmente liberamos entre 15 GB e 60 GB de espaço que estavam bloqueados por lixo eletrônico.')
        ]
    },
    {
        'slug': 'instalacao-programas',
        'nav_title': 'Instalação de Programas e Softwares',
        'eyebrow': 'INSTALAÇÃO SEGURA DE SOFTWARES EM BELO HORIZONTE',
        'h1': 'Precisa instalar um programa e não consegue?<br><span>Instalamos, atualizamos e configuramos para você.</span>',
        'desc': 'Pacote Office, leitores de PDF, navegadores, antivírus, softwares de trabalho e utilitários instalados de forma oficial, limpa e sem vírus.',
        'icon': 'fas fa-download',
        'whatsapp_msg': 'Olá! Preciso instalar e configurar alguns programas no meu computador. Podem me ajudar pelo suporte remoto?',
        'cta_btn': 'INSTALAR PROGRAMAS NO MEU PC',
        'problems': [
            ('Erro ao instalar ou instalar travado', 'A barra de instalação para na metade ou dá mensagem de "Erro desconhecido".'),
            ('Medo de baixar de sites falsos com vírus', 'Baixar programas da internet sem saber qual botão de download é verdadeiro.'),
            ('Programas que não abrem após atualizar', 'Softwares que pararam de funcionar de repente após uma atualização do Windows.'),
            ('Configuração de periféricos e drivers', 'Instalação de webcam, mesa digitalizadora, leitor de código de barras ou assinatura digital.'),
            ('Programas do governo e tributários', 'Instalação de IRPF (Receita Federal), emissor de NF-e, Java e navegadores compatíveis.')
        ],
        'how_it_works': 'Baixamos os instaladores diretamente dos repositórios oficiais dos fabricantes, realizamos a instalação limpa (sem barras extras nem adwares) e deixamos os atalhos prontos na sua área de trabalho.',
        'faqs': [
            ('Vocês instalam programas piratas?', 'Não. Trabalhamos exclusivamente com softwares homologados, gratuitos ou licenças adquiridas pelo cliente, garantindo a sua segurança jurídica e digital.'),
            ('Instalam pacote Office (Word, Excel)?', 'Configuramos sua conta Microsoft 365 ou instalamos alternativas gratuitas compatíveis como LibreOffice com perfeição.')
        ]
    }
]

def render_service_page(svc, template_html):
    icon_html = f'<i class="{svc["icon"]}" aria-hidden="true"></i>' if svc["icon"] != 'virus' else '<img src="/assets/virus.png" alt="Vírus" class="service-icon-img">'

    problems_cards = "".join(f'''
      <article class="remote-service">
        <i class="fas fa-exclamation-circle text-blue" aria-hidden="true"></i>
        <h3>{title}</h3>
        <p>{desc}</p>
        <a data-contact="{html.escape(svc['whatsapp_msg'], quote=True)}" href="#atendimento">Resolver este problema <span aria-hidden="true">→</span></a>
      </article>''' for title, desc in svc['problems'])

    faqs_html = "".join(f'''
      <details>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>''' for q, a in svc['faqs'])

    content = f'''<main id="content" class="remote">
  <!-- HERO SECTION -->
  <section class="remote-hero">
    <div class="remote-container remote-hero-grid">
      <div>
        <p class="eyebrow"><i class="fas fa-shield-alt" aria-hidden="true"></i> {svc['eyebrow']}</p>
        <h1>{svc['h1']}</h1>
        <p class="hero-description">{svc['desc']}</p>
        
        <div class="hero-actions">
          <a class="remote-button remote-button-pulse" data-contact="{html.escape(svc['whatsapp_msg'], quote=True)}" href="#atendimento">
            <i class="fab fa-whatsapp" aria-hidden="true"></i> {svc['cta_btn']}
          </a>
          <a class="remote-button-secondary" href="#sintomas">
            <i class="fas fa-chevron-down" aria-hidden="true"></i> Ver sintomas comuns
          </a>
        </div>
        
        <div class="hero-trust-badges">
          <span><i class="fas fa-eye" aria-hidden="true"></i> Você assiste tudo ao vivo</span>
          <span><i class="fas fa-home" aria-hidden="true"></i> Sem sair de casa</span>
          <span><i class="fas fa-lock" aria-hidden="true"></i> Conexão 100% segura</span>
          <span><i class="fas fa-award" aria-hidden="true"></i> Atendimento em Belo Horizonte</span>
        </div>
      </div>
      
      <div class="support-visual" aria-label="Painel de suporte técnico da Top Info BH">
        <div class="monitor">
          <div class="monitor-top">
            <img src="/assets/75c233edaf0044c6.png" alt="Top Info BH">
            <span class="status-live"><span class="pulse-dot"></span> Atendimento Imediato em BH</span>
          </div>
          <div class="monitor-body">
            <span class="screen-icon">{icon_html}</span>
            <h2>{svc['nav_title']}</h2>
            <p>Diagnóstico rápido e orçamento combinado antes de começar.</p>
            <div class="screen-tags">
              <span><i class="fas fa-check" aria-hidden="true"></i> Sem carregar peso</span>
              <span><i class="fas fa-check" aria-hidden="true"></i> Suporte seguro</span>
              <span><i class="fas fa-check" aria-hidden="true"></i> Nota Fiscal e Garantia</span>
            </div>
          </div>
        </div>
        <div class="monitor-base"></div>
        <div class="visual-caption"><i class="fas fa-user-check" aria-hidden="true"></i> Atendimento assistido em tempo real na sua frente.</div>
      </div>
    </div>
  </section>

  <!-- QUICK VALUE STRIP -->
  <div class="remote-strip">
    <div class="remote-container">
      <span><i class="fas fa-couch" aria-hidden="true"></i> Sem levar na assistência</span>
      <span><i class="fas fa-eye" aria-hidden="true"></i> Você vê tudo ao vivo</span>
      <span><i class="fas fa-clock" aria-hidden="true"></i> Atendimento em minutos</span>
      <span><i class="fas fa-hand-holding-usd" aria-hidden="true"></i> Valor combinado antes</span>
    </div>
  </div>

  <nav class="breadcrumbs remote-container" aria-label="Você está em">
    <a href="/">Início</a><span aria-hidden="true"> / </span><a href="/suporte-remoto/">Suporte Remoto</a><span aria-hidden="true"> / </span><span>{svc['nav_title']}</span>
  </nav>

  <!-- SINTOMAS / PROBLEMAS -->
  <section class="remote-section" id="sintomas">
    <div class="remote-container">
      <div class="section-intro">
        <p class="eyebrow">SINTOMAS FREQUENTES</p>
        <h2>Identificou algum destes <span>problemas no seu computador?</span></h2>
        <p>Veja os casos mais recorrentes que resolvemos diariamente em Belo Horizonte através do suporte técnico remoto:</p>
      </div>

      <div class="services-grid">
        {problems_cards}
      </div>
    </div>
  </section>

  <!-- COMO FUNCIONA -->
  <section class="remote-section how-section">
    <div class="remote-container">
      <div class="section-intro">
        <p class="eyebrow">PASSO A PASSO</p>
        <h2>Como resolvemos o seu problema <span>pela internet:</span></h2>
        <p>{svc['how_it_works']}</p>
      </div>

      <div class="steps">
        <article>
          <span class="step-number">01</span>
          <h3>Chame no WhatsApp</h3>
          <p>Você conta o que está acontecendo. Avaliamos a situação e passamos o orçamento fechado antes de iniciar.</p>
        </article>
        <article>
          <span class="step-number">02</span>
          <h3>Autorize o Acesso</h3>
          <p>Você abre um programinha oficial e seguro (como AnyDesk) e nos informa o código na tela. Ninguém entra sem sua permissão.</p>
        </article>
        <article>
          <span class="step-number">03</span>
          <h3>Acompanhe ao Vivo</h3>
          <p>Você assiste cada clique e conserto na sua frente em tempo real. Ao terminar, fechamos a sessão e pronto!</p>
        </article>
      </div>
      <p class="how-note"><i class="fas fa-shield-alt text-green" aria-hidden="true"></i> <strong>Privacidade absoluta:</strong> Conexão criptografada de ponta a ponta. Você acompanha tudo e pode interromper o acesso a qualquer segundo.</p>
    </div>
  </section>

  <!-- DÚVIDAS FREQUENTES -->
  <section class="remote-section faq-section" id="duvidas">
    <div class="remote-container faq-grid">
      <div>
        <p class="eyebrow">DÚVIDAS FREQUENTES</p>
        <h2>Perguntas e respostas sobre <span>este serviço.</span></h2>
        <p>Tire suas dúvidas antes de solicitar o atendimento.</p>
        <div class="faq-cta-box">
          <p><strong>Quer tirar uma dúvida específica?</strong></p>
          <a class="text-link" data-contact="Olá! Tenho uma dúvida sobre o serviço de {svc['nav_title']}." href="#atendimento">Falar com o técnico no WhatsApp <span aria-hidden="true">→</span></a>
        </div>
      </div>
      <div class="faq-list">
        {faqs_html}
      </div>
    </div>
  </section>

  <!-- CTA FINAL -->
  <section class="contact-section" id="atendimento">
    <div class="remote-container">
      <p class="eyebrow">ATENDIMENTO IMEDIATO EM BELO HORIZONTE</p>
      <h2>Vamos resolver o problema do seu computador agora?</h2>
      <p class="contact-lead">Clique no botão abaixo, fale direto com o nosso técnico e receba um atendimento humano, paciente e sem compromisso.</p>
      <a class="remote-button remote-button-large" data-contact="{html.escape(svc['whatsapp_msg'], quote=True)}" href="#atendimento">
        <i class="fab fa-whatsapp" aria-hidden="true"></i> CONVERSAR NO WHATSAPP COM O TÉCNICO
      </a>
      <div class="contact-guarantees">
        <span><i class="fas fa-check text-green" aria-hidden="true"></i> Orçamento sem compromisso</span>
        <span><i class="fas fa-check text-green" aria-hidden="true"></i> Sem precisar sair de casa</span>
        <span><i class="fas fa-check text-green" aria-hidden="true"></i> Mais de 15 anos de confiança em BH</span>
      </div>
    </div>
  </section>
</main>'''

    # Apply whatsapp link formatting to data-contact
    def contact(m):
        return m.group(0).replace('href="#atendimento"', 'href="https://api.whatsapp.com/send?phone=5531991133939&amp;text=' + quote(html.unescape(m.group(1))) + '" target="_blank" rel="noopener noreferrer"')
    content = re.sub(r'<a[^>]*data-contact="([^"]+)"[^>]*>', contact, content)

    # Replace <main> in template
    return re.sub(r'<main\b.*?</main>', lambda _: content, template_html, count=1, flags=re.S)

if __name__ == '__main__':
    base_template = (DIST / 'suporte-remoto/index.html').read_text(encoding='utf-8')
    for svc in SERVICES:
        out_dir = DIST / svc['slug']
        out_dir.mkdir(parents=True, exist_ok=True)
        html_out = render_service_page(svc, base_template)
        (out_dir / 'index.html').write_text(html_out, encoding='utf-8')
        print(f"Created page: dist/{svc['slug']}/index.html")

