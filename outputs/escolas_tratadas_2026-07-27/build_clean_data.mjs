import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const workDir = "C:/Users/Richard Wagner/Documents/Grupo MGI/outputs/escolas_tratadas_2026-07-27";
const sourceDir = path.join(workDir, "fonte_extraida", "pasta das escolas");
const sourceMain = path.join(sourceDir, "escolas_saude_alto_tiete_expandido_2026-07-27.csv");
const sourceDuplicates = path.join(sourceDir, "escolas_saude_alto_tiete_expandido_duplicados_2026-07-27.csv");
const outputXlsx = path.join(workDir, "escolas_saude_alto_tiete_tratado_2026-07-27.xlsx");
const outputCsv = path.join(workDir, "escolas_saude_alto_tiete_tratado_2026-07-27.csv");
const previewDir = path.join(workDir, "previews");

await fs.mkdir(previewDir, { recursive: true });

const mainText = await fs.readFile(sourceMain, "utf8");
const duplicateText = await fs.readFile(sourceDuplicates, "utf8");
const mainImport = await Workbook.fromCSV(mainText, { sheetName: "Importação" });
const dupImport = await Workbook.fromCSV(duplicateText, { sheetName: "Importação" });
const mainValues = mainImport.worksheets.getItemAt(0).getUsedRange(true).values;
const duplicateValues = dupImport.worksheets.getItemAt(0).getUsedRange(true).values;

function rowsFromMatrix(matrix) {
  const headers = matrix[0].map((v) => String(v ?? "").trim());
  return matrix.slice(1).filter((row) => row.some((v) => String(v ?? "").trim() !== "")).map((row) => {
    const obj = {};
    headers.forEach((header, index) => {
      obj[header] = row[index] == null ? "" : String(row[index]).trim();
    });
    return obj;
  });
}

const sourceRows = rowsFromMatrix(mainValues);
const duplicateRows = rowsFromMatrix(duplicateValues);

function cleanText(value) {
  return String(value ?? "").replace(/\s+/g, " ").trim();
}

function normalize(value) {
  return cleanText(value)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]/g, "");
}

function formatBrazilPhone(digits) {
  let local = digits;
  if ((local.length === 12 || local.length === 13) && local.startsWith("55")) {
    local = local.slice(2);
  }
  if (local.length === 8 || local.length === 9) {
    local = `11${local}`;
  }
  if (local.length !== 10 && local.length !== 11) return "";
  const ddd = local.slice(0, 2);
  const number = local.slice(2);
  const formatted = number.length === 9
    ? `${number.slice(0, 5)}-${number.slice(5)}`
    : `${number.slice(0, 4)}-${number.slice(4)}`;
  return `+55 (${ddd}) ${formatted}`;
}

function cleanPhones(value) {
  const original = cleanText(value);
  if (!original) return { primary: "", secondary: "", flags: [], changed: false };
  const flags = [];
  const parts = original.split(/[;|]+/).map((part) => part.trim()).filter(Boolean);
  const formatted = [];
  for (const part of parts) {
    const digits = part.replace(/\D/g, "");
    if (digits.length === 14) {
      flags.push(`Possível CNPJ no telefone: ${digits}`);
      continue;
    }
    const phone = formatBrazilPhone(digits);
    if (phone) {
      if (!formatted.includes(phone)) formatted.push(phone);
    } else {
      flags.push(`Telefone com formato não reconhecido: ${part}`);
    }
  }
  if (formatted.length > 2) flags.push("Mais de dois telefones no campo original");
  return {
    primary: formatted[0] ?? "",
    secondary: formatted[1] ?? "",
    flags,
    changed: original !== formatted.filter(Boolean).join("; "),
  };
}

function cleanEmail(value) {
  const original = cleanText(value);
  if (!original) return { value: "", valid: "", flags: [], changed: false };
  let result = original.toLowerCase().replace(/\s+/g, "");
  result = result.replace(/@uol\.combr$/i, "@uol.com.br");
  result = result.replace(/@gmaiil$/i, "@gmail.com");
  const valid = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(result);
  return {
    value: result,
    valid: valid ? "Sim" : "Não",
    flags: valid ? [] : [`E-mail precisa de validação: ${original}`],
    changed: result !== original,
  };
}

function cleanUrl(value) {
  const result = cleanText(value);
  if (!result) return "";
  if (/^https?:\/\//i.test(result)) return result;
  return `https://${result}`;
}

function scoreRow(row) {
  let score = 0;
  if (row.telefonePrincipal) score += 25;
  if (row.emailValido === "Sim") score += 25;
  if (row.site) score += 15;
  if (row.whatsapp) score += 10;
  if (row.instagram) score += 5;
  if (row.facebook) score += 5;
  if (row.linkedin) score += 5;
  if (row.notaGoogle && row.avaliacoesGoogle) score += 10;
  return score;
}

function classification(score) {
  if (score >= 60) return "Prioridade Alta";
  if (score >= 35) return "Prioridade Média";
  return "Prioridade Baixa";
}

const auditLog = [];
const cleanRows = sourceRows.map((row, index) => {
  const id = `AT-${String(index + 1).padStart(5, "0")}`;
  const phone = cleanPhones(row["Telefone"]);
  const whatsapp = cleanPhones(row["WhatsApp"]);
  const email = cleanEmail(row["E-mail"]);
  const reasons = [...phone.flags, ...email.flags];
  if (!cleanText(row["Bairro"])) reasons.push("Bairro ausente");
  if (!phone.primary && !email.value && !cleanText(row["Site"])) reasons.push("Sem telefone, e-mail ou site");
  if (phone.secondary) reasons.push("Campo original continha múltiplos telefones");

  if (phone.changed && cleanText(row["Telefone"])) {
    auditLog.push([id, "Telefone", cleanText(row["Telefone"]), [phone.primary, phone.secondary].filter(Boolean).join("; "), phone.flags.length ? "Normalizado com ressalva" : "Normalizado", phone.flags.join("; ")]);
  }
  if (email.changed) {
    auditLog.push([id, "E-mail", cleanText(row["E-mail"]), email.value, email.valid === "Sim" ? "Formatação corrigida" : "Correção parcial", email.flags.join("; ")]);
  } else if (email.valid === "Não") {
    auditLog.push([id, "E-mail", cleanText(row["E-mail"]), email.value, "Revisão necessária", email.flags.join("; ")]);
  }

  const cleaned = {
    id,
    nome: cleanText(row["Nome"]),
    tipo: cleanText(row["Tipo"]),
    categoria: cleanText(row["Categoria"]),
    cidade: cleanText(row["Cidade"]),
    bairro: cleanText(row["Bairro"]),
    endereco: cleanText(row["Endereço"]),
    telefonePrincipal: phone.primary,
    telefoneSecundario: phone.secondary,
    whatsapp: whatsapp.primary,
    email: email.value,
    emailValido: email.valid,
    site: cleanUrl(row["Site"]),
    instagram: cleanText(row["Instagram"]),
    facebook: cleanText(row["Facebook"]),
    linkedin: cleanText(row["LinkedIn"]),
    googleMaps: cleanUrl(row["Google Maps"]),
    notaGoogle: cleanText(row["Nota no Google"]),
    avaliacoesGoogle: cleanText(row["Quantidade de avaliações"]),
    status: "Não contatado",
    revisao: reasons.length ? "Sim" : "Não",
    motivos: reasons.join("; "),
    origem: "Base expandida 2026-07-27",
    telefoneOriginal: cleanText(row["Telefone"]),
    emailOriginal: cleanText(row["E-mail"]),
    scoreOriginal: Number(row["Score comercial"]) || 0,
    classeOriginal: cleanText(row["Classificação comercial"]),
    observacoes: cleanText(row["Observações comerciais"]),
  };
  cleaned.score = scoreRow(cleaned);
  cleaned.classe = classification(cleaned.score);
  return cleaned;
});

const byNameCity = new Map();
for (const row of cleanRows) {
  const key = `${normalize(row.nome)}|${normalize(row.cidade)}`;
  if (!byNameCity.has(key)) byNameCity.set(key, []);
  byNameCity.get(key).push(row);
}

const duplicateReview = duplicateRows.map((row, index) => {
  const name = cleanText(row["Nome"]);
  const city = cleanText(row["Cidade"]);
  const candidates = byNameCity.get(`${normalize(row["Duplicado de"] || name)}|${normalize(city)}`)
    ?? byNameCity.get(`${normalize(name)}|${normalize(city)}`)
    ?? [];
  const phone = cleanPhones(row["Telefone"]).primary;
  const address = cleanText(row["Endereço"]);
  const sameAddress = candidates.some((candidate) => normalize(candidate.endereco) === normalize(address));
  const samePhone = phone && candidates.some((candidate) => candidate.telefonePrincipal === phone);
  const sameEmail = cleanText(row["E-mail"]) && candidates.some((candidate) => normalize(candidate.email) === normalize(row["E-mail"]));
  let assessment = "Revisão manual";
  let action = "Comparar com a unidade principal";
  if (sameAddress || samePhone || sameEmail) {
    assessment = "Duplicado provável";
    action = "Manter fora da base principal após confirmação";
  } else if (candidates.length && address) {
    assessment = "Possível filial";
    action = "Confirmar unidade antes de excluir";
  } else if (!candidates.length) {
    assessment = "Sem correspondente claro";
    action = "Avaliar reinclusão";
  }
  return [
    `DUP-${String(index + 1).padStart(4, "0")}`,
    name,
    cleanText(row["Tipo"]),
    cleanText(row["Categoria"]),
    city,
    cleanText(row["Bairro"]),
    address,
    cleanText(row["Telefone"]),
    cleanText(row["E-mail"]),
    cleanText(row["Duplicado de"]),
    candidates.length,
    sameAddress ? "Sim" : "Não",
    samePhone ? "Sim" : "Não",
    assessment,
    action,
  ];
});

const headers = [
  "ID", "Nome", "Tipo", "Categoria", "Cidade", "Bairro", "Endereço",
  "Telefone principal", "Telefone secundário", "WhatsApp (não verificado)",
  "E-mail", "E-mail válido", "Site", "Instagram", "Facebook", "LinkedIn",
  "Google Maps", "Nota no Google", "Quantidade de avaliações", "Status comercial",
  "Score padronizado", "Classificação padronizada", "Revisão necessária",
  "Motivos da revisão", "Origem", "Telefone original", "E-mail original",
  "Score original", "Classificação original", "Observações originais",
];

const dataRows = cleanRows.map((row) => [
  row.id, row.nome, row.tipo, row.categoria, row.cidade, row.bairro, row.endereco,
  row.telefonePrincipal, row.telefoneSecundario, row.whatsapp, row.email, row.emailValido,
  row.site, row.instagram, row.facebook, row.linkedin, row.googleMaps, row.notaGoogle,
  row.avaliacoesGoogle, row.status, row.score, row.classe, row.revisao, row.motivos,
  row.origem, row.telefoneOriginal, row.emailOriginal, row.scoreOriginal,
  row.classeOriginal, row.observacoes,
]);

function csvEscape(value) {
  const text = String(value ?? "");
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

const csv = [headers, ...dataRows].map((row) => row.map(csvEscape).join(",")).join("\r\n");
await fs.writeFile(outputCsv, `\uFEFF${csv}`, "utf8");

const workbook = Workbook.create();
const summary = workbook.worksheets.add("Resumo");
const data = workbook.worksheets.add("Dados Tratados");
const review = workbook.worksheets.add("Revisão Duplicidades");
const log = workbook.worksheets.add("Log Correções");
const rules = workbook.worksheets.add("Regras");
workbook.comments.setSelf({ displayName: "Richard Wagner" });

const navy = "#17365D";
const blue = "#2F75B5";
const lightBlue = "#D9EAF7";
const green = "#70AD47";
const yellow = "#FFD966";
const red = "#F4CCCC";
const lightGray = "#F2F2F2";
const white = "#FFFFFF";

summary.showGridLines = false;
summary.getRange("A1:H1").merge();
summary.getRange("A1").values = [["Base tratada — Escolas e Saúde | Alto Tietê"]];
summary.getRange("A1:H1").format = { fill: navy, font: { bold: true, color: white, size: 16 }, horizontalAlignment: "center", verticalAlignment: "center" };
summary.getRange("A1:H1").format.rowHeight = 30;
summary.getRange("A2:H2").merge();
summary.getRange("A2").values = [["Tratamento em 2026-07-27 · Originais preservados · Score de contatabilidade padronizado"]];
summary.getRange("A2:H2").format = { fill: lightBlue, font: { italic: true, color: navy }, horizontalAlignment: "center" };

summary.getRange("A4:B4").values = [["Indicador", "Resultado"]];
summary.getRange("A5:A11").values = [
  ["Registros tratados"],
  ["Registros em revisão"],
  ["Possíveis duplicados/filiais"],
  ["Com telefone"],
  ["Com e-mail válido"],
  ["Com site"],
  ["Sem canal direto"],
];
summary.getRange("B5").formulas = [[`=COUNTA('Dados Tratados'!$A$2:$A$${dataRows.length + 1})`]];
summary.getRange("B6").formulas = [[`=COUNTIF('Dados Tratados'!$W$2:$W$${dataRows.length + 1},"Sim")`]];
summary.getRange("B7").formulas = [[`=COUNTA('Revisão Duplicidades'!$A$2:$A$${duplicateReview.length + 1})`]];
summary.getRange("B8").formulas = [[`=SUM('Dados Tratados'!$AE$2:$AE$${dataRows.length + 1})`]];
summary.getRange("B9").formulas = [[`=COUNTIF('Dados Tratados'!$L$2:$L$${dataRows.length + 1},"Sim")`]];
summary.getRange("B10").formulas = [[`=SUM('Dados Tratados'!$AF$2:$AF$${dataRows.length + 1})`]];
summary.getRange("B11").formulas = [[`=SUM('Dados Tratados'!$AG$2:$AG$${dataRows.length + 1})`]];

summary.getRange("D4:E4").values = [["Cidade", "Registros"]];
const cities = ["Guarulhos", "Mogi das Cruzes", "Suzano", "Itaquaquecetuba", "Arujá"];
summary.getRange("D5:D9").values = cities.map((city) => [city]);
summary.getRange("E5").formulas = [[`=COUNTIF('Dados Tratados'!$E$2:$E$${dataRows.length + 1},D5)`]];
summary.getRange("E5:E9").fillDown();

summary.getRange("G4:H4").values = [["Classificação", "Registros"]];
const classes = ["Prioridade Alta", "Prioridade Média", "Prioridade Baixa"];
summary.getRange("G5:G7").values = classes.map((item) => [item]);
summary.getRange("H5").formulas = [[`=COUNTIF('Dados Tratados'!$V$2:$V$${dataRows.length + 1},G5)`]];
summary.getRange("H5:H7").fillDown();

for (const rangeName of ["A4:B4", "D4:E4", "G4:H4"]) {
  summary.getRange(rangeName).format = { fill: blue, font: { bold: true, color: white }, horizontalAlignment: "center" };
}
summary.getRange("A5:B11").format.borders = { preset: "inside", style: "thin", color: "#D9E2F3" };
summary.getRange("D5:E9").format.borders = { preset: "inside", style: "thin", color: "#D9E2F3" };
summary.getRange("G5:H7").format.borders = { preset: "inside", style: "thin", color: "#D9E2F3" };
summary.getRange("B5:B11").format.numberFormat = "#,##0";
summary.getRange("E5:E9").format.numberFormat = "#,##0";
summary.getRange("H5:H7").format.numberFormat = "#,##0";
summary.getRange("A13:H13").merge();
summary.getRange("A13").values = [["Leitura rápida"]];
summary.getRange("A13:H13").format = { fill: navy, font: { bold: true, color: white } };
summary.getRange("A14:H17").merge();
summary.getRange("A14").values = [[
  "A aba Dados Tratados contém a base operacional. Revisão Duplicidades preserva os 90 registros anteriormente removidos. " +
  "O score mede contatabilidade: telefone 25, e-mail válido 25, site 15, WhatsApp 10, redes sociais 5 cada e Google 10. " +
  "Os contatos não foram validados externamente; itens suspeitos aparecem em Revisão necessária."
]];
summary.getRange("A14:H17").format = { fill: lightGray, wrapText: true, verticalAlignment: "top" };
summary.getRange("A:A").format.columnWidth = 26;
summary.getRange("B:B").format.columnWidth = 14;
summary.getRange("C:C").format.columnWidth = 3;
summary.getRange("D:D").format.columnWidth = 22;
summary.getRange("E:E").format.columnWidth = 14;
summary.getRange("F:F").format.columnWidth = 3;
summary.getRange("G:G").format.columnWidth = 22;
summary.getRange("H:H").format.columnWidth = 14;
summary.freezePanes.freezeRows(2);

data.getRangeByIndexes(0, 0, dataRows.length + 1, headers.length).values = [headers, ...dataRows];
data.freezePanes.freezeRows(1);
data.freezePanes.freezeColumns(2);
data.showGridLines = false;
data.getRange("AE1:AG1").values = [["Tem telefone", "Tem site", "Sem canal direto"]];
data.getRange("A1:AG1").format = { fill: navy, font: { bold: true, color: white }, wrapText: true, horizontalAlignment: "center", verticalAlignment: "center" };
data.getRange("A1:AG1").format.rowHeight = 36;
data.getRange(`U2:U${dataRows.length + 1}`).format.numberFormat = "0";
data.getRange(`U2`).formulas = [[`=IF(LEN(H2)>0,25,0)+IF(L2="Sim",25,0)+IF(LEN(M2)>0,15,0)+IF(LEN(J2)>0,10,0)+IF(LEN(N2)>0,5,0)+IF(LEN(O2)>0,5,0)+IF(LEN(P2)>0,5,0)+IF(AND(LEN(R2)>0,LEN(S2)>0),10,0)`]];
data.getRange(`U2:U${dataRows.length + 1}`).fillDown();
data.getRange("V2").formulas = [[`=IF(U2>=60,"Prioridade Alta",IF(U2>=35,"Prioridade Média","Prioridade Baixa"))`]];
data.getRange(`V2:V${dataRows.length + 1}`).fillDown();
data.getRange("AE2").formulas = [[`=IF(LEN(H2)>0,1,0)`]];
data.getRange(`AE2:AE${dataRows.length + 1}`).fillDown();
data.getRange("AF2").formulas = [[`=IF(LEN(M2)>0,1,0)`]];
data.getRange(`AF2:AF${dataRows.length + 1}`).fillDown();
data.getRange("AG2").formulas = [[`=IF(AND(LEN(H2)=0,LEN(K2)=0,LEN(M2)=0),1,0)`]];
data.getRange(`AG2:AG${dataRows.length + 1}`).fillDown();
data.getRange(`T2:T${dataRows.length + 1}`).dataValidation = { rule: { type: "list", values: ["Não contatado", "Tentativa de contato", "Contato realizado", "Reunião agendada", "Proposta enviada", "Cliente", "Sem interesse"] } };
data.getRange(`V2:V${dataRows.length + 1}`).conditionalFormats.add("containsText", { text: "Alta", format: { fill: "#C6E0B4", font: { color: "#375623", bold: true } } });
data.getRange(`V2:V${dataRows.length + 1}`).conditionalFormats.add("containsText", { text: "Média", format: { fill: "#FFF2CC", font: { color: "#7F6000" } } });
data.getRange(`V2:V${dataRows.length + 1}`).conditionalFormats.add("containsText", { text: "Baixa", format: { fill: "#FCE4D6", font: { color: "#843C0C" } } });
data.getRange(`W2:W${dataRows.length + 1}`).conditionalFormats.add("containsText", { text: "Sim", format: { fill: red, font: { color: "#9C0006", bold: true } } });
const dataTable = data.tables.add(`A1:AG${dataRows.length + 1}`, true, "DadosTratados");
dataTable.style = "TableStyleMedium2";
data.getRange("A:A").format.columnWidth = 12;
data.getRange("B:B").format.columnWidth = 32;
data.getRange("C:D").format.columnWidth = 18;
data.getRange("E:F").format.columnWidth = 20;
data.getRange("G:G").format.columnWidth = 48;
data.getRange("H:J").format.columnWidth = 22;
data.getRange("K:Q").format.columnWidth = 28;
data.getRange("R:S").format.columnWidth = 14;
data.getRange("T:W").format.columnWidth = 20;
data.getRange("X:X").format.columnWidth = 55;
data.getRange("Y:AC").format.columnWidth = 22;
data.getRange("AD:AD").format.columnWidth = 60;
data.getRange("AE:AG").format.columnWidth = 15;
workbook.comments.addThread({ cell: data.getRange("U1") }, "Score auditável: telefone 25; e-mail válido 25; site 15; WhatsApp 10; Instagram, Facebook e LinkedIn 5 cada; nota e avaliações Google 10.");

const reviewHeaders = ["ID revisão", "Nome", "Tipo", "Categoria", "Cidade", "Bairro", "Endereço", "Telefone original", "E-mail original", "Marcado como duplicado de", "Candidatos na base", "Mesmo endereço", "Mesmo telefone", "Avaliação", "Ação sugerida"];
review.getRangeByIndexes(0, 0, duplicateReview.length + 1, reviewHeaders.length).values = [reviewHeaders, ...duplicateReview];
review.freezePanes.freezeRows(1);
review.showGridLines = false;
review.getRange("A1:O1").format = { fill: navy, font: { bold: true, color: white }, wrapText: true, horizontalAlignment: "center" };
review.getRange(`N2:N${duplicateReview.length + 1}`).conditionalFormats.add("containsText", { text: "Possível filial", format: { fill: yellow, font: { color: "#7F6000", bold: true } } });
review.getRange(`N2:N${duplicateReview.length + 1}`).conditionalFormats.add("containsText", { text: "Duplicado provável", format: { fill: "#C6E0B4", font: { color: "#375623" } } });
review.tables.add(`A1:O${duplicateReview.length + 1}`, true, "RevisaoDuplicidades").style = "TableStyleMedium2";
review.getRange("A:A").format.columnWidth = 14;
review.getRange("B:B").format.columnWidth = 34;
review.getRange("C:F").format.columnWidth = 20;
review.getRange("G:G").format.columnWidth = 48;
review.getRange("H:J").format.columnWidth = 28;
review.getRange("K:M").format.columnWidth = 16;
review.getRange("N:O").format.columnWidth = 32;

const logHeaders = ["ID", "Campo", "Valor original", "Valor tratado", "Ação", "Observação"];
log.getRangeByIndexes(0, 0, auditLog.length + 1, logHeaders.length).values = [logHeaders, ...auditLog];
log.freezePanes.freezeRows(1);
log.showGridLines = false;
log.getRange("A1:F1").format = { fill: navy, font: { bold: true, color: white }, horizontalAlignment: "center" };
if (auditLog.length) log.tables.add(`A1:F${auditLog.length + 1}`, true, "LogCorrecoes").style = "TableStyleMedium2";
log.getRange("A:A").format.columnWidth = 14;
log.getRange("B:B").format.columnWidth = 18;
log.getRange("C:D").format.columnWidth = 35;
log.getRange("E:E").format.columnWidth = 24;
log.getRange("F:F").format.columnWidth = 55;

rules.showGridLines = false;
rules.getRange("A1:F1").merge();
rules.getRange("A1").values = [["Regras de tratamento e auditoria"]];
rules.getRange("A1:F1").format = { fill: navy, font: { bold: true, color: white, size: 15 }, horizontalAlignment: "center" };
rules.getRange("A3:C3").values = [["Componente do score", "Pontos", "Regra"]];
rules.getRange("A4:C11").values = [
  ["Telefone principal", 25, "Telefone reconhecido e padronizado"],
  ["E-mail válido", 25, "Validação apenas sintática"],
  ["Site", 15, "URL preenchida"],
  ["WhatsApp", 10, "Número informado; não houve confirmação externa"],
  ["Instagram", 5, "Campo preenchido"],
  ["Facebook", 5, "Campo preenchido"],
  ["LinkedIn", 5, "Campo preenchido"],
  ["Google", 10, "Nota e quantidade de avaliações preenchidas"],
];
rules.getRange("E3:F3").values = [["Faixa", "Classificação"]];
rules.getRange("E4:F6").values = [
  ["60 a 100", "Prioridade Alta"],
  ["35 a 59", "Prioridade Média"],
  ["0 a 34", "Prioridade Baixa"],
];
rules.getRange("A13:F13").merge();
rules.getRange("A13").values = [["Tratamentos aplicados"]];
rules.getRange("A14:F21").values = [
  ["Telefones", "", "Padronização em +55 (DDD) número; DDD 11 adicionado quando ausente; múltiplos números separados; sequências de 14 dígitos sinalizadas como possível CNPJ.", "", "", ""],
  ["E-mails", "", "Conversão para minúsculas, retirada de espaços e correção de domínios evidentemente quebrados; validação sintática, sem teste de entrega.", "", "", ""],
  ["URLs", "", "Espaços removidos e protocolo HTTPS adicionado quando ausente.", "", "", ""],
  ["Status", "", "Todos iniciados como Não contatado, com lista controlada para atualização operacional.", "", "", ""],
  ["Duplicidades", "", "Nenhum dos 90 descartados foi apagado; todos permanecem na aba Revisão Duplicidades.", "", "", ""],
  ["Originais", "", "Telefone, e-mail, score, classificação e observações originais permanecem na base tratada.", "", "", ""],
  ["Validação externa", "", "Não realizada. Sites, telefones, e-mails, WhatsApp e perfis do Google ainda precisam ser confirmados.", "", "", ""],
  ["Fonte", "", "escolasbinho.zip, recebido em 2026-07-27.", "", "", ""],
];
for (const rangeName of ["A3:C3", "E3:F3", "A13:F13"]) {
  rules.getRange(rangeName).format = { fill: blue, font: { bold: true, color: white }, horizontalAlignment: "center" };
}
rules.getRange("A14:F21").format = { wrapText: true, verticalAlignment: "top" };
rules.getRange("A:A").format.columnWidth = 24;
rules.getRange("B:B").format.columnWidth = 12;
rules.getRange("C:C").format.columnWidth = 70;
rules.getRange("D:D").format.columnWidth = 3;
rules.getRange("E:F").format.columnWidth = 22;
rules.freezePanes.freezeRows(1);

const summaryInspect = await workbook.inspect({
  kind: "table",
  range: "Resumo!A1:H17",
  include: "values,formulas",
  tableMaxRows: 20,
  tableMaxCols: 10,
  maxChars: 6000,
});
console.log("INSPECT_SUMMARY");
console.log(summaryInspect.ndjson);

const dataInspect = await workbook.inspect({
  kind: "table",
  range: "Dados Tratados!A1:AD6",
  include: "values,formulas",
  tableMaxRows: 6,
  tableMaxCols: 30,
  maxChars: 9000,
});
console.log("INSPECT_DATA");
console.log(dataInspect.ndjson);

const errorInspect = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
console.log("FORMULA_ERRORS");
console.log(errorInspect.ndjson);

const renderTargets = [
  ["Resumo", "A1:H17"],
  ["Dados Tratados", "A1:L15"],
  ["Revisão Duplicidades", "A1:O15"],
  ["Log Correções", "A1:F15"],
  ["Regras", "A1:F21"],
];
for (const [sheetName, range] of renderTargets) {
  const preview = await workbook.render({ sheetName, range, scale: 1.2, format: "png" });
  const safeName = normalize(sheetName) || "sheet";
  await fs.writeFile(path.join(previewDir, `${safeName}.png`), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputXlsx);
const savedBlob = await FileBlob.load(outputXlsx);
const savedWorkbook = await SpreadsheetFile.importXlsx(savedBlob);
const savedInspect = await savedWorkbook.inspect({
  kind: "table",
  range: "Resumo!A4:H11",
  include: "values,formulas",
  tableMaxRows: 10,
  tableMaxCols: 8,
  maxChars: 4000,
});
console.log("SAVED_WORKBOOK_CHECK");
console.log(savedInspect.ndjson);

const stats = {
  sourceRows: sourceRows.length,
  outputRows: dataRows.length,
  duplicateReviewRows: duplicateReview.length,
  auditLogRows: auditLog.length,
  reviewRequired: cleanRows.filter((row) => row.revisao === "Sim").length,
  validEmails: cleanRows.filter((row) => row.emailValido === "Sim").length,
  phones: cleanRows.filter((row) => row.telefonePrincipal).length,
  sites: cleanRows.filter((row) => row.site).length,
  noDirectChannel: cleanRows.filter((row) => !row.telefonePrincipal && !row.email && !row.site).length,
  classes: Object.fromEntries(["Prioridade Alta", "Prioridade Média", "Prioridade Baixa"].map((item) => [item, cleanRows.filter((row) => row.classe === item).length])),
};
console.log("STATS");
console.log(JSON.stringify(stats));
