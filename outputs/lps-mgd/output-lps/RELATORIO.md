# Revisão das 5 LPs de amostra (output-lps)

Arquivos: `tablet-industrial-samsung`, `tablet-para-agentes-de-transito`, `tablet-para-controle-de-estoque`,
`tablet-para-equipe-de-campo`, `tablet-para-fiscalizacao`. Originais em `output-lps/`, corrigidos em `output-lps/ajustados/`
(gerados por `ajustar_lps.py`, repetível).

## Resultado do verificador (`verificar_unicidade.py`)
| | Antes | Depois |
|---|---|---|
| Problemas | 20 | 0 |
| Avisos | 46 | 7 (todos dependem do WordPress) |

## O que estava fora do modelo e foi corrigido
1. **Vazamento de rótulo** em `tablet-industrial-samsung`: "Pilar Corporativo" aparecia no breadcrumb, nos H2 e no CTA.
2. **Sem WhatsApp** nas 5 páginas. Incluído botão no hero e no CTA final com a mensagem
   "Olá, vim pelo site MGD e gostaria de orçamento de Samsung Galaxy Tab Active5 5G." (número 5511986350609).
3. **Links internos quebrados:** a navegação apontava para `/tablet-para-industria/`, `/tablet-para-mineracao/`,
   `/tablet-para-hospital/` etc., que não são os slugs dos pilares. Agora aponta para os 8 pilares reais
   (`/tablet-robusto-active5-{segmento}/`).
4. **Bloco "Benefícios" idêntico** nas 5 (só mudava uma palavra). Reescrito por situação.
5. **Afirmações sem base na página do produto**, trocadas por texto verificável ou por "confirmado na proposta":
   Samsung Knox / Knox Manage, "tela antirreflexo", "queda de até 1,8 m", "hot-swap", "100% compatível com SAP/Totvs",
   "assinatura com validade legal", GNSS (GPS/Glonass/Galileo/BeiDou), S Pen "EMR", "5G ultrarrápido", PTT, multi-slot cradle,
   "tela legível sob sol", "8 a 12 horas de bateria", "leitura de códigos 1D/2D com inteligência em baixa luz".
6. **Kit na caixa contraditório:** uma LP dizia que a capa vem na caixa e outra listava itens que a página do produto não confirma.
   Agora: "a composição do kit é confirmada na proposta".
7. **Schema:** só havia `FAQPage`. Adicionado `BreadcrumbList`.

## Pendências que dependem de você
- **Title, meta description e canonical** não estão nos arquivos. Defina no plugin de SEO de cada página (valores em
  `matriz-100-lps.csv`, coluna `title_seo`) e confirme que o canonical aponta para a própria URL.
- **Conteúdo curto:** cerca de 900 palavras úteis por LP, contra ~2.100 do modelo de Logística. Falta texto em critérios,
  "por que é indispensável" e benefícios do modelo. Recomendo ampliar antes de publicar as 83.
- **Canibalização dentro da amostra:** `tablet-para-fiscalizacao` cobre ambiental, sanitária, obras, transporte e fazendária,
  e concorre com "fiscalização em campo", "fiscalização municipal" e "agente de fiscalização". Mantenha uma só página para essas
  3 buscas ou separe cada uma por atividade específica. Mesmo caso para controle de estoque × gestão de estoque × inventário, e
  equipe de campo × serviço de campo × técnico de campo.
- **Pilares em rascunho:** os links do menu "Outros segmentos" dão 404 até os 8 pilares serem publicados.
- **Formulário:** estas LPs usam iframe do HubSpot (`share.hsforms.com`); o modelo de Logística usa o script `hbspt.forms.create`.
  Padronize em um dos dois para o rastreamento funcionar igual.
- **Dados a confirmar:** tela de 8,0", 1920×1200, octa-core, 128 GB e código SM-X306BZGAL05 (não constam na página do produto).
