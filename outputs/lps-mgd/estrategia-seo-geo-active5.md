# Active5 (MGD): abrangência de SEO + GEO

Base: Keyword Stats do Planejador (Set/2025 a Ago/2026, 690 termos). Dados da matriz: `matriz-100-lps.csv`.

## 1. O que os dados mostram

**Demanda B2B real (filtrada do arquivo):**

| Termo | Buscas/mês | Lance topo (R$) | Uso |
|---|---:|---|---|
| tablet robusto | 500 | 0,37–5,50 | Hub principal |
| tablet para empresa | 500 | 3,00–11,64 | Hub comercial (maior intenção) |
| tablet samsung para trabalho | 500 | 0,29–1,18 | Hub |
| tablet profissional para trabalho | 500 | 0,31–2,61 | Hub |
| tablet bom para trabalho | 500 | 0,31–1,71 | Hub |
| tablet empresarial | 50 | 2,61–9,33 | Consolidar em "para empresa" |
| tablet para uso industrial | 50 | 2,69–10,32 | Manufatura |
| tablet para industria | 50 | 2,87–9,46 | Manufatura |
| tablet samsung para empresas | 50 | 0,96–12,84 | Hub |
| tablet para uso empresarial | 50 | 2,08–5,71 | Hub |
| tablet empresa | 50 | 3,29–6,36 | Hub |
| tablet para campo | 50 | 1,43–4,41 | Serviços / Leitura de dados em campo |
| tablet resistente à impacto | 50 | n/d | Hub resistência |
| tablet para fiscalização municipal | <10 | n/d | Governo |

**Três conclusões:**

1. **Os segmentos verticais quase não têm volume medido.** Logística, mineração, saúde, utilities e governo aparecem com 0 a 10 buscas/mês. O arquivo só cobre variações de "tablet para…". Essas LPs não valem por volume. Valem por intenção altíssima e por serem a resposta que a IA cita (ver seção 3).
2. **Armadilha: "leitura".** "tablet para leitura" (5.000/mês) é e-reader e ebook, tráfego errado. O pilar "Leitura de dados externo" deve falar de **coleta de dados em campo**, **leitura de medidores** e **leitura de código de barras/RFID**. Nunca use "tablet para leitura" sozinho em title, H1 ou anchor.
3. **A intenção B2B custa mais.** Os lances são de R$ 9 a R$ 13 nos termos de empresa e indústria, contra R$ 0,30 a R$ 0,50 nos consumer. Isso indica lead de valor, e o orgânico economiza mídia.

**Negativar no Google Ads e evitar no conteúdo:** leitura (ebook/pdf), estudar, desenho, jogos, barato, criança, iPad, Xiaomi.

## 2. Arquitetura SEO (9 pilares → 83 LPs (após consolidar canibalização, seção 7))

Página principal: Samsung Galaxy Tab Active5 5G. Cada pilar liga de volta a ela, e cada LP filha tem canonical próprio e liga ao seu pilar.

| Pilar | Slug | Termo-âncora | Filhas (da matriz) |
|---|---|---|---|
| Hub geral | tablet-robusto-active5 | tablet robusto / para empresa | 20 |
| Governo | ...-governo | tablet para fiscalização / prefeitura | 14 |
| Logística | ...-logistica | tablet para logística / estoque | 14 |
| Manufatura | ...-manufatura | tablet para indústria / chão de fábrica | 14 |
| Mineração | ...-mineracao | tablet para mineração | 10 |
| Saúde | ...-saude | tablet para hospital | 10 |
| Serviços | ...-servicos | tablet para trabalho em campo | 10 |
| Utilities | ...-utilities | tablet para leitura de medidores / setor elétrico | 8 |
| Bens de consumo | ...-bens-de-consumo | tablet para PDV / merchandising / reposição | a criar (hoje 0 na matriz) |
| Leitura de dados externo | ...-coleta-de-dados-campo | tablet para coleta de dados em campo / leitura de medidores | a criar |

Pendências: **Bens de consumo** e **Leitura de dados externo** não têm filhas na matriz. Sugestão de long-tails:
- Bens de consumo: tablet para promotor de vendas, tablet para merchandising, tablet para reposição em PDV, tablet para equipe de vendas externa, tablet para pesquisa de preços.
- Leitura de dados: tablet para coleta de dados em campo, tablet para leitura de medidores, tablet com leitor de código de barras, tablet para formulário offline, tablet para levantamento em campo.

## 3. GEO (citação em ChatGPT, Gemini, Perplexity, AI Overviews)

A IA cita páginas que respondem de forma direta, com dados verificáveis. Em cada LP:

1. **Resposta em 40 a 60 palavras no topo** (primeiro parágrafo após o H1): "O Galaxy Tab Active5 é um tablet robusto IP68 e MIL-STD-810H, com 5G e bateria removível, indicado para [segmento] porque…".
2. **Ficha técnica em tabela HTML**, com números conferidos no site da Samsung: IP68, MIL-STD-810H, 5G, bateria removível, uso com luvas e caneta S Pen. Não invente números.
3. **FAQ com 4 a 6 perguntas reais** ("Tablet comum serve para fiscalização?", "Qual a diferença entre tablet robusto e tablet comum?") com schema `FAQPage`.
4. **Schema:** `Product` (Active5), `Organization` (MGD), `BreadcrumbList`, `FAQPage`. Entidade consistente: sempre "Samsung Galaxy Tab Active5" + "MGD".
5. **EEAT:** caso de uso ou cliente real por segmento, autor/responsável, CNPJ e telefone, data de atualização visível.
6. **Comparativo** "tablet robusto x tablet comum" e "Active5 x Active4 Pro" (a IA cita muito esse formato).
7. **Conteúdo citável fora do site:** perfil Google Business, LinkedIn da MGD e menções em portais do setor.
8. Liberar `GPTBot`, `PerplexityBot` e `Google-Extended` no robots.txt, se não estiver liberado.

## 4. SEO técnico (causa do "alternativa com canonical")

- Canonical **self-referencing** em todas as LPs (plugin de SEO e template "Elementor largura total").
- Sitemap com as LPs publicadas. Linkagem interna: página principal → 9 pilares → filhas, com anchors descritivas.
- Title ≤ 60 caracteres. Hoje 14 passam disso na matriz.
- Conteúdo único por LP: dor, cenário de uso, FAQ e imagem próprios.

## 5. Ordem de execução

| Quando | Ação | Resultado |
|---|---|---|
| Semana 1 | Corrigir canonical, publicar os 9 pilares, negativar "leitura/estudo/desenho" no Ads | Destrava indexação e economiza mídia |
| Semana 2 | Publicar 15 LPs: hub geral + termos de empresa, indústria e campo | Pega o pouco volume real e de maior lance |
| Semana 3 a 4 | FAQ + schema + comparativos (GEO), e as LPs de Bens de consumo e Leitura de dados | Entra nas respostas de IA |
| Depois | As demais filhas, em ondas de 20 | Cobertura total |

**Riscos:** volume baixo nos verticais (não prometa tráfego, prometa leads qualificados); conteúdo fino ou duplicado em escala; afirmações técnicas sem conferência. Meça por leads via WhatsApp, menções em IA (teste mensal com 20 perguntas) e impressões no Search Console, não por cliques.

## 6. "As pessoas também perguntam" (PAA)

Perguntas coletadas no Google, classificadas por aderência ao Active5.

| Pergunta | Usar? | Onde |
|---|---|---|
| Qual o melhor tablet para uso corporativo? | **Sim, prioridade 1** | FAQ do hub "tablet para empresa" e do pilar Geral |
| Qual tablet é resistente para uso no trabalho? | **Sim, prioridade 1** | FAQ do hub "tablet robusto" e de todas as LPs |
| Qual tablet é bom para trabalhar com planilhas? | Sim, com ressalva | FAQ de Serviços, Logística e Bens de consumo (formulários, conferência, relatórios) |
| Qual tablet substitui um notebook? | Parcial | Seção "Active5 x notebook em campo": substitui o notebook em rota e em vistoria, não no escritório |
| Como acessar um HD externo no tablet? | Não | Intenção informacional e consumer. Não gera lead |
| Qual o melhor tablet específico para leitura? | Não | E-reader. Fora do público B2B |
| Como se chama o tablet de leitura? | Não | Idem |

### Respostas-modelo (formato GEO: direta, 40 a 60 palavras)

Conferir cada dado técnico no site da Samsung antes de publicar.

- **Melhor tablet para uso corporativo?** Para equipes que trabalham fora do escritório, o melhor é um tablet robusto, como o Samsung Galaxy Tab Active5: tem certificação IP68 e MIL-STD-810H, suporta 5G e bateria removível. Para uso só em escritório, um tablet comum atende.
- **Tablet resistente para o trabalho?** O Galaxy Tab Active5 resiste a água, poeira e quedas (IP68 e MIL-STD-810H) e funciona com luvas. É indicado para logística, indústria, mineração, saúde, serviços e campo.
- **Tablet bom para planilhas?** Para preencher formulários e consultar sistemas em campo, o Active5 atende: tela sensível com luvas e S Pen incluída. Para planilhas pesadas, o notebook no escritório continua mais indicado. (Não afirmar compatibilidade com Excel nem teclado: não consta na página do produto.)
- **Tablet que substitui notebook?** Em rotas de entrega, vistorias e fiscalização, o tablet robusto substitui o notebook: é mais leve, liga rápido e aguenta o uso externo. Para edição pesada, o notebook continua necessário.

### Como usar

1. Coloque as 4 perguntas "Sim" em FAQ com schema `FAQPage` em todas as LPs, variando a resposta pelo segmento.
2. Crie um post de blog "Tablet robusto x tablet comum: qual escolher para a empresa" que responda as 4 e ligue ao hub.
3. Não escreva conteúdo para as 3 perguntas de HD externo e leitura.

## 7. Unicidade: sem canibalização e sem duplicidade

### Canibalização (duas URLs disputando a mesma busca)
Auditei a matriz: 17 pares tinham a mesma intenção e mudavam só o adjetivo (*robusto / industrial / resistente / samsung*). O Google trata como a mesma busca e rankeia só uma. Por exemplo, "tablet para mineração", "tablet robusto para mineração", "tablet industrial para mineração" e "tablet resistente para mineração".

**Regra adotada:** uma intenção = uma URL. As variantes viram **palavras secundárias** da URL principal (aparecem em H2, FAQ e texto), não ganham página própria. A matriz foi regenerada:
- **83 LPs únicas** (antes 96) e 17 linhas marcadas CONSOLIDAR.
- Nova coluna `kw_secundarias` com as variantes que cada página deve cobrir.
- Cada palavra principal aponta para **uma só URL**. Não repita a palavra principal de outra LP no title, H1 ou H2.

As 13 vagas liberadas devem ir para intenções realmente diferentes (Bens de consumo e Leitura de dados em campo, seção 2).

### Duplicidade (texto igual com uma palavra trocada)
Trocar "logística" por "mineração" no mesmo molde é duplicidade. Cada LP precisa destes 6 elementos **únicos**:

1. **Persona e cenário real.** Ex.: "conferente no CD com luvas às 5h" ≠ "fiscal de posturas sob chuva".
2. **Problema específico da atividade**, não do segmento.
3. **Requisito do Active5 priorizado para aquele caso.** Ex.: luva e bateria removível (logística), IP68 (saneamento), higienização (saúde).
4. **Fluxo de trabalho de ponta a ponta:** o que o usuário faz no tablet, passo a passo.
5. **FAQ próprio**, com 4 a 6 perguntas, das quais no máximo 2 podem ser compartilhadas com outras LPs.
6. **Title, H1, meta description e slug exclusivos.** A ficha técnica e o rodapé comercial podem se repetir, mas ficam abaixo de 30% do texto.

### Trava antes de publicar
`verificar_unicidade.py <pasta-com-html>` barra a publicação se houver:
- title, H1 ou meta description repetidos ou vazios;
- canonical que não aponta para a própria página (causa do status "alternativa com canonical adequada");
- menos de 600 palavras ou title com mais de 60 caracteres;
- pergunta de FAQ repetida em mais de 2 páginas;
- similaridade de texto acima de 30% entre qualquer par de LPs (shingles de 5 palavras).

Fluxo: gerar HTML → rodar o verificador → só publicar em rascunho quando sair sem problemas. Testei o verificador com páginas de exemplo e ele pegou uma cópia com 97% de similaridade.

## 8. Modelo "mesmo produto, situação diferente"

O produto é um só: [Active5 5G](https://mgd-dist.com.br/produtos/active5/). O que muda em cada LP é a **situação de uso**. Isso define a estrutura:

| Elemento | Regra |
|---|---|
| Canonical | A própria LP. A página do produto mantém o canonical dela. |
| Palavra-chave | Só a situação ("tablet para controle de estoque"). **Nenhuma LP disputa o termo de marca** ("tablet robusto samsung galaxy tab active 5 5g"), que fica para a página do produto. |
| H1 | A situação, não o produto. Ex.: "Tablet para conferência de mercadorias no armazém". |
| Produto | Aparece como solução, em um bloco que leva à página do produto (CTA "Ver a página principal do Active5 5G"). |
| Especificações | Só as **verificadas** em `fatos_active5.json` (conferidas na página do produto), com o destaque que a situação pede. |
| Diferenciação | Persona, cenário, problema, fluxo de trabalho e FAQ da situação (seção 7). |

Consequência: a variação entre as LPs é de **situação**, e os fatos do produto ficam constantes. Por isso a ficha técnica se repete, mas deve ficar abaixo de 30% do texto para passar no verificador. O diferencial de cada LP precisa ser o cenário.

**Fatos que não constam na página e não devem ser afirmados:** Excel/Office, teclado acessório, leitor de código de barras integrado, autonomia em horas, peso, tamanho de tela e preço. Se quiser usá-los, confirme com a Samsung ou a equipe da MGD primeiro.

## 9. Modelo oficial: LP de Logística

Li a [LP de Logística](https://mgd-dist.com.br/tablet-robusto-active5-logistica/) publicada e salvei o bloco de conteúdo em `modelo-logistica.html` (CSS `.mgd-lp`, 14 seções, 2 JSON-LD, ~2.100 palavras, 7 FAQs). O `index.html` local não está acessível daqui; usei a versão publicada. Se o `index.html` for diferente, me envie.

### Estrutura (todas as categorias seguem)
| # | Bloco | Muda por categoria? |
|---|---|---|
| 1 | Hero: H1 "Melhor Tablet para {situação}: Samsung Galaxy Tab Active5 5G" + CTAs | H1, subtítulo, bullets |
| 2 | Formulário HubSpot (`#orcamento`) + WhatsApp | Só a mensagem do WhatsApp |
| 3 | Critérios do melhor tablet para {situação} (6 cards `h3`) | **Sim, totalmente** |
| 4 | Aplicações (6 cards: recebimento, separação, inventário…) | **Sim, totalmente** |
| 5 | Recursos e ficha técnica | Ficha fixa, destaque por situação |
| 6 | "Por que o tablet robusto é indispensável…" (3 `h3`) | **Sim, totalmente** |
| 7 | Benefícios da operação (6 `h3`: doca, empilhadeira, turnos, chuva/EPI, Knox) | **Sim, totalmente** |
| 8 | Como funciona (4 passos) | Texto adaptado |
| 9 | FAQ (7 perguntas) + `FAQPage` | **Sim, 5 das 7 únicas** |
| 10 | Links para produto e outros segmentos | Lista de segmentos irmãos |
| 11 | CTA final | Situação no texto |
| - | JSON-LD: `BreadcrumbList`, `Product`, `Organization`, `FAQPage` | URLs e FAQ |

Os blocos 3, 4, 6, 7 e 9 concentram o conteúdo único. É onde o verificador de duplicidade deve atuar.

### Pontos de atenção no modelo (conferir antes de replicar 83 vezes)
1. **Afirmações que não constam na página do produto:** "Tela de 8”", "Wi-Fi 6", "Leitura 1D/2D e Assinatura Digital", "Samsung Knox", "Integração WMS/ERP e Menor TCO", "Modo Sem Bateria", "Wet Touch". Confirme com a Samsung ou a equipe da MGD, porque serão repetidas em todas as LPs. Em especial: o FAQ pergunta se o Active5 "substitui um coletor de dados com leitor de código de barras". A resposta precisa ser honesta sobre como a leitura é feita (câmera ou acessório), para não gerar reclamação de cliente.
2. **Palavra-chave:** o H1 do modelo começa com "Melhor Tablet para Logística", que pode ter intenção de comparação ("melhor"). Mantenha, mas o title "Tablet robusto Active5 para logística | MGD" repete o termo de marca do produto. Nas novas LPs o title deve ser a situação: "Tablet para controle de estoque | Samsung Galaxy Tab Active5 | MGD".
3. **Canonical:** o modelo já tem canonical próprio (`/tablet-robusto-active5-logistica/`), ok. Como as 8 LPs originais também são pilares, as filhas devem ligar ao pilar e ao produto.
4. **Slug do modelo** (`tablet-robusto-active5-logistica`) difere do padrão da matriz (`tablet-para-logistica`). Decisão: manter os 9 slugs dos pilares como estão e usar o padrão da matriz nas filhas.

### Próximo passo
Gerar cada LP a partir do `modelo-logistica.html`, mantendo CSS e blocos fixos e reescrevendo os blocos 3, 4, 6, 7 e 9 por situação, com `verificar_unicidade.py` como trava.
