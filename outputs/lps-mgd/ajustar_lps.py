#!/usr/bin/env python3
"""Ajusta as LPs de output-lps/ e grava em output-lps/ajustados/.

Corrige: vazamento "Pilar Corporativo", afirmações sem base na página do produto,
links internos quebrados, ausência de WhatsApp e de BreadcrumbList, e o bloco
"Benefícios" que era idêntico entre as LPs. Cada troca é conferida (falha se o texto não existir).
"""
import os, re, sys, urllib.parse

SRC, DST = "output-lps", "output-lps/ajustados"
WA_MSG = "Olá, vim pelo site MGD e gostaria de orçamento de Samsung Galaxy Tab Active5 5G."
WA = ("https://api.whatsapp.com/send/?phone=5511986350609&text=" + urllib.parse.quote(WA_MSG)
      + "&type=phone_number&app_absent=0")
WA_BTN = (' <a class="btn" style="margin-left:12px" href="' + WA + '" target="_blank" rel="noopener"'
          ' data-track="whatsapp">Falar no WhatsApp</a>')

PILARES = [("Logística", "logistica"), ("Governo", "governo"), ("Manufatura", "manufatura"),
           ("Mineração", "mineracao"), ("Saúde", "saude"), ("Serviços", "servicos"),
           ("Utilities", "utilities"), ("Bens de consumo", "bens-de-consumo")]
NAV = ('<nav class="related" aria-label="Outros segmentos do Active5">\n' + "\n".join(
    f'                <a href="https://mgd-dist.com.br/tablet-robusto-active5-{s}/">{n}</a>' for n, s in PILARES)
    + "\n            </nav>")

def beneficios(kicker, h2, cards):
    c = "\n".join(f'                <article class="card">\n                    <h3>{t}</h3>\n                    <p>{p}</p>\n                </article>' for t, p in cards)
    return (f'<section id="beneficios">\n        <div class="wrap"><span class="kicker">{kicker}</span>\n'
            f'            <h2>{h2}</h2>\n            <div class="grid">\n{c}\n            </div>\n        </div>\n    </section>')

# (arquivo) -> dict(crumb, beneficios, trocas)
P = {}
P["tablet-industrial-samsung"] = dict(
    crumb="Corporativo",
    ben=beneficios("Benefícios para operações corporativas", "Uma frota padronizada e pronta para a rotina", [
        ("Padronização da frota", "Um único modelo para filiais e equipes facilita suporte, acessórios e treinamento."),
        ("Menos paradas por quebra", "IP68 e MIL-STD-810H foram pensados para rotinas exigentes, dentro dos limites do fabricante."),
        ("Bateria planejável", "A bateria removível permite planejar trocas e turnos, com acessórios avaliados na proposta.")]),
    trocas=[
        ("/ Pilar Corporativo</nav>", "/ Corporativo</nav>"),
        ("Aplicações em Pilar Corporativo", "Aplicações corporativas"),
        ("Active5 para Pilar Corporativo: tire suas dúvidas", "Active5 para empresas: tire suas dúvidas"),
        ("sua operação de pilar corporativo", "sua operação corporativa"),
        ("combina a confiabilidade do hardware militar com o ecossistema Android corporativo e a segurança Samsung Knox.",
         "combina robustez certificada (IP68 e MIL-STD-810H) com o ecossistema Android."),
        ('<span class="chip">Garantia Nacional</span>', '<span class="chip">Distribuição MGD</span>'),
        ("Distribuidora oficial com estoque no Brasil, faturamento direto e garantia de fábrica.",
         "Distribuidora MGD, do Grupo MGITECH. Garantia, prazo e faturamento são definidos na proposta."),
        ("Disponibilidade imediata para projetos corporativos de TI e automação.", "Consulte a disponibilidade para o seu projeto corporativo."),
        ("O Galaxy Tab Active5 oferece ciclo de vida estendido, atualizações de segurança garantidas, facilidade de gerenciamento via MDM e durabilidade para múltiplos anos de operação pesada.",
         "O Galaxy Tab Active5 foi projetado para rotinas pesadas, com certificação IP68 e MIL-STD-810H. Políticas de atualização e gerenciamento (MDM) devem ser validadas com o fabricante e com a sua TI."),
        ("Tablets comuns descontinuados a cada 6 meses, quebrando a padronização da frota", "Tablets comuns com reposição frequente, quebrando a padronização da frota"),
        ("Vulnerabilidades de segurança em aparelhos sem proteção em nível de chip", "Gestão e segurança difíceis quando cada equipe usa um modelo diferente"),
        ("Configuração em massa, bloqueio de apps indevidos e atualização silenciosa via Knox Manage.", "Configuração em massa e controle de aplicativos com a solução de MDM adotada pela empresa."),
        ("Suporte a troca de baterias sem parada e estações de carregamento coletivas (Multi-slot cradle).", "Bateria removível e planejamento de carregamento coletivo; acessórios são avaliados na proposta."),
        ("Conexão com leitores RFID, scanners de anel, impressoras e balanças industriais.", "Conexão com acessórios compatíveis, conforme definido na proposta."),
        ("<h3>Comunicação PTT (Push-To-Talk)</h3>\n                    <p>Botão programável lateral configurado para rádio comunicação instantânea entre equipes.</p>",
         "<h3>Registro de evidências</h3>\n                    <p>Fotos e anotações com a S Pen em aplicativos compatíveis.</p>"),
        ("Utilização em modo contínuo sem bateria em quiosques, veículos e máquinas.", "Uso em pontos fixos, veículos e máquinas, com alimentação e acessórios validados na proposta."),
        ("Fornecemos a versão oficial brasileira com conectividade 5G (SM-X306BZGAL05), homologada pela Anatel com garantia integral no país.",
         "Trabalhamos com a versão brasileira com conectividade 5G (SM-X306BZGAL05). Garantia e condições constam na proposta."),
        ("Acompanha o tablet Samsung Galaxy Tab Active5, caneta S Pen com ponta sobressalente, capa protetora de alta resistência, bateria original e cabo de dados.",
         "O tablet acompanha a S Pen. A composição completa do kit (capa, bateria, cabo e outros itens) é confirmada na proposta."),
    ])
P["tablet-para-agentes-de-transito"] = dict(
    crumb="Agentes de trânsito",
    ben=beneficios("Benefícios para agentes de trânsito", "Hardware alinhado ao trabalho na rua", [
        ("Consulta e autuação no local", "Reduza idas e vindas à base, usando os aplicativos do órgão direto na via."),
        ("Toque com luvas", "A tela sensível com luvas ajuda no preenchimento durante a abordagem; valide o modelo de luva da equipe."),
        ("Chuva e poeira", "IP68 protege contra água e poeira, conforme as condições do fabricante.")]),
    trocas=[
        ('<span class="chip">Tela Antirreflexo</span>', '<span class="chip">Toque com luvas</span>'),
        ("Agilize blitzes, consultas ao Renavam/Renach e emissão eletrônica de infrações com o Samsung Galaxy Tab Active5. Robustez comprovada para motociclistas e viaturas.",
         "Agilize blitzes, consultas a sistemas de trânsito e emissão eletrônica de infrações com o Samsung Galaxy Tab Active5, conforme os aplicativos e integrações do seu órgão. Robustez para uso em vias públicas."),
        ("Compatível com suportes veiculares robustos e docas POGO de recarga rápida.", "Suportes veiculares e acessórios com pinos POGO: confirme a compatibilidade na proposta."),
        ("Prontidão operacional e conectividade 5G contínua em vias públicas.", "Prontidão operacional em vias públicas, com conectividade 5G sujeita à cobertura da operadora."),
        ("Receba proposta comercial com preços de atacado direto da distribuidora MGD para autarquias e secretarias de mobilidade urbana.",
         "Receba a proposta comercial da distribuidora MGD para autarquias e secretarias de mobilidade urbana."),
        ("O Samsung Galaxy Tab Active5 foi testado com padrões militares para resistir a quedas de até 1,8m com capa protetora, operando com luvas e em altas temperaturas.",
         "O Samsung Galaxy Tab Active5 tem certificação MIL-STD-810H e IP68, com tela sensível mesmo com luvas. Os limites de uso seguem as condições do fabricante."),
        ("Fixação em suportes robustos com alimentação contínua e desacoplamento com uma mão.", "Fixação em suportes veiculares compatíveis; os acessórios são validados na proposta."),
        ("Sim, a tecnologia do Active5 permite regular a sensibilidade da tela para toques precisos mesmo utilizando luvas de couro ou proteção.",
         "O Active5 tem tela sensível com luvas. Teste o modelo de luva usado pela equipe antes de padronizar."),
        ("Sim, conta com a plataforma de segurança Samsung Knox integrada ao hardware, homologada por agências de segurança internacionais.",
         "O Active5 roda Android corporativo. Proteção de dados e políticas de segurança dependem do MDM e dos aplicativos adotados pelo órgão."),
        ("Sim, através dos conectores magnéticos POGO laterais, garantindo carregamento rápido em bases veiculares sem desgaste de cabos.",
         "O Active5 tem pinos POGO para conectar acessórios e bases. Confirme na proposta a base de recarga compatível com o seu veículo."),
    ])
P["tablet-para-controle-de-estoque"] = dict(
    crumb="Controle de estoque",
    ben=beneficios("Benefícios para o almoxarifado", "Hardware alinhado ao trabalho no corredor", [
        ("Contagem na prateleira", "Registre contagens e movimentações no ponto da prateleira, sem papel."),
        ("Poeira e quedas", "IP68 e MIL-STD-810H apoiam o uso em depósitos, dentro dos limites do fabricante."),
        ("Bateria removível", "Planeje a troca de bateria em inventários longos.")]),
    trocas=[
        ('<span class="chip">Acuracidade Total</span><span class="chip">Leitura de Lotes</span><span class="chip">Bateria de Longa Duração</span>',
         '<span class="chip">Inventário em tempo real</span><span class="chip">Fotos e registros</span><span class="chip">Bateria Removível</span>'),
        ("oferece a velocidade necessária para auditar milhares de SKUs com acuracidade impecável.", "ajuda a contar milhares de SKUs com mais acuracidade."),
        ("Sim, o Active5 conta com câmera traseira de alta resolução com foco automático e inteligência de leitura de códigos 1D e 2D mesmo em ambientes de baixa iluminação.",
         "A câmera traseira pode ler códigos de barras e QR Code em aplicativos compatíveis. Para volume alto de leitura, a MGD também oferece leitores e coletores de dados, e indica a melhor configuração na proposta."),
        ("Sim, por rodar Android corporativo, é 100% compatível com os apps mobile dos principais ERPs e WMS de mercado.",
         "Por rodar Android, executa os aplicativos mobile de ERP e WMS, desde que o fornecedor do sistema ofereça o app. Valide com o seu fornecedor (SAP, Totvs, Sankhya etc.)."),
        ("O Active5 possui selo IP68, sendo totalmente vedado contra a entrada de partículas microscópicas de poeira e areia.",
         "O Active5 tem certificação IP68, com proteção contra poeira e água conforme as condições do fabricante."),
        ("Sim, a MGD é um distribuidor que mantém estoque estratégico corporativo à pronta entrega para atendimento ágil em todo o Brasil.",
         "Prazo e disponibilidade são informados na proposta. Informe a quantidade e o local de entrega no formulário."),
        ("Mapeamento e reendereçamento de produtos nas prateleiras com leitura óptica.", "Mapeamento e reendereçamento de produtos nas prateleiras, com leitura de códigos por aplicativos compatíveis."),
    ])
P["tablet-para-equipe-de-campo"] = dict(
    crumb="Equipes de campo",
    ben=beneficios("Benefícios para equipes de campo", "Hardware alinhado à rotina do técnico", [
        ("Evidências na hora", "Fotos, anotações e assinatura da O.S. no local, com aplicativos compatíveis."),
        ("Proteção no trajeto", "IP68 e MIL-STD-810H para chuva, poeira e quedas, conforme as condições do fabricante."),
        ("Bateria e conectividade", "Bateria removível e 5G, sujeito à cobertura, para a jornada externa.")]),
    trocas=[
        ('<span class="chip">5G Ultrarrápido</span>', '<span class="chip">Conectividade 5G</span>'),
        ('<span class="chip">GPS de Precisão</span>', '<span class="chip">S Pen incluída</span>'),
        ("Preços corporativos diferenciados para frotas de campo com suporte nacional.", "Condições comerciais e suporte para frotas de campo são definidos na proposta."),
        ("Com o Galaxy Tab Active5, seu técnico tem um aparelho certificado contra quedas de até 1,8m, proteção contra intempéries e autonomia com baterias extras para jornadas prolongadas.",
         "Com o Galaxy Tab Active5, seu técnico tem um aparelho com certificação MIL-STD-810H, proteção IP68 e bateria removível, que permite planejar baterias extras para jornadas longas."),
        ("Testes de velocidade de rede, leitura de fibra óptica e ativação de modems de clientes.", "Testes e ativações com aplicativos compatíveis e registro fotográfico da instalação."),
        ("Sim, o Samsung Galaxy Tab Active5 já vem de fábrica acompanhado da capa protetora de alta resistência que garante proteção militar contra impactos.",
         "A composição do kit é confirmada na proposta. A MGD também oferece capas robustas e películas para o Active5."),
        ("Não! A S Pen do Active5 utiliza tecnologia de ressonância magnética (EMR) e não necessita de nenhuma bateria ou recarga para funcionar.",
         "Não. A S Pen incluída é certificada IP68 e dispensa recargas, conforme a página do produto."),
        ("Sim, como distribuidora especializada, disponibilizamos baterias sobressalentes, pontas de caneta e acessórios originais.",
         "Consulte na proposta a disponibilidade de baterias sobressalentes e acessórios."),
        ("O modelo conta com modem 5G de última geração, garantindo uploads ultrarrápidos de fotos e relatórios de campo mesmo em redes de dados congestionadas.",
         "O Active5 tem conectividade 5G. A velocidade real depende da cobertura e do plano de dados da operadora."),
    ])
P["tablet-para-fiscalizacao"] = dict(
    crumb="Fiscalização",
    ben=beneficios("Benefícios para a fiscalização", "Hardware alinhado ao trabalho em campo", [
        ("Autos e termos no local", "Preencha e registre fotos no ponto da vistoria, com o sistema do órgão."),
        ("S Pen para assinatura", "S Pen incluída para assinaturas e anotações em aplicativos compatíveis."),
        ("Proteção contra o tempo", "IP68 protege contra água e poeira, conforme as condições do fabricante.")]),
    trocas=[
        ('<span class="chip">Bateria Hot-Swap</span>', '<span class="chip">Bateria Removível</span>'),
        ("lavre autos com assinatura digital na S Pen e colete fotos com alta durabilidade sob qualquer clima.", "lavre autos com assinatura na S Pen e colete fotos com um equipamento projetado para rotinas exigentes."),
        ("O Galaxy Tab Active5 possui padrão militar de resistência MIL-STD-810H, tela legível sob luz solar direta e a precisão da caneta S Pen para assinaturas digitais com validade legal.",
         "O Galaxy Tab Active5 tem certificação MIL-STD-810H e S Pen incluída para assinaturas e anotações em aplicativos compatíveis. A validade legal da assinatura depende do sistema e da norma do órgão."),
        ("Insegurança jurídica com assinaturas ilegíveis em papéis molhados", "Assinaturas ilegíveis e autos danificados em papel molhado"),
        ("Vistorias em áreas rurais e matas, registro de coordenadas GPS precisas e relatórios offline.", "Vistorias em áreas rurais e matas, com registro de localização e relatórios por aplicativos compatíveis."),
        ("Auditoria de cozinhas, hospitais e comércios com tablet lavável e passível de desinfecção.", "Auditoria de cozinhas, hospitais e comércios, com equipamento que pode ser limpo com desinfetantes."),
        ("Sim, a S Pen oferece alta precisão de toque com níveis de pressão e rejeição da palma, ideal para colher assinaturas nos formulários do sistema de fiscalização.",
         "A S Pen é incluída e permite assinaturas e anotações em aplicativos compatíveis. A validade legal depende do sistema e da norma do órgão."),
        ("Sim, o Active5 foi desenvolvido para permitir limpeza com desinfetantes e soluções alcoólicas sem degradar o display ou a carcaça.",
         "O Active5 pode ser limpo com desinfetantes, conforme as orientações do fabricante."),
        ("A bateria aguenta um turno completo de 8 a 12 horas?", "Como planejar a bateria para um turno completo?"),
        ("Sim, a bateria de 5.050 mAh suporta a jornada de trabalho e pode ser trocada rapidamente em campo (bateria removível) sem precisar desligar o processo de trabalho.",
         "A bateria removível de 5.050 mAh permite planejar a troca em campo. A autonomia depende do uso, da rede e dos aplicativos, então valide em um teste piloto."),
        ("Sim, o chip GNSS integrado opera com GPS, Glonass, Galileo e BeiDou de forma autônoma para registro de geolocalização.",
         "A localização por GPS pode funcionar sem sinal de dados, mas mapas e sistemas online dependem de conexão. Valide o modo offline no aplicativo usado."),
    ])

os.makedirs(DST, exist_ok=True)
falhas = 0
for slug, cfg in P.items():
    h = open(f"{SRC}/{slug}.html", encoding="utf-8").read()
    for a, b in cfg["trocas"]:
        if a not in h:
            print(f"[{slug}] NÃO ENCONTRADO: {a[:70]}..."); falhas += 1; continue
        h = h.replace(a, b)
    h = re.sub(r'<section id="beneficios">.*?</section>', lambda m: cfg["ben"], h, count=1, flags=re.S)
    h = re.sub(r'<nav class="related".*?</nav>', lambda m: NAV, h, count=1, flags=re.S)
    h = re.sub(r'(<a class="btn"\s+href="#orcamento">.*?</a>)', lambda m: m.group(1) + WA_BTN, h, flags=re.S)
    bc = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
          '{"@type":"ListItem","position":1,"name":"MGD Distribuição","item":"https://mgd-dist.com.br/"},'
          '{"@type":"ListItem","position":2,"name":"Samsung Galaxy Tab Active5 5G","item":"https://mgd-dist.com.br/produtos/active5/"},'
          f'{{"@type":"ListItem","position":3,"name":"{cfg["crumb"]}","item":"https://mgd-dist.com.br/{slug}/"}}]}}')
    h = h.replace("<!-- /wp:html -->", f'<script type="application/ld+json">{bc}</script>\n<!-- /wp:html -->')
    open(f"{DST}/{slug}.html", "w", encoding="utf-8").write(h)
print("arquivos gerados:", len(P), "| trocas não encontradas:", falhas)
sys.exit(1 if falhas else 0)
