---
name: gestao-checkin-analysis
description: >
  Esta skill deve ser usada quando o usuário pedir para "analisar check-ins",
  "ver check-ins de ontem", "rodar análise diária de check-ins", "como estão os
  clientes hoje", "o que os accounts reportaram", "novos check-ins",
  "análise de tendências dos clientes" ou qualquer leitura dos check-ins
  preenchidos pelos accounts da unidade.
metadata:
  version: "2.0.0"
---

# Análise Diária de Check-ins

Leia os check-ins preenchidos pelos accounts desde a última análise, identifique tendências por cliente, extraia os pontos-chave dos comentários e sugira planos de ação proativos.

> **Importante:** Os check-ins refletem um touch point frequente de relacionamento. Eles NÃO representam a avaliação final do cliente, que é composta também por NPS, Quality Check e Retrospectivas. Use esses dados para identificar tendências e agir antes que problemas se consolidem.

---

## Configurações fixas

- **Pasta dos arquivos:** `./bases/gestao-checkins/dados`
- **Arquivo de estado:** `./bases/gestao-checkins/dados/.checkin_state.json`
- **Pasta de saída:** `./bases/gestao-checkins/dados/`

---

## Passo 1 — Determinar o período de análise

Use a ferramenta de leitura adequada para ler o arquivo de estado em:
`./bases/gestao-checkins/dados/.checkin_state.json`

- Se o arquivo **existir**, leia o campo `ultima_analise` (formato `YYYY-MM-DD`). Esse será a data de corte.
- Se o arquivo **não existir**, use a data de ontem como ponto de partida.

Guarde essa data como `[DATA_CORTE]` (formato `DD/MM/YYYY` para comparar com o CSV).

---

## Passo 2 — Encontrar o CSV mais recente

Analise o diretório:
`./bases/gestao-checkins/dados`

Encontre todos os arquivos `.csv` e utilize o que possuir a data de modificação mais recente. Guarde o caminho completo do arquivo como `[ARQUIVO_CSV]`.

---

## Passo 3 — Ler e processar o CSV com Python

### 3.1 — Ler o arquivo (ou parte dele)

Abra e leia o arquivo `[ARQUIVO_CSV]`. Este arquivo CSV pode conter descrições longas contendo quebras de linha (multiline fields).

### 3.2 — Salvar em formato temporário para parsing ou rodar script

Execute o seguinte script em Python para extrair e filtrar os resultados. Ele cruza o histórico com os dados novos a partir do corte:

```python
import csv
import json
import os
import sys
from datetime import datetime
from collections import defaultdict

# Pegar argumentos caso o agent queira passar, senão substitui via prompt
ARQUIVO = r"[ARQUIVO_CSV]"
DATA_CORTE_STR = "[DATA_CORTE_DD/MM/YYYY]"

try:
    data_corte = datetime.strptime(DATA_CORTE_STR, "%d/%m/%Y")
except ValueError:
    print("Formato de data inválido. Use DD/MM/YYYY")
    sys.exit(1)

registros = []
with open(ARQUIVO, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            data_str = row.get("Data da Reunião", "").strip()
            if not data_str:
                continue
            data = datetime.strptime(data_str, "%d/%m/%Y")
            registros.append({
                "data": data,
                "data_str": data_str,
                "cliente": row.get("Cliente", "").strip(),
                "account": row.get("Gestor do Projeto", "").strip(),
                "nota_resultado": float(row.get("Nota Resultado", 0) or 0),
                "nota_entrega": float(row.get("Nota Entrega", 0) or 0),
                "nota_relacionamento": float(row.get("Nota Relacionamento", 0) or 0),
                "nota_checkin": float(row.get("Nota Checkin", 0) or 0),
                "media": float(row.get("Média das notas", 0) or 0),
                "observacao": row.get("Observação sobre o Check-in:", "").strip(),
            })
        except Exception:
            continue

# Separar novos e histórico
novos = [r for r in registros if r["data"] >= data_corte]
clientes_novos = {r["cliente"] for r in novos}

historico = [r for r in registros if r["data"] < data_corte and r["cliente"] in clientes_novos]

# Pegar últimos 3 históricos por cliente
historico_por_cliente = defaultdict(list)
for r in sorted(historico, key=lambda x: x["data"], reverse=True):
    if len(historico_por_cliente[r["cliente"]]) < 3:
        historico_por_cliente[r["cliente"]].append(r)

# Médias dos novos
if novos:
    media_nota = sum(r["nota_checkin"] for r in novos) / len(novos)
    media_resultado = sum(r["nota_resultado"] for r in novos) / len(novos)
    media_entrega = sum(r["nota_entrega"] for r in novos) / len(novos)
    media_relacionamento = sum(r["nota_relacionamento"] for r in novos) / len(novos)
else:
    media_nota = media_resultado = media_entrega = media_relacionamento = 0

resultado = {
    "total_novos": len(novos),
    "clientes_analisados": len(clientes_novos),
    "accounts_envolvidos": len({r["account"] for r in novos}),
    "media_nota": round(media_nota, 2),
    "media_resultado": round(media_resultado, 2),
    "media_entrega": round(media_entrega, 2),
    "media_relacionamento": round(media_relacionamento, 2),
    "novos": novos,
    "historico_por_cliente": {k: v for k, v in historico_por_cliente.items()},
    "clientes_atencao": [r for r in novos if r["nota_checkin"] < 3.0],
}

# Serializar datas para JSON
def serialize(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    raise TypeError(f"Type {type(obj)} not serializable")

print(json.dumps(resultado, default=serialize, ensure_ascii=False, indent=2))
```

Salve a saída JSON no buffer da sessão ou arquivo e use os dados extraídos para o próximo passo.

---

## Passo 4 — Montar o relatório HTML

Com base na saída do Python e da sua interpretação inteligente dos comentários, gere o relatório seguindo um design em **HTML responsivo e limpo** para facilitar a leitura. Use a estrutura abaixo como base, mantendo um visual moderno:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  body { font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; background-color: #f8fafc; }
  h1 { color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }
  h2 { color: #1e293b; margin-top: 2rem; }
  table { width: 100%; border-collapse: collapse; margin: 1rem 0; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
  th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #e2e8f0; }
  th { background-color: #f1f5f9; font-weight: 600; }
  .alert { background: #fffbeb; border-left: 4px solid #f59e0b; padding: 1rem; margin: 1rem 0; border-radius: 4px; }
  .danger { background: #fef2f2; border-left: 4px solid #ef4444; padding: 1rem; margin: 1rem 0; border-radius: 4px; }
  .quote { background: #eff6ff; border-left: 4px solid #3b82f6; padding: 1rem; font-style: italic; margin: 1rem 0; }
  .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600; }
  .badge-alta { background: #fee2e2; color: #991b1b; }
  .badge-media { background: #fef3c7; color: #92400e; }
  .badge-baixa { background: #d1fae5; color: #065f46; }
</style>
</head>
<body>

<h1>Análise de Check-ins — [DATA DE HOJE]</h1>
<p><strong>Período:</strong> [DATA_CORTE] a [DATA DE HOJE]<br>
<strong>Check-ins:</strong> N | <strong>Clientes:</strong> X | <strong>Accounts:</strong> Y</p>

<div class="alert">
  ⚠️ Lembrete: check-ins são um indicador de tendência. A avaliação final inclui NPS, Quality Check e Retrospectivas.
</div>

<h2>📊 Panorama Geral</h2>
<table>
  <tr><th>Métrica</th><th>Média do Período</th></tr>
  <tr><td>Nota Geral</td><td>X.X</td></tr>
  <tr><td>Resultado</td><td>X.X</td></tr>
  <tr><td>Entregas</td><td>X.X</td></tr>
  <tr><td>Relacionamento</td><td>X.X</td></tr>
</table>
<p>[Síntese executiva analítica sobre o que o período revela]</p>

<h2>🔴 Clientes em Atenção (Notas < 3.0)</h2>
<div class="danger">Atenção imediata para clientes com sinais críticos.</div>
<table>
  <tr><th>Cliente</th><th>Account</th><th>Data</th><th>Nota</th></tr>
  <!-- iterar clientes em atenção -->
  <tr><td>...</td><td>...</td><td>...</td><td>...</td></tr>
</table>

<h2>📈 Evolução por Cliente</h2>
<!-- Para CADA cliente novo -->
<h3>[Nome do Cliente] — Account: [Nome do Account]</h3>
<table>
  <tr><th>Data</th><th>Nota</th><th>Δ</th></tr>
  <tr><td>[hist -1]</td><td>...</td><td>—</td></tr>
  <tr><td><strong>[NOVO]</strong></td><td>...</td><td>↑/→/↓</td></tr>
</table>
<p><strong>Tendência:</strong> [Frase direta resumindo a tendência de performance técnica vs percepção]</p>

<h2>💬 Destaques</h2>
<!-- Para CADA check-in com observação significativa -->
<h3>[Nome do Cliente]</h3>
<p><strong>Account:</strong> [Account] | <strong>Data:</strong> [Data]</p>
<div class="quote">"[Trecho mais crítico/insight real]"</div>
<ul>
  <li><strong>Pontos:</strong> [Ponto positivo/negativo]</li>
  <li><strong>Leitura:</strong> [SEU diagnóstico de gestor]</li>
</ul>

<h2>✅ Planos de Ação Recomendados</h2>
<table>
  <tr><th>Prioridade</th><th>Cliente</th><th>Ação</th></tr>
  <!-- iterar acoes -->
  <tr><td><span class="badge badge-alta">🔴 Alta</span></td><td>...</td><td>...</td></tr>
</table>

<p style="text-align: center; color: #64748b; margin-top: 3rem; font-size: 0.875rem;">
  Análise gerada em [DATA_HOJE] • Fonte: Arquivo de Check-ins
</p>

</body>
</html>
```

---

## Passo 5 — Salvar o relatório localmente

Escreva e grave o relatório na sua íntegra em formato HTML:
`./bases/gestao-checkins/dados/checkin-[YYYY-MM-DD].html`
(Use a data de hoje para compor o nome).

---

## Passo 6 — Atualizar o estado do Check-in

Salve/Atualize o arquivo de log JSON:
`./bases/gestao-checkins/dados/.checkin_state.json`

```json
{
  "ultima_analise": "YYYY-MM-DD (apenas se executou até hoje com sucesso)",
  "ultimo_arquivo": "checkin-[YYYY-MM-DD].html",
  "csv_utilizado": "[nome completo do arquivo csv usado]",
  "total_checkins_analisados": "[A quantidade de checkins NO RECORTE]"
}
```

---

## Passo 7 — Entrega e Feedback no Chat para Mim (Usuário)

No chat da nossa conversa, não jogue o relatório inteiro. Apenas me entregue de forma condensada:

1. **Resumo em 3 a 4 frases** explicando o sentimento geral da análise.
2. **Planos de ação apenas de 🔴 Alta prioridade** em destaque, dizendo o que eu preciso fazer hoje.
3. **Link rápido para leitura:** Mostre o path clicável para o arquivo HTML usando `file:///` e o caminho absoluto originado a partir de `./bases/gestao-checkins/dados/...`.
4. Pergunte: "Deseja que eu te traga algum detalhamento de algum dos clientes médios/baixos agora?"

---

## 📌 Recomendações e Boas Práticas Comportamentais (Importantíssimo):
- **Não minta informações ou invente clientes.** Extraia apenas dos dados.
- **Ajude nas Entrelinhas:** Os accounts costumam suavizar problemas ("tivemos bons insights mas sem vendas" = inércia comercial / possível churn). Traduza de forma fria para o gestor.
- **Se o campo "observação" de um check-in estiver em branco ou genérico**, não o coloque na aba destaques. Use apenas a tendência fria das notas.
- **Evite planos genéricos** como "Acompanhar de perto". Recomende "Agendar call quinta com Account Fulano para revisar funnel da etapa 3". Tente ser pragmático.
