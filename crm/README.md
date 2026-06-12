# KROG B2B CRM 工作台

本文件夹用于 KROG 巴西 B2B 精准获客。当前阶段只创建结构、规则和本地工具，不开始大量搜索。

## 文件

- `leads.csv`：主 CRM 线索库
- `today_contact_list.csv`：今日 A/B 级优先联系名单
- `rejected_leads.csv`：不建议联系或 D 级线索
- `followup_tasks.csv`：D+1 / D+3 / D+7 跟进任务
- `lead_scoring_rules.md`：评分规则
- `message_templates_ptbr.md`：巴西葡语 WhatsApp 话术模板
- `krog_product_matching.md`：KROG 类目匹配逻辑
- `daily_workflow.md`：每日执行流程
- `index.html`：本地 CRM 看板
- `lead_processor.py`：CSV 清洗、评分、话术和导出脚本

## 使用方式

1. 把公开来源找到的线索追加到 `leads.csv`
2. 运行 `python lead_processor.py`
3. 查看 `today_contact_list.csv`
4. 用 `index.html` 导入 `leads.csv` 或 `today_contact_list.csv` 查看、筛选和复制话术

## 当前账号确认

已由用户确认当前允许 Chrome 账号为：Simth Duke / sduke5186@gmail.com

## 禁止动作

不登录 WhatsApp，不发送 WhatsApp，不私信、不关注、不点赞、不评论、不提交表单、不切换账号、不处理验证码。
