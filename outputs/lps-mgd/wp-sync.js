#!/usr/bin/env node
/**
 * Envia as LPs do Active5 para o WordPress como RASCUNHO, em lotes por categoria.
 *
 * Uso (na sua máquina, nunca compartilhe a senha):
 *   set WP_URL=https://mgd-dist.com.br
 *   set WP_USER=seu_usuario
 *   set WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx     (Usuários > Perfil > Senhas de Aplicativo)
 *   node wp-sync.js --dir "C:\Users\Richard Wagner\Documents\MGD\output-lps" --dry-run
 *   node wp-sync.js --dir "...\output-lps" --categoria Logística --lote 20
 *   node wp-sync.js --dir "...\output-lps" --todas --lote 20     (uma categoria por vez, lotes de 20)
 *
 * Cada arquivo deve se chamar <slug>.html. Progresso em sync-state.json (retoma de onde parou).
 * Opções: --status draft|publish (padrão draft), --template <slug do template>, --matriz <json>.
 */
const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf("--" + n); return i < 0 ? d : (args[i + 1] && !args[i + 1].startsWith("--") ? args[i + 1] : true); };
const DIR = opt("dir", "output-lps");
const MATRIZ = opt("matriz", path.join(__dirname, "matriz-100-lps.json"));
const LOTE = parseInt(opt("lote", "20"), 10);
const STATUS = opt("status", "draft");
const TEMPLATE = opt("template", "");
const DRY = !!opt("dry-run", false);
const CAT = opt("categoria", "");
const TODAS = !!opt("todas", false);
const STATE = path.join(__dirname, "sync-state.json");
const { WP_URL, WP_USER, WP_APP_PASSWORD } = process.env;

// Pilares já existentes no WordPress (IDs do levantamento); são atualizados por slug.
const PILARES = {
  "Logística": "tablet-robusto-active5-logistica", "Manufatura": "tablet-robusto-active5-manufatura",
  "Mineração": "tablet-robusto-active5-mineracao", "Saúde": "tablet-robusto-active5-saude",
  "Governo": "tablet-robusto-active5-governo", "Serviços": "tablet-robusto-active5-servicos",
  "Utilities": "tablet-robusto-active5-utilities", "Bens de consumo": "tablet-robusto-active5-bens-de-consumo",
  "Geral (hub)": "tablet-robusto-active5",
};

const rows = JSON.parse(fs.readFileSync(MATRIZ, "utf8")).filter(r => r.acao.startsWith("CRIAR"));
const itens = [];
for (const [seg, slug] of Object.entries(PILARES))
  itens.push({ segmento: seg, slug, titulo: null, pilar: true });
for (const r of rows)
  if (!Object.values(PILARES).includes(r.slug))
    itens.push({ segmento: r.segmento, slug: r.slug, titulo: r.title_seo, pilar: false });

const state = fs.existsSync(STATE) ? JSON.parse(fs.readFileSync(STATE, "utf8")) : {};
const save = () => fs.writeFileSync(STATE, JSON.stringify(state, null, 2));
const auth = "Basic " + Buffer.from(`${WP_USER}:${(WP_APP_PASSWORD || "").replace(/\s/g, " ")}`).toString("base64");

async function wp(method, endpoint, body) {
  const res = await fetch(`${WP_URL}/wp-json/wp/v2/${endpoint}`, {
    method, headers: { Authorization: auth, "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const txt = await res.text();
  if (!res.ok) throw new Error(`${method} ${endpoint} -> ${res.status} ${txt.slice(0, 200)}`);
  return JSON.parse(txt);
}

function conteudo(file) {
  const html = fs.readFileSync(file, "utf8");
  return "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->";
}

async function enviar(it) {
  const file = path.join(DIR, it.slug + ".html");
  if (!fs.existsSync(file)) return { skip: true, motivo: "sem arquivo (ainda não gerado): " + path.basename(file) };
  const content = conteudo(file);
  if (DRY) return { ok: true, motivo: `dry-run (${content.length} bytes)` };
  const achados = await wp("GET", `pages?slug=${it.slug}&status=any&context=edit`);
  const dados = { content, status: STATUS, slug: it.slug };
  if (it.titulo) dados.title = it.titulo;
  if (TEMPLATE) dados.template = TEMPLATE;
  const pag = achados.length ? await wp("POST", `pages/${achados[0].id}`, dados) : await wp("POST", "pages", { title: it.slug, ...dados });
  const conf = await wp("GET", `pages/${pag.id}?context=edit`);   // confirma que gravou
  const gravou = conf.content.raw.length === content.length;
  return gravou ? { ok: true, id: pag.id, motivo: (achados.length ? "atualizada" : "criada") + " " + conf.status }
                : { ok: false, id: pag.id, motivo: "conteúdo gravado difere do enviado (cache/filtro do WP?)" };
}

(async () => {
  if (!DRY && !(WP_URL && WP_USER && WP_APP_PASSWORD)) { console.error("Defina WP_URL, WP_USER e WP_APP_PASSWORD (ou use --dry-run)."); process.exit(2); }
  const cats = CAT ? [CAT] : TODAS ? [...new Set(itens.map(i => i.segmento))] : [];
  if (!cats.length) { console.error("Informe --categoria <nome> ou --todas."); process.exit(2); }
  for (const cat of cats) {
    const fila = itens.filter(i => i.segmento === cat && !(state[i.slug] && state[i.slug].ok));
    console.log(`\n== ${cat}: ${fila.length} pendentes ==`);
    for (let i = 0; i < fila.length; i += LOTE) {
      const lote = fila.slice(i, i + LOTE);
      console.log(`-- lote ${i / LOTE + 1} (${lote.length} páginas) --`);
      for (const it of lote) {
        try { const r = await enviar(it); if (r.skip) { console.log("PULA ", it.slug, "-", r.motivo); continue; } state[it.slug] = r; console.log((r.ok ? "OK   " : "FALHA"), it.slug, "-", r.motivo); }
        catch (e) { state[it.slug] = { ok: false, motivo: e.message }; console.log("FALHA", it.slug, "-", e.message); }
        if (!DRY) save();
      }
      if (lote.some(it => state[it.slug] && !state[it.slug].ok)) { console.log("Há falhas no lote. Corrija antes do próximo lote."); process.exit(1); }
    }
  }
  console.log("\nConcluído.");
})();
