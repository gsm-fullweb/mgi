# Comparação SEO — Mogi das Cruzes x Cotia

Data da análise: 2026-08-03

## A) Resumo da auditoria

Escopo: comparação de duas páginas locais de aluguel de impressoras no site mgi.com.br, cobrindo SEO on-page, conteúdo local, links, dados estruturados, imagens, compartilhamento social e sinais de desempenho.

URLs:

- https://mgi.com.br/aluguel-de-impressoras/mogi-das-cruzes/
- https://mgi.com.br/aluguel-de-impressoras/cotia/

### Veredito

**Cotia está tecnicamente mais limpa; Mogi tem o conteúdo local mais convincente.**

- **Mogi das Cruzes:** melhor diferenciação geográfica, prova de presença física, suporte local, mais conteúdo e narrativa mais confiável. Perde força por 11 links internos quebrados, meta description excessiva e imagens/links reaproveitados de outras localidades.
- **Cotia:** melhor meta description, links internos saudáveis e segmentação clara para logística/indústria. Perde força por reutilizar grande parte do template, conter imagens/alt texts de Mogi/Alto Tietê e declarar `LocalBusiness` em Cotia sem evidência de uma unidade física completa.

### Pontuação comparativa

| Área | Mogi das Cruzes | Cotia | Vencedora |
|---|---:|---:|---|
| Relevância e prova local | Forte | Boa | Mogi |
| Metadados | Regular | Boa | Cotia |
| Estrutura de headings | Boa | Boa | Empate |
| Conteúdo e profundidade | Forte | Boa | Mogi |
| Links internos | Crítica | Boa | Cotia |
| Schema | Boa com ressalvas | Regular com risco local | Mogi |
| Imagens/localização | Regular | Fraca | Mogi |
| Open Graph/Twitter | Fraca | Fraca | Empate |
| Desempenho móvel | Não medido | Não medido | Indeterminado |

Pontuação numérica geral não foi atribuída porque o PageSpeed Insights respondeu com limite de API e não forneceu métricas de laboratório ou campo. A avaliação comparativa acima usa somente evidências confirmadas.

## Evidências principais

### On-page

| Elemento | Mogi das Cruzes | Cotia |
|---|---|---|
| HTTP | 200 | 200 |
| Title | 47 caracteres; adequado | 37 caracteres; adequado, porém curto |
| Meta description | 227 caracteres; tende a truncar | 148 caracteres; dentro da faixa recomendada |
| H1 | Único e alinhado à busca local | Único e alinhado à busca local |
| Canonical | Autorreferente e correto | Autorreferente e correto |
| Robots | Não há `noindex`; `max-image-preview:large` | Não há `noindex`; `max-image-preview:large` |
| Palavras detectadas | 1.173 | 1.039 |
| Open Graph | Ausente | Ausente |
| Twitter Card | Ausente | Ausente |

### Conteúdo local

Mogi contém sinais locais fortes e específicos: sede na Av. João XXIII, bairro Socorro, comércio no centro, indústrias em Brás Cubas e atuação no Alto Tietê. Isso demonstra presença e experiência real, reduzindo o risco de a página parecer apenas uma troca programática de cidade.

Cotia possui boa adaptação ao perfil econômico local, citando polos logísticos, Raposo Tavares, e-commerce, distribuidoras, etiquetas, romaneios e documentação de carga. Porém, os dois parágrafos mais locais aparecem depois do FAQ, perto do fim da página. Eles deveriam aparecer antes das seções genéricas para diferenciar a página mais cedo.

As duas páginas repetem blocos extensos: soluções, modelos, impressoras térmicas, setores, benefícios, processo e texto institucional. O conteúdo local existente é suficiente para gerar valor, mas precisa ser distribuído ao longo da página e acompanhado por provas locais distintas.

### Links internos

- **Mogi:** 11 destinos internos retornaram 404. Todos usam a estrutura antiga `/outsourcing/aluguel-de-impressoras-em-{cidade}/`.
- **Cotia:** 7 links saudáveis, 0 quebrados e 2 redirecionados. A estrutura atual `/aluguel-de-impressoras/{cidade}/` está consistente.

Os 404 de Mogi prejudicam experiência, distribuição de autoridade interna e rastreamento. É o maior problema da comparação.

### Dados estruturados

Ambas possuem `Service`, `BreadcrumbList`, `LocalBusiness` e `FAQPage` em JSON-LD.

- `Service` e `BreadcrumbList` estão bem contextualizados por cidade.
- `FAQPage` não deve ser tratado como oportunidade de rich result para este negócio comercial; a elegibilidade do Google é restrita. O conteúdo FAQ pode continuar visível, mas o markup deve ser removido ou mantido sem expectativa de resultado enriquecido.
- Em Mogi, `LocalBusiness` é coerente com a alegação de sede local.
- Em Cotia, o `LocalBusiness` usa localidade e coordenadas de Cotia, mas o conteúdo analisado não comprova endereço físico completo nessa cidade. Se não houver filial real, usar a organização principal como `provider` dentro de `Service` e manter `areaServed: Cotia`; não representar uma unidade local inexistente.

### Imagens

- Diversas imagens não possuem `width` e `height`, criando risco de deslocamento de layout.
- Cotia reutiliza alt texts como “Aluguel de impressora multifuncional em Mogi das Cruzes”, “Alto Tietê” e “Suzano e Mogi”. Isso enfraquece a coerência local e evidencia reaproveitamento do template.
- Mogi também possui imagens genéricas e algumas sem dimensões, mas seus alt texts são mais coerentes com a página.
- O pixel de Facebook sem alt é decorativo/técnico e não é uma falha de acessibilidade relevante.

### Legibilidade

O script registrou 924 palavras úteis para Mogi e 861 para Cotia, com frases médias de 15,9 e 17,2 palavras. O índice Flesch do script foi desenhado para inglês e, portanto, não deve ser usado como nota confiável para português. Como sinal direcional, Cotia tem frases ligeiramente mais longas e mais vocabulário técnico; recomenda-se simplificar trechos sobre logística, outsourcing e equipamentos.

### Desempenho

O PageSpeed Insights bloqueou ambas as medições por limite de API. Não há evidência suficiente para comparar LCP, INP, CLS ou nota de desempenho. Pela inspeção do HTML, muitas imagens sem dimensões são um risco provável de CLS, mas não uma falha medida.

## B) Tabela de achados

| Área | Severidade | Confiança | Achado | Evidência | Correção |
|---|---|---|---|---|---|
| Links internos — Mogi | Critical | Confirmed | 11 links internos retornam 404 | URLs antigas sob `/outsourcing/aluguel-de-impressoras-em-*` | Atualizar para a estrutura atual ou criar redirects 301 |
| Conteúdo local — Cotia | Warning | Confirmed | Alt texts citam Mogi, Suzano e Alto Tietê | Imagens de produtos carregam descrições de outras localidades | Reescrever alts conforme a imagem e o contexto de Cotia |
| Schema — Cotia | Warning | Confirmed | `LocalBusiness` representa uma unidade em Cotia sem endereço completo comprovado | JSON-LD contém localidade e coordenadas de Cotia | Se não houver filial, remover o `LocalBusiness` local e usar `Service.areaServed` |
| Metadados — Mogi | Warning | Confirmed | Meta description excessiva | 227 caracteres | Reduzir para aproximadamente 145–160 caracteres |
| Social | Warning | Confirmed | Open Graph e Twitter Cards ausentes nas duas páginas | 0/7 OG e 0/6 Twitter nos testes | Adicionar título, descrição, URL, tipo e imagem social |
| Imagens | Warning | Confirmed | Muitas imagens não declaram dimensões | Parser encontrou `width`/`height` nulos | Definir dimensões e manter lazy loading abaixo da dobra |
| Conteúdo programático | Warning | Confirmed | Grandes blocos são compartilhados entre as páginas | Estruturas e textos de soluções, setores e processo são quase idênticos | Distribuir exemplos, SLAs, provas e casos locais em cada seção |
| FAQ schema | Info | Confirmed | `FAQPage` está presente, mas é restrito para rich results comerciais | JSON-LD detectado nas duas páginas | Manter FAQ visível; remover markup se não houver outra finalidade |
| Indexabilidade | Pass | Confirmed | Canonical e robots permitem indexação | Canonical autorreferente; nenhum `noindex` | Manter |
| H1/estrutura | Pass | Confirmed | Cada página possui um único H1 e hierarquia H2/H3 organizada | Parser HTML | Manter |

## C) Plano priorizado resumido

1. Corrigir os 11 links quebrados de Mogi.
2. Remover referências a Mogi/Alto Tietê/Suzano das imagens de Cotia.
3. Confirmar se existe filial física em Cotia e ajustar o `LocalBusiness`.
4. Encurtar a meta description de Mogi.
5. Adicionar Open Graph e Twitter Card às duas páginas.
6. Tornar os blocos genéricos mais locais e únicos.
7. Definir dimensões das imagens e medir CWV quando a API estiver disponível.

## D) Desconhecidos e próximos testes

- Core Web Vitals e nota Lighthouse: indisponíveis por rate limit do PageSpeed.
- Rankings, impressões, CTR e conversões: exigem Google Search Console e Analytics.
- Existência de unidade física/Google Business Profile em Cotia: precisa de confirmação interna.
- Percentual exato de duplicação entre todas as páginas locais: exige crawl completo do diretório.
