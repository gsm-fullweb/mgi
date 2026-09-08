# Plano de ação SEO — páginas locais de aluguel de impressoras

Data: 2026-08-03

## 1. Imediato — corrigir Mogi das Cruzes

**Impacto: alto | Esforço: baixo | Tipo: quick win**

Substituir os 11 links da seção de cidades, que hoje apontam para URLs antigas sob `/outsourcing/aluguel-de-impressoras-em-*`, pelas páginas atuais em `/aluguel-de-impressoras/{cidade}/`. Se alguma página atual ainda não existir, remover o link ou criar a página antes de vinculá-la. Criar redirects 301 das URLs antigas quando houver equivalência.

Validar após a correção com novo teste de links e confirmar zero respostas 404.

## 2. Imediato — corrigir coerência local de Cotia

**Impacto: alto | Esforço: baixo | Tipo: quick win**

Reescrever alt texts que mencionam Mogi das Cruzes, Alto Tietê e Suzano. O alt deve descrever a imagem; incluir Cotia apenas quando isso for verdadeiro e natural.

Mover os parágrafos sobre Raposo Tavares, galpões, e-commerce, romaneios e expedição para antes da seção de soluções ou integrá-los ao hero. Isso diferencia a página antes dos blocos compartilhados.

## 3. Imediato — validar schema local de Cotia

**Impacto: alto | Esforço: baixo | Tipo: quick win**

Confirmar se a MGI possui filial física real, endereço verificável e presença empresarial em Cotia.

- Se sim: completar `PostalAddress`, manter coordenadas reais e alinhar com o Google Business Profile.
- Se não: remover o `LocalBusiness` específico de Cotia. Manter `Service` com `provider` apontando para a organização MGI e `areaServed` apontando para Cotia.

## 4. Metadados

**Impacto: médio | Esforço: baixo | Tipo: quick win**

Meta recomendada para Mogi:

> Aluguel de impressoras em Mogi das Cruzes com manutenção, toner e suporte técnico local. Solicite uma proposta sob medida para sua empresa.

Adicionar às duas páginas:

- `og:title`
- `og:description`
- `og:image`
- `og:url`
- `og:type=website`
- `og:locale=pt_BR`
- `twitter:card=summary_large_image`

## 5. Conteúdo local único

**Impacto: alto | Esforço: médio | Tipo: estratégico**

Para Mogi, reforçar:

- sede, endereço e equipe própria;
- SLA real de atendimento;
- Brás Cubas, centro, universidades, clínicas e indústrias;
- depoimento/case verificável do Alto Tietê.

Para Cotia, reforçar:

- Raposo Tavares e polos logísticos;
- cenários de etiquetas, romaneios e expedição;
- SLA e logística de atendimento desde a base real da MGI;
- case ou depoimento verificável de cliente da região.

Evitar apenas trocar nomes de cidades. Cada seção compartilhada deve receber pelo menos um exemplo, prova ou detalhe operacional local.

## 6. Imagens e estabilidade visual

**Impacto: médio | Esforço: médio | Tipo: manutenção**

- Definir `width` e `height` para todas as imagens.
- Usar WebP/AVIF quando possível.
- Aplicar `loading=lazy` abaixo da dobra.
- Criar ao menos uma imagem social 1200×630 específica para cada localidade.
- Não usar alt text para inserir palavras-chave que não descrevem a imagem.

## 7. Schema e FAQ

**Impacto: médio | Esforço: baixo | Tipo: manutenção**

Manter `Service` e `BreadcrumbList`. Manter as perguntas visíveis para usuários, mas remover `FAQPage` se o objetivo for somente rich result, pois o tipo não oferece elegibilidade normal para uma empresa comercial.

## 8. Medição e validação

**Impacto: alto | Esforço: médio | Tipo: estratégico**

Após as correções:

1. executar novo broken-link check;
2. validar JSON-LD;
3. medir Lighthouse móvel para LCP, INP e CLS;
4. acompanhar no Search Console as consultas por cidade, impressões, CTR e posição;
5. comparar conversões de orçamento/WhatsApp por página durante 30–60 dias.
