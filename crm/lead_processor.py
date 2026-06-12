#!/usr/bin/env python3
import csv
import os
import re
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path(__file__).resolve().parent
LEADS_PATH = BASE_DIR / "leads.csv"
TODAY_PATH = BASE_DIR / "today_contact_list.csv"
REJECTED_PATH = BASE_DIR / "rejected_leads.csv"
FOLLOWUP_PATH = BASE_DIR / "followup_tasks.csv"

FIELDS = [
    "lead_id", "created_at", "updated_at", "source_platform", "source_detail", "source_url",
    "lead_name", "store_name", "profile_url", "store_url", "facebook_url", "instagram_url",
    "linkedin_url", "shopee_url", "mercado_livre_url", "whatsapp_raw", "whatsapp_clean",
    "email", "city", "state", "country", "customer_type", "sales_platform",
    "product_category_detected", "recommended_krog_category", "business_signal",
    "source_reason", "pain_point", "krog_angle", "lead_score", "lead_level",
    "contact_priority", "whatsapp_message_1", "whatsapp_followup_d1", "whatsapp_followup_d3",
    "whatsapp_followup_d7", "whatsapp_link", "email_message_1", "linkedin_note_draft",
    "status", "next_action", "next_followup_date", "notes", "risk_flag", "duplicate_flag",
    "last_contact_date", "reply_summary",
]

FIELD_LABELS_ZH = {
    "lead_id": "线索编号",
    "created_at": "创建日期",
    "updated_at": "更新日期",
    "source_platform": "来源平台",
    "source_detail": "来源详情",
    "source_url": "来源链接",
    "lead_name": "联系人姓名",
    "store_name": "店铺名称",
    "profile_url": "主页链接",
    "store_url": "店铺网站",
    "facebook_url": "Facebook链接",
    "instagram_url": "Instagram链接",
    "linkedin_url": "LinkedIn链接",
    "shopee_url": "Shopee链接",
    "mercado_livre_url": "Mercado Livre链接",
    "whatsapp_raw": "WhatsApp原始号码",
    "whatsapp_clean": "WhatsApp清洗号码",
    "email": "邮箱",
    "city": "城市",
    "state": "州",
    "country": "国家",
    "customer_type": "客户类型",
    "sales_platform": "销售平台",
    "product_category_detected": "识别到的产品类目",
    "recommended_krog_category": "推荐KROG类目",
    "business_signal": "客户价值信号",
    "source_reason": "发现原因",
    "pain_point": "可能痛点",
    "krog_angle": "KROG切入角度",
    "lead_score": "客户评分",
    "lead_level": "客户等级",
    "contact_priority": "联系优先级",
    "whatsapp_message_1": "WhatsApp首触达话术",
    "whatsapp_followup_d1": "D+1跟进话术",
    "whatsapp_followup_d3": "D+3跟进话术",
    "whatsapp_followup_d7": "D+7跟进话术",
    "whatsapp_link": "wa.me一键链接",
    "email_message_1": "邮件首触达草稿",
    "linkedin_note_draft": "LinkedIn建联草稿",
    "status": "状态",
    "next_action": "下一步动作",
    "next_followup_date": "下次跟进日期",
    "notes": "备注",
    "risk_flag": "风险标记",
    "duplicate_flag": "重复标记",
    "last_contact_date": "上次联系日期",
    "reply_summary": "回复摘要",
    "rejection_reason": "拒绝原因",
}

FIELD_LABELS = {
    "lead_id": "xiansuo_bianhao",
    "created_at": "chuangjian_riqi",
    "updated_at": "gengxin_riqi",
    "source_platform": "laiyuan_pingtai",
    "source_detail": "laiyuan_xiangqing",
    "source_url": "laiyuan_lianjie",
    "lead_name": "lianxiren_xingming",
    "store_name": "dianpu_mingcheng",
    "profile_url": "zhuye_lianjie",
    "store_url": "dianpu_wangzhan",
    "facebook_url": "facebook_lianjie",
    "instagram_url": "instagram_lianjie",
    "linkedin_url": "linkedin_lianjie",
    "shopee_url": "shopee_lianjie",
    "mercado_livre_url": "mercado_livre_lianjie",
    "whatsapp_raw": "whatsapp_yuanshi_haoma",
    "whatsapp_clean": "whatsapp_qingxi_haoma",
    "email": "youxiang",
    "city": "chengshi",
    "state": "zhou",
    "country": "guojia",
    "customer_type": "kehu_leixing",
    "sales_platform": "xiaoshou_pingtai",
    "product_category_detected": "shibie_chanpin_leimu",
    "recommended_krog_category": "tuijian_krog_leimu",
    "business_signal": "kehu_jiazhi_xinhao",
    "source_reason": "faxian_yuanyin",
    "pain_point": "keneng_tongdian",
    "krog_angle": "krog_qieru_jiaodu",
    "lead_score": "kehu_pingfen",
    "lead_level": "kehu_dengji",
    "contact_priority": "lianxi_youxianji",
    "whatsapp_message_1": "whatsapp_shouci_huashu",
    "whatsapp_followup_d1": "d1_genjin_huashu",
    "whatsapp_followup_d3": "d3_genjin_huashu",
    "whatsapp_followup_d7": "d7_genjin_huashu",
    "whatsapp_link": "wa_me_yijian_lianjie",
    "email_message_1": "youjian_shouci_caogao",
    "linkedin_note_draft": "linkedin_jianlian_caogao",
    "status": "zhuangtai",
    "next_action": "xiayibu_dongzuo",
    "next_followup_date": "xiaci_genjin_riqi",
    "notes": "beizhu",
    "risk_flag": "fengxian_biaoji",
    "duplicate_flag": "chongfu_biaoji",
    "last_contact_date": "shangci_lianxi_riqi",
    "reply_summary": "huifu_zhaiyao",
    "rejection_reason": "jujue_yuanyin",
}

LABEL_TO_FIELD = {field: field for field in FIELDS}
LABEL_TO_FIELD.update({label: field for field, label in FIELD_LABELS_ZH.items()})
LABEL_TO_FIELD.update({label: field for field, label in FIELD_LABELS.items()})

FOLLOWUP_FIELDS = [
    "task_id", "lead_id", "lead_name", "store_name", "whatsapp_clean",
    "followup_stage", "followup_date", "message", "status", "notes",
]

FOLLOWUP_LABELS_ZH = {
    "task_id": "任务编号",
    "lead_id": "线索编号",
    "lead_name": "联系人姓名",
    "store_name": "店铺名称",
    "whatsapp_clean": "WhatsApp清洗号码",
    "followup_stage": "跟进阶段",
    "followup_date": "跟进日期",
    "message": "跟进话术",
    "status": "状态",
    "notes": "备注",
}

FOLLOWUP_LABELS = {
    "task_id": "renwu_bianhao",
    "lead_id": "xiansuo_bianhao",
    "lead_name": "lianxiren_xingming",
    "store_name": "dianpu_mingcheng",
    "whatsapp_clean": "whatsapp_qingxi_haoma",
    "followup_stage": "genjin_jieduan",
    "followup_date": "genjin_riqi",
    "message": "genjin_huashu",
    "status": "zhuangtai",
    "notes": "beizhu",
}

FOLLOWUP_LABEL_TO_FIELD = {field: field for field in FOLLOWUP_FIELDS}
FOLLOWUP_LABEL_TO_FIELD.update({label: field for field, label in FOLLOWUP_LABELS_ZH.items()})
FOLLOWUP_LABEL_TO_FIELD.update({label: field for field, label in FOLLOWUP_LABELS.items()})

POSITIVE_RULES = [
    ("procuro fornecedor", 30), ("dropshipping", 30), ("quero catálogo", 25),
    ("quero catalogo", 25), ("tenho loja", 20), ("vendo online", 20),
    ("fornecedor confiável", 30), ("fornecedor confiavel", 30),
    ("estou começando", 10), ("estou comecando", 10), ("preciso de produtos", 20),
]

KROG_MATCHES = {
    "infantil": (
        ["infantil", "bebê", "bebe", "criança", "crianca", "maternidade", "baby"],
        "acessórios para bebês; roupa infantil; toalha infantil; pantufa infantil; brinquedo; papelaria",
        "Temos opções infantis e para bebês com estoque no Brasil, sem necessidade de comprar lote grande.",
    ),
    "feminina": (
        ["feminina", "moda", "bolsa", "bolsas", "acessório", "acessorio", "pantufa"],
        "bolsas femininas; bolsas; pantufas; cachecol; luvas; toucas; acessórios; moda feminina",
        "Temos linhas como bolsas, pantufas e acessórios que combinam com loja feminina e podem ser testadas sem estoque próprio.",
    ),
    "casa": (
        ["casa", "utilidades", "cozinha", "banho", "toalha", "luminária", "luminaria", "decoração", "decoracao"],
        "utilidades; cozinha; luminárias; banho; toalhas; ferramentas; guarda-chuva; capa de chuva",
        "Temos categorias para casa, utilidades e cozinha com estoque local e envio direto ao cliente.",
    ),
    "fitness": (
        ["fitness", "academia", "esporte", "bicicleta", "esteira", "patinete"],
        "fitness; bicicleta ergométrica; esteira elétrica; patinete; bola",
        "Temos produtos fitness e equipamentos para venda online com modelo One Drop Shipping.",
    ),
    "ferramentas": (
        ["ferramenta", "ferramentas", "automotivo", "fechadura", "camera", "câmera", "suporte"],
        "ferramentas; suporte para celular; limpeza automotiva; bomba de ar; fechadura; camera",
        "Temos ferramentas e acessórios úteis para marketplace, com estoque local no Brasil.",
    ),
}

FOLLOWUPS = {
    "D+1": "Oi, {name}, tudo bem? Só passando para confirmar se você conseguiu ver minha mensagem. Posso te enviar algumas categorias que combinam com sua loja?",
    "D+3": "{name}, temos várias linhas para lojistas online, como pantufas, bolsas, toalhas, infantil, utilidades, fitness e produtos para casa. Qual dessas combina melhor com sua loja hoje?",
    "D+7": "Tudo bem, {name}. Vou deixar meu contato por aqui. Se em algum momento você precisar de fornecedor nacional com estoque no Brasil e modelo One Drop Shipping, fico à disposição.",
}


def today_date():
    override = os.environ.get("KROG_TODAY")
    if override:
        return date.fromisoformat(override)
    return date.today()


def norm(value):
    return (value or "").strip()


def joined_text(row):
    return " ".join(norm(row.get(k)) for k in [
        "source_detail", "source_reason", "business_signal", "customer_type", "sales_platform",
        "product_category_detected", "notes", "store_name"
    ]).lower()


def clean_whatsapp(raw):
    digits = re.sub(r"\D+", "", raw or "")
    if not digits:
        return ""
    if digits.startswith("00"):
        digits = digits[2:]
    if digits.startswith("55"):
        return digits
    if digits.startswith("0") and len(digits) in (11, 12):
        digits = digits[1:]
    if len(digits) in (10, 11):
        return "55" + digits
    return digits


def lead_level(score):
    score = max(0, min(100, score))
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 50:
        return "C"
    return "D"


def is_rejected_risk(row):
    risk_text = joined_text({
        "notes": " ".join([
            row.get("risk_flag", ""),
            row.get("notes", ""),
            row.get("customer_type", ""),
            row.get("sales_platform", ""),
        ])
    })
    return any(token in risk_text for token in [
        "疑似同行供应商", "供应商", "somente atacado", "atacado caixa fechada",
        "importador", "concorrente", "fornecedor/importador",
    ])


def score_row(row):
    text = joined_text(row)
    score = 0
    for token, points in POSITIVE_RULES:
        if token in text:
            score += points
    if norm(row.get("shopee_url")):
        score += 30
    if norm(row.get("mercado_livre_url")):
        score += 25
    if norm(row.get("instagram_url")):
        score += 15
    if norm(row.get("whatsapp_clean")) or norm(row.get("whatsapp_raw")):
        score += 15
    if norm(row.get("store_url")):
        score += 20
    if norm(row.get("linkedin_url")) and any(x in text for x in ["e-commerce", "marketplace", "founder", "owner", "dono", "fundador"]):
        score += 20
    if any(x in text for x in ["produto", "produtos", "loja", "catálogo", "catalogo"]):
        score += 15
    if any(x in text for x in ["30 dias", "recente", "post recente", "atualizado"]):
        score += 15
    if match_category(row)[0] != "catálogo amplo":
        score += 20
    if any(x in text for x in ["infantil", "casa", "bolsas", "pantufas", "moda feminina", "utilidades", "fitness", "ferramentas", "banho", "cozinha"]):
        score += 20
    if norm(row.get("email")) or norm(row.get("whatsapp_clean")) or norm(row.get("whatsapp_raw")):
        score += 15
    if norm(row.get("instagram_url")) and (norm(row.get("whatsapp_clean")) or norm(row.get("whatsapp_raw"))):
        score += 20
    if norm(row.get("shopee_url")) and norm(row.get("instagram_url")):
        score += 25
    if norm(row.get("shopee_url")) and (norm(row.get("whatsapp_clean")) or norm(row.get("whatsapp_raw"))):
        score += 30
    if any(x in text for x in ["comentário", "comentario", "preço", "preco", "quanto custa"]):
        score += 10
    if any(x in text for x in ["foto real", "produto real", "imagens reais"]):
        score += 10
    channels = sum(bool(norm(row.get(k))) for k in ["instagram_url", "shopee_url", "mercado_livre_url", "store_url", "facebook_url"])
    if channels >= 2:
        score += 15

    risk = joined_text({"notes": row.get("risk_flag", "") + " " + row.get("notes", "")})
    if "pessoal" in risk or "个人" in risk:
        score -= 20
    if not (norm(row.get("email")) or norm(row.get("whatsapp_clean")) or norm(row.get("whatsapp_raw"))):
        score -= 15
    if "não combina" in risk or "nao combina" in risk or "类目不匹配" in risk:
        score -= 20
    if "concorrente" in risk or "供应商" in risk or "somente atacado" in risk or "importador" in risk:
        score -= 60
    if "informação insuficiente" in risk or "informacao insuficiente" in risk or "信息不足" in risk:
        score -= 10
    if "fake" in risk or "空号" in risk:
        score -= 30
    return max(0, min(100, score))


def match_category(row):
    text = joined_text(row)
    for _, (keywords, categories, angle) in KROG_MATCHES.items():
        if any(keyword in text for keyword in keywords):
            return categories, angle
    return "catálogo amplo", "catálogo amplo com várias categorias para testar sem estoque"


def display_name(row):
    return norm(row.get("lead_name")) or norm(row.get("store_name")) or "tudo bem"


def source_phrase(row):
    platform = norm(row.get("source_platform"))
    if platform == "Facebook":
        return "Vi seu comentário no Facebook sobre fornecedor/dropshipping"
    if platform == "Instagram":
        return "Vi a sua loja no Instagram"
    if platform == "LinkedIn":
        return "Vi seu perfil no LinkedIn e percebi que você atua com e-commerce/loja online"
    if platform == "Shopee":
        return f"Encontrei a loja {norm(row.get('store_name')) or 'de vocês'} pela Shopee"
    if platform == "Google":
        return f"Encontrei a loja {norm(row.get('store_name')) or 'de vocês'} pesquisando lojas online"
    return "Vi que você trabalha com vendas online"


def build_message(row):
    name = display_name(row)
    categories, angle = match_category(row)
    source = source_phrase(row)
    return (
        f"Olá, {name}, tudo bem? {source} e achei que poderia fazer sentido conversar.\n\n"
        f"Sou da KROG, fornecedor nacional com estoque em São Paulo. Trabalhamos com One Drop Shipping para lojistas que querem ampliar o catálogo sem comprar lote grande.\n\n"
        f"Hoje vocês vendem mais por Shopee, Mercado Livre, Instagram ou WhatsApp?"
    )


def make_link(phone, message):
    if not phone or not message:
        return ""
    return f"https://wa.me/{phone}?text={quote(message)}"


def read_rows(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            normalized = {}
            for key, value in row.items():
                normalized_key = LABEL_TO_FIELD.get(key) or FOLLOWUP_LABEL_TO_FIELD.get(key) or key
                normalized[normalized_key] = value
            rows.append(normalized)
        return rows


def write_rows(path, rows, fields, labels=None):
    labels = labels or FIELD_LABELS
    output_fields = [labels.get(field, field) for field in fields]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=output_fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({labels.get(field, field): row.get(field, "") for field in fields})


def similar(a, b):
    a, b = norm(a).lower(), norm(b).lower()
    return bool(a and b and SequenceMatcher(None, a, b).ratio() >= 0.88)


def is_dedupe_url(value):
    value = norm(value).lower()
    if not value:
        return False
    return "/explore/tags/" not in value and "/p/" not in value and "/reel/" not in value


def merge_rows(primary, duplicate):
    for key, value in duplicate.items():
        if norm(value) and not norm(primary.get(key)):
            primary[key] = value
    dup_source = norm(duplicate.get("source_platform"))
    notes = norm(primary.get("notes"))
    primary["notes"] = (notes + " | " if notes else "") + f"duplicate_source:{dup_source or 'unknown'}"
    primary["duplicate_flag"] = "yes"
    return primary


def dedupe(rows):
    result = []
    for row in rows:
        duplicate_index = None
        for i, existing in enumerate(result):
            same_phone = norm(row.get("whatsapp_clean")) and norm(row.get("whatsapp_clean")) == norm(existing.get("whatsapp_clean"))
            same_links = any(
                is_dedupe_url(row.get(k))
                and norm(row.get(k)) == norm(existing.get(k))
                for k in ["instagram_url", "facebook_url", "linkedin_url", "shopee_url"]
            )
            same_store = norm(row.get("source_platform")) == norm(existing.get("source_platform")) and similar(row.get("store_name"), existing.get("store_name"))
            if same_phone or same_links or same_store:
                duplicate_index = i
                break
        if duplicate_index is None:
            result.append(row)
            continue
        existing = result[duplicate_index]
        existing_score = int(existing.get("lead_score") or 0)
        row_score = int(row.get("lead_score") or 0)
        if row_score > existing_score:
            result[duplicate_index] = merge_rows(row, existing)
        else:
            result[duplicate_index] = merge_rows(existing, row)
    return result


def ensure_row(row, index):
    today = today_date().isoformat()
    for field in FIELDS:
        row.setdefault(field, "")
    row["lead_id"] = norm(row.get("lead_id")) or f"KROG-{today.replace('-', '')}-{index:04d}"
    row["created_at"] = norm(row.get("created_at")) or today
    row["updated_at"] = today
    row["country"] = norm(row.get("country")) or "Brasil"
    row["whatsapp_clean"] = clean_whatsapp(row.get("whatsapp_raw") or row.get("whatsapp_clean"))
    categories, angle = match_category(row)
    row["recommended_krog_category"] = norm(row.get("recommended_krog_category")) or categories
    row["krog_angle"] = norm(row.get("krog_angle")) or angle
    row["whatsapp_message_1"] = norm(row.get("whatsapp_message_1")) or build_message(row)
    name = display_name(row)
    row["whatsapp_followup_d1"] = norm(row.get("whatsapp_followup_d1")) or FOLLOWUPS["D+1"].format(name=name)
    row["whatsapp_followup_d3"] = norm(row.get("whatsapp_followup_d3")) or FOLLOWUPS["D+3"].format(name=name)
    row["whatsapp_followup_d7"] = norm(row.get("whatsapp_followup_d7")) or FOLLOWUPS["D+7"].format(name=name)
    row["lead_score"] = str(score_row(row))
    row["lead_level"] = lead_level(int(row["lead_score"]))
    row["contact_priority"] = {"A": "must_contact_today", "B": "priority", "C": "later", "D": "do_not_contact"}[row["lead_level"]]
    if is_rejected_risk(row):
        row["status"] = "rejeitado"
        row["contact_priority"] = "do_not_contact"
    elif not norm(row.get("status")):
        row["status"] = "contactar" if row["lead_level"] in ("A", "B") else "qualificado" if row["lead_level"] == "C" else "rejeitado"
    row["next_action"] = norm(row.get("next_action")) or ("WhatsApp manual review" if row["lead_level"] in ("A", "B") else "Keep in CRM")
    row["whatsapp_link"] = make_link(row["whatsapp_clean"], row["whatsapp_message_1"])
    return row


def build_followups(rows):
    tasks = []
    today = today_date()
    for row in rows:
        if row.get("lead_level") not in ("A", "B"):
            continue
        for stage, delta, field in [("D+1", 1, "whatsapp_followup_d1"), ("D+3", 3, "whatsapp_followup_d3"), ("D+7", 7, "whatsapp_followup_d7")]:
            tasks.append({
                "task_id": f"{row['lead_id']}-{stage}",
                "lead_id": row["lead_id"],
                "lead_name": row.get("lead_name", ""),
                "store_name": row.get("store_name", ""),
                "whatsapp_clean": row.get("whatsapp_clean", ""),
                "followup_stage": stage,
                "followup_date": (today + timedelta(days=delta)).isoformat(),
                "message": row.get(field, ""),
                "status": "pending",
                "notes": "",
            })
    return tasks


def main():
    rows = read_rows(LEADS_PATH)
    processed = [ensure_row(dict(row), index + 1) for index, row in enumerate(rows)]
    processed = dedupe(processed)
    processed = [ensure_row(row, index + 1) for index, row in enumerate(processed)]
    today_rows = [
        row for row in processed
        if row.get("lead_level") in ("A", "B")
        and row.get("whatsapp_clean")
        and row.get("status") != "rejeitado"
        and not is_rejected_risk(row)
    ]
    rejected_rows = []
    for row in processed:
        if row.get("lead_level") == "D" or row.get("status") == "rejeitado" or is_rejected_risk(row):
            rejected = dict(row)
            rejected["rejection_reason"] = norm(row.get("risk_flag")) or "lead_score_below_50"
            rejected_rows.append(rejected)
    write_rows(LEADS_PATH, processed, FIELDS)
    write_rows(TODAY_PATH, today_rows, FIELDS)
    write_rows(REJECTED_PATH, rejected_rows, FIELDS + ["rejection_reason"])
    write_rows(FOLLOWUP_PATH, build_followups(today_rows), [
        "task_id", "lead_id", "lead_name", "store_name", "whatsapp_clean",
        "followup_stage", "followup_date", "message", "status", "notes",
    ], FOLLOWUP_LABELS)
    print(f"Processed {len(processed)} leads")
    print(f"Today contact list: {len(today_rows)}")
    print(f"Rejected leads: {len(rejected_rows)}")


if __name__ == "__main__":
    main()
