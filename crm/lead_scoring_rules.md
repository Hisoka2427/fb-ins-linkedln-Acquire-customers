# KROG Lead Scoring Rules

## 等级

- A 级：85-100，今天必须联系，进入 `today_contact_list.csv`
- B 级：70-84，优先联系，进入 `today_contact_list.csv`
- C 级：50-69，保留在 `leads.csv`，不进入今日优先名单
- D 级：0-49，仅保留记录，不建议联系

## 加分规则

| 信号 | 分数 |
|---|---:|
| 明确说 `procuro fornecedor` | +30 |
| 明确说 `dropshipping` | +30 |
| 明确说 `quero catálogo` | +25 |
| 明确说 `tenho loja` / `vendo online` | +20 |
| 明确说 `fornecedor confiável` | +30 |
| 明确说 `estou começando` | +10 |
| 明确说 `preciso de produtos` | +20 |
| 有 Shopee 店铺 | +30 |
| 有 Mercado Livre 店铺 | +25 |
| 有 Instagram 店铺 | +15 |
| 有 WhatsApp | +15 |
| 有 loja virtual | +20 |
| LinkedIn 标题含 e-commerce / marketplace / founder / owner / dono / fundador | +20 |
| 主页有持续产品内容 | +15 |
| 近期 30 天内有产品更新 | +15 |
| 类目匹配 KROG 产品 | +20 |
| 类目是 infantil / casa / bolsas / pantufas / moda feminina / utilidades / fitness / ferramentas / banho / cozinha | +20 |
| 公开留下联系方式 | +15 |
| 同时有 Instagram + WhatsApp | +20 |
| 同时有 Shopee + Instagram | +25 |
| 同时有 Shopee + WhatsApp | +30 |
| 有客户评论询价 | +10 |
| 有真实产品图 | +10 |
| 有多个销售渠道 | +15 |

## 扣分规则

| 风险 | 分数 |
|---|---:|
| 只有普通个人主页 | -20 |
| 没有任何联系方式 | -15 |
| 类目完全不匹配 | -20 |
| 疑似同行供应商 | -30 |
| 疑似批发商只找低价货源但无店铺 | -10 |
| 信息不足 | -10 |
| 疑似假号或空号 | -30 |

## 今日名单规则

只把 A/B 级客户放入 `today_contact_list.csv`。C/D 级客户保留在 CRM 中，D 级和不适合客户同步输出到 `rejected_leads.csv`。
