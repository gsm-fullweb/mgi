#!/usr/bin/env python3
"""Gera a matriz das 100 LPs do Active5 (MGD) em CSV e JSON."""
import csv, json, re, unicodedata

PRODUTO = "Tablet robusto Samsung Galaxy Tab Active5"

# segmento -> (pilar, dor, palavras-chave)
SEGMENTOS = {
    "Geral (hub)": ("tablet-robusto-active5", "Tablet comum quebra, molha e não aguenta rotina de trabalho pesado.", [
        "tablet robusto", "tablet robusto samsung", "tablet samsung robusto", "tablet industrial",
        "tablet industrial samsung", "tablet profissional", "tablet profissional para trabalho",
        "tablet para empresa", "tablet para empresas", "tablet empresarial", "tablet corporativo",
        "tablet samsung para empresa", "tablet samsung para trabalho", "tablet resistente",
        "tablet resistente a quedas", "tablet resistente a água", "tablet resistente a poeira",
        "tablet IP68", "tablet com certificação militar", "tablet para trabalho pesado"]),
    "Governo": ("tablet-robusto-active5-governo", "Servidor em campo coleta dados, fotos e formulários com equipamento sujeito a queda, chuva e poeira.", [
        "tablet robusto para prefeitura", "tablet para prefeitura", "tablet para órgão público",
        "tablet para órgãos públicos", "tablet para administração pública", "tablet para fiscalização",
        "tablet para fiscalização em campo", "tablet para fiscalização municipal",
        "tablet para agente de fiscalização", "tablet para agentes públicos", "tablet para guarda municipal",
        "tablet para agentes de trânsito", "tablet para secretaria de obras", "tablet para vistoria em campo"]),
    "Logística": ("tablet-robusto-active5-logistica", "Conferência, inventário e comprovante de entrega com equipamento que cai, molha e para a operação.", [
        "tablet para logística", "tablet robusto para logística", "tablet industrial para logística",
        "tablet para transportadora", "tablet para transporte", "tablet para centro de distribuição",
        "tablet para armazém", "tablet para controle de estoque", "tablet para inventário",
        "tablet para conferência de mercadorias", "tablet para gestão de estoque",
        "tablet para operador logístico", "tablet para entrega", "tablet para gestão de frota"]),
    "Manufatura": ("tablet-robusto-active5-manufatura", "Apontamento, inspeção e manutenção no chão de fábrica, com luvas, poeira e queda frequente.", [
        "tablet para indústria", "tablet robusto para indústria", "tablet industrial para fábrica",
        "tablet para fábrica", "tablet para chão de fábrica", "tablet robusto para chão de fábrica",
        "tablet para produção industrial", "tablet para apontamento de produção",
        "tablet para controle de produção", "tablet para manutenção industrial",
        "tablet para inspeção industrial", "tablet para controle de qualidade",
        "tablet para rastreabilidade industrial", "tablet para indústria 4.0"]),
    "Mineração": ("tablet-robusto-active5-mineracao", "Operação externa com partículas, vibração e manutenção em campo destroem tablets comuns.", [
        "tablet para mineração", "tablet robusto para mineração", "tablet industrial para mineração",
        "tablet para mineradora", "tablet para trabalho em mineração", "tablet resistente para mineração",
        "tablet para inspeção em mineração", "tablet para manutenção em mineração",
        "tablet para operação em campo mineração", "tablet para ambiente severo"]),
    "Saúde": ("tablet-robusto-active5-saude", "Prontuário e atendimento à beira do leito exigem equipamento que aguente higienização frequente.", [
        "tablet para hospital", "tablet para hospitais", "tablet para saúde", "tablet robusto para hospital",
        "tablet para uso hospitalar", "tablet para enfermagem", "tablet para atendimento hospitalar",
        "tablet para prontuário eletrônico", "tablet para equipe médica", "tablet para atendimento em campo saúde"]),
    "Serviços": ("tablet-robusto-active5-servicos", "Técnicos externos emitem ordens de serviço e vistorias em equipamento que não foi feito para rua.", [
        "tablet para trabalho em campo", "tablet robusto para trabalho em campo", "tablet para equipe de campo",
        "tablet para serviço de campo", "tablet para técnico de campo", "tablet para manutenção em campo",
        "tablet para ordem de serviço", "tablet para vistoria", "tablet para inspeção em campo",
        "tablet resistente para trabalho externo"]),
    "Utilities": ("tablet-robusto-active5-utilities", "Leitura de medidores e manutenção de rede a céu aberto, com chuva, poeira e queda.", [
        "tablet para companhia de energia", "tablet para setor elétrico", "tablet para manutenção elétrica",
        "tablet para empresa de saneamento", "tablet para saneamento", "tablet para leitura de medidores",
        "tablet para manutenção de rede", "tablet para concessionária de serviços públicos"]),
}

# variantes (plural/sinônimo) que canibalizam a página principal: consolidar como H2/seção
CONSOLIDAR = {
    # plural/sinonimo
    "tablet para empresas": "tablet para empresa",
    "tablet empresarial": "tablet para empresa",
    "tablet para órgãos públicos": "tablet para órgão público",
    "tablet para hospitais": "tablet para hospital",
    # mesma intencao, so muda o adjetivo (robusto/industrial/resistente/samsung)
    "tablet samsung para empresa": "tablet para empresa",
    "tablet profissional para trabalho": "tablet samsung para trabalho",
    "tablet robusto para prefeitura": "tablet para prefeitura",
    "tablet robusto para logística": "tablet para logística",
    "tablet industrial para logística": "tablet para logística",
    "tablet robusto para indústria": "tablet para indústria",
    "tablet industrial para fábrica": "tablet para fábrica",
    "tablet robusto para chão de fábrica": "tablet para chão de fábrica",
    "tablet robusto para mineração": "tablet para mineração",
    "tablet industrial para mineração": "tablet para mineração",
    "tablet resistente para mineração": "tablet para mineração",
    "tablet robusto para hospital": "tablet para hospital",
    "tablet robusto para trabalho em campo": "tablet para trabalho em campo",
}

def slugify(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

def intencao(kw, seg):
    if seg == "Geral (hub)":
        return "Comercial (pesquisa de produto)"
    return "Comercial (caso de uso por atividade)"

rows, n = [], 0
for seg, (pilar, dor, kws) in SEGMENTOS.items():
    for kw in kws:
        n += 1
        slug = slugify(kw)
        titulo = f"{kw[0].upper() + kw[1:]} | Galaxy Tab Active5 | MGD"
        consolidar = CONSOLIDAR.get(kw, "")
        canonical = slug if not consolidar else slugify(consolidar)
        rows.append({
            "n": n, "palavra_chave": kw, "segmento": seg, "pilar_pai": pilar,
            "intencao": intencao(kw, seg), "title_seo": titulo, "title_len": len(titulo),
            "h1": f"{kw[0].upper() + kw[1:]}: {PRODUTO.split(' ', 2)[2]}",
            "slug": slug, "canonical": f"/{canonical}/",
            "acao": "CONSOLIDAR na página " + consolidar if consolidar else "CRIAR LP (canonical próprio)",
            "dor_cliente": dor,
            "cta_whatsapp": f"Olá, vim pelo site MGD e gostaria de orçamento de {PRODUTO} para {kw.replace('tablet ', '', 1)}.",
        })

sec = {}
for r in rows:
    if r["acao"].startswith("CONSOLIDAR"):
        sec.setdefault(r["canonical"].strip("/"), []).append(r["palavra_chave"])
for r in rows:
    r["kw_secundarias"] = " | ".join(sec.get(r["slug"], [])) if r["acao"].startswith("CRIAR") else ""

with open("matriz-100-lps.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=";")
    w.writeheader(); w.writerows(rows)
with open("matriz-100-lps.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
print(n, "linhas;", sum(r["acao"].startswith("CRIAR") for r in rows), "LPs únicas;",
      sum(r["title_len"] > 60 for r in rows), "titles > 60 caracteres")
