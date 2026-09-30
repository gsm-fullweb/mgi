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

## 2. Arquitetura SEO (9 pilares → 96 LPs)

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
