---
name: gestao-checkin-analysis
description: >
  Esta skill deve ser usada quando o usuário pedir para "analisar check-ins",
  "ver check-ins de ontem", "rodar análise diária de check-ins", "como estão os
  clientes hoje", "o que os accounts reportaram", "novos check-ins",
  "análise de tendências dos clientes" ou qualquer leitura dos check-ins
  preenchidos pelos accounts da unidade.
metadata:
  version: "2.1.0"
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
- **Atenção:** Se o `total_checkins_analisados` do estado for `0` e o arquivo HTML correspondente estiver vazio (0 bytes), significa que a última execução falhou. Nesse caso, recue a data de corte para o dia anterior ao `ultima_analise` registrado, para garantir que check-ins recentes não sejam perdidos.

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

### 3.2 — Rodar o script de processamento

Execute o seguinte script em Python. Ele cruza o histórico com os dados novos a partir do corte. Use `safe_float()` para evitar falhas silenciosas na conversão de notas, e tente múltiplos formatos de data:

```python
import csv
import json
import sys
from datetime import datetime
from collections import defaultdict

ARQUIVO = r"[ARQUIVO_CSV]"
DATA_CORTE_STR = "[DATA_CORTE_DD/MM/YYYY]"

try:
    data_corte = datetime.strptime(DATA_CORTE_STR, "%d/%m/%Y")
except ValueError:
    print("Formato de data inválido. Use DD/MM/YYYY")
    sys.exit(1)

def safe_float(val, default=0.0):
    try:
        v = str(val).strip().replace(",", ".")
        return float(v) if v else default
    except:
        return default

registros = []
with open(ARQUIVO, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            data_str = row.get("Data da Reunião", "").strip()
            if not data_str:
                continue
            data = None
            for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]:
                try:
                    data = datetime.strptime(data_str, fmt)
                    break
                except:
                    pass
            if data is None:
                continue
            registros.append({
                "data": data,
                "data_str": data.strftime("%d/%m/%Y"),
                "cliente": row.get("Cliente", "").strip(),
                "account": row.get("Gestor do Projeto", "").strip(),
                "nota_resultado": safe_float(row.get("Nota Resultado", 0)),
                "nota_entrega": safe_float(row.get("Nota Entrega", 0)),
                "nota_relacionamento": safe_float(row.get("Nota Relacionamento", 0)),
                "nota_checkin": safe_float(row.get("Nota Checkin", 0)),
                "media": safe_float(row.get("Média das notas", 0)),
                "observacao": row.get("Observação sobre o Check-in:", "").strip(),
            })
        except Exception:
            continue

# Separar novos e histórico
novos = [r for r in registros if r["data"] >= data_corte]
clientes_novos = {r["cliente"] for r in novos}

historico = [r for r in registros if r["data"] < data_corte and r["cliente"] in clientes_novos]

# Pegar últimos 3 históricos por cliente em ordem cronológica crescente (para exibir na tabela)
historico_por_cliente = defaultdict(list)
for r in sorted(historico, key=lambda x: x["data"], reverse=True):
    if len(historico_por_cliente[r["cliente"]]) < 3:
        historico_por_cliente[r["cliente"]].append(r)
for k in historico_por_cliente:
    historico_por_cliente[k] = list(reversed(historico_por_cliente[k]))

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
    "clientes_resultado_critico": [r for r in novos if r["nota_resultado"] < 3.0],
}

def serialize(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    raise TypeError(f"Type {type(obj)} not serializable")

print(json.dumps(resultado, default=serialize, ensure_ascii=False, indent=2))
```

Salve a saída JSON no buffer da sessão ou arquivo e use os dados extraídos para o próximo passo.

---

## Passo 4 — Montar o relatório HTML

Com base na saída do Python e da sua interpretação inteligente dos comentários, gere o relatório seguindo um design em **HTML responsivo e limpo**. Use a estrutura abaixo como base:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Análise de Check-ins — [DATA DE HOJE]</title>
<style>
  body { font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.6; color: #333; max-width: 920px; margin: 0 auto; padding: 24px; background-color: #f8fafc; }
  h1 { color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; margin-bottom: 0.4rem; }
  h2 { color: #1e293b; margin-top: 2rem; margin-bottom: 0.5rem; }
  h3 { color: #334155; margin-top: 1.5rem; margin-bottom: 0.3rem; }
  p { margin: 0.4rem 0 0.8rem; }
  table { width: 100%; border-collapse: collapse; margin: 0.8rem 0 1.4rem; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
  th, td { padding: 11px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; font-size: 0.93rem; }
  th { background-color: #f1f5f9; font-weight: 600; color: #475569; }
  tr:last-child td { border-bottom: none; }
  .alert { background: #fffbeb; border-left: 4px solid #f59e0b; padding: 0.85rem 1rem; margin: 1rem 0; border-radius: 4px; font-size: 0.9rem; color: #78350f; }
  .danger { background: #fef2f2; border-left: 4px solid #ef4444; padding: 0.85rem 1rem; margin: 0.5rem 0 1rem; border-radius: 4px; }
  .info { background: #f0fdf4; border-left: 4px solid #22c55e; padding: 0.85rem 1rem; margin: 0.5rem 0 1rem; border-radius: 4px; }
  .quote { background: #eff6ff; border-left: 4px solid #3b82f6; padding: 0.9rem 1rem; font-style: italic; margin: 0.8rem 0; border-radius: 4px; color: #1e3a8a; }
  .badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.82rem; font-weight: 600; }
  .badge-alta { background: #fee2e2; color: #991b1b; }
  .badge-media { background: #fef3c7; color: #92400e; }
  .badge-baixa { background: #d1fae5; color: #065f46; }
  .nota-critica { color: #dc2626; font-weight: 700; }
  .nota-ok { color: #16a34a; font-weight: 600; }
  .nota-media { color: #d97706; font-weight: 600; }
  .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 1rem 0 1.5rem; }
  .kpi-card { background: #fff; border-radius: 8px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }
  .kpi-label { font-size: 0.78rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.04em; }
  .kpi-value { font-size: 1.9rem; font-weight: 700; color: #0f172a; margin: 4px 0 0; }
  .section-card { background: #fff; border-radius: 8px; padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin: 1rem 0; }
  /* Linhas de observação inline nas tabelas de evolução */
  .obs-row td { background: #f8fafc; font-size: 0.83rem; color: #475569; font-style: italic; padding: 6px 15px 10px 15px; border-bottom: 1px solid #e2e8f0; }
  .obs-row td span { font-style: normal; font-weight: 600; color: #94a3b8; margin-right: 4px; }
  .obs-vazia td { background: #f8fafc; font-size: 0.83rem; color: #cbd5e1; font-style: italic; padding: 6px 15px 10px 15px; border-bottom: 1px solid #e2e8f0; }
  .trend-stable { color: #64748b; }
  .footer { text-align: center; color: #94a3b8; margin-top: 3rem; font-size: 0.82rem; border-top: 1px solid #e2e8f0; padding-top: 1.2rem; }
</style>
</head>
<body>

<h1>📋 Análise de Check-ins — [DATA DE HOJE]</h1>
<p style="color:#64748b; font-size:0.9rem;">
  <strong>Período:</strong> [DATA_CORTE] a [DATA DE HOJE] &nbsp;|&nbsp;
  <strong>Check-ins:</strong> N &nbsp;|&nbsp;
  <strong>Clientes:</strong> X &nbsp;|&nbsp;
  <strong>Accounts:</strong> Y
</p>

<div class="alert">
  ⚠️ <strong>Lembrete:</strong> Check-ins são um indicador de tendência. A avaliação final do cliente inclui NPS, Quality Check e Retrospectivas. Use estes dados para agir preventivamente.
</div>

<!-- PANORAMA GERAL — usar cards KPI, não tabela simples -->
<h2>📊 Panorama Geral</h2>
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">Nota Check-in</div>
    <div class="kpi-value" style="color:[COR_CHECKIN];">[MEDIA_CHECKIN]</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Resultado</div>
    <div class="kpi-value" style="color:[COR_RESULTADO];">[MEDIA_RESULTADO]</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Entregas</div>
    <div class="kpi-value" style="color:[COR_ENTREGA];">[MEDIA_ENTREGA]</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Relacionamento</div>
    <div class="kpi-value" style="color:[COR_RELAC];">[MEDIA_RELAC]</div>
  </div>
</div>
<div class="section-card">
  <p>[Síntese executiva analítica: o que o período revela, incluindo divergências entre notas de check-in e resultado]</p>
</div>

<!-- RADAR DE ATENÇÃO — inclui check-in < 3.0 E resultado < 3.0 mesmo com check-in OK -->
<h2>🔴 Radar de Atenção</h2>
<div class="danger">
  [Descreva os casos críticos: check-in baixo OU resultado crítico. Nota de resultado < 3.0 deve ser destacada mesmo que a nota de check-in esteja OK.]
</div>
<table>
  <tr>
    <th>Cliente</th><th>Account</th><th>Data</th>
    <th>Nota Check-in</th><th>Nota Resultado</th><th>Nota Entrega</th><th>Nota Relac.</th>
  </tr>
  <!-- iterar clientes_atencao + clientes_resultado_critico (deduplizados) -->
  <tr>
    <td>...</td><td>...</td><td>...</td>
    <td class="nota-[ok|media|critica]">X,X</td>
    <td class="nota-[ok|media|critica]">X,X [🔴|🟡]</td>
    <td>X,X</td><td>X,X</td>
  </tr>
</table>

<!-- EVOLUÇÃO POR CLIENTE — com comentários históricos inline -->
<h2>📈 Evolução por Cliente</h2>
<!-- Para CADA cliente novo, criar um section-card -->
<div class="section-card">
  <h3>[Nome do Cliente] — Account: [Nome do Account]</h3>
  <table>
    <tr><th>Data</th><th>Check-in</th><th>Resultado</th><th>Entrega</th><th>Relac.</th><th>Δ Resultado</th></tr>

    <!-- Para cada check-in histórico (ordem cronológica crescente): -->
    <tr>
      <td>[DATA_HIST]</td>
      <td>[nota_checkin]</td>
      <td class="nota-[ok|media|critica]">[nota_resultado]</td>
      <td>[nota_entrega]</td>
      <td>[nota_relacionamento]</td>
      <td class="trend-stable">— / ↑ / → / ↓</td>
    </tr>
    <!-- SEMPRE adicionar linha de observação após cada linha de dados -->
    <!-- Se a observação existir: -->
    <tr class="obs-row">
      <td colspan="6">
        <span>Obs:</span> "[texto da observação]" — <em>[seu comentário editorial se relevante]</em>
      </td>
    </tr>
    <!-- Se a observação estiver vazia: -->
    <tr class="obs-vazia">
      <td colspan="6"><span>Obs:</span> sem observação registrada. <em style="color:#dc2626;">[adicionar nota se a queda de nota coincidir com ausência de obs]</em></td>
    </tr>

    <!-- Linha do check-in NOVO (destacada) -->
    <tr style="background:#fef2f2;"><!-- ou #f0fdf4 se positivo -->
      <td><strong>[DATA_NOVO] ★</strong></td>
      <td class="nota-ok"><strong>[nota_checkin]</strong></td>
      <td class="nota-critica"><strong>[nota_resultado] 🔴</strong></td>
      <td class="nota-ok"><strong>[nota_entrega]</strong></td>
      <td class="nota-ok"><strong>[nota_relacionamento]</strong></td>
      <td style="color:#dc2626; font-weight:700;">↓↓</td>
    </tr>
    <tr class="obs-row" style="background:#fef2f2;">
      <td colspan="6"><span>Obs:</span> "[observação do check-in novo]" — <em>[seu diagnóstico]</em></td>
    </tr>
  </table>
  <p><strong>Tendência:</strong> [Frase direta resumindo a trajetória das notas ao longo do histórico, conectando os comentários à evolução das métricas]</p>
</div>

<!-- DESTAQUES — apenas check-ins com observações significativas -->
<h2>💬 Destaques dos Comentários</h2>
<!-- Para CADA check-in novo com observação não-vazia e não-genérica -->
<div class="section-card">
  <h3>[Nome do Cliente]</h3>
  <p><strong>Account:</strong> [Account] &nbsp;|&nbsp; <strong>Data:</strong> [Data]</p>
  <div class="quote">"[Trecho mais crítico ou revelador da observação]"</div>
  <ul>
    <li><strong>Leitura fria:</strong> [Seu diagnóstico de gestor — traduza suavizações em linguagem direta]</li>
    <li><strong>Risco:</strong> [O que pode acontecer se não houver ação]</li>
  </ul>
</div>

<!-- PLANOS DE AÇÃO -->
<h2>✅ Planos de Ação Recomendados</h2>
<table>
  <tr><th style="width:110px;">Prioridade</th><th>Cliente</th><th>Account</th><th>Ação Específica</th></tr>
  <!-- iterar ações ordenadas por prioridade -->
  <tr>
    <td><span class="badge badge-alta">🔴 Alta</span></td>
    <td>...</td><td>...</td>
    <td>[Ação concreta com dia, pessoa e objetivo — nunca "acompanhar de perto"]</td>
  </tr>
  <tr>
    <td><span class="badge badge-media">🟡 Média</span></td>
    <td>...</td><td>...</td><td>...</td>
  </tr>
</table>

<div class="footer">
  Análise gerada em [DATA_HOJE] &nbsp;•&nbsp; Fonte: [nome do CSV] &nbsp;•&nbsp; [N] check-ins analisados
</div>

</body>
</html>
```

### Regras de cor para os KPI cards:
- Nota ≥ 4,0 → `#16a34a` (verde)
- Nota 3,0–3,9 → `#d97706` (amarelo)
- Nota < 3,0 → `#dc2626` (vermelho)

### Regras para a coluna Δ Resultado:
- Primeira linha → `—`
- Subiu → `↑` (verde)
- Estável → `→` (cinza)
- Caiu 1 ponto → `↓` (vermelho)
- Caiu 2+ pontos → `↓↓` (vermelho negrito)

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
3. **Link rápido para leitura:** Mostre o path clicável usando `computer://` e o caminho absoluto do arquivo HTML.
4. Pergunte: "Deseja que eu te traga algum detalhamento de algum dos clientes médios/baixos agora?"

---

## 📌 Recomendações e Boas Práticas Comportamentais (Importantíssimo):
- **Não minta informações ou invente clientes.** Extraia apenas dos dados.
- **Ajude nas Entrelinhas:** Os accounts costumam suavizar problemas ("tivemos bons insights mas sem vendas" = inércia comercial / possível churn). Traduza de forma fria para o gestor.
- **Se o campo "observação" de um check-in estiver em branco ou genérico**, não o coloque na seção de Destaques. Use apenas a tendência fria das notas.
- **Exiba SEMPRE as observações inline nas tabelas de evolução**, linha por linha — tanto para check-ins históricos quanto para o novo. Se a observação estiver vazia, use a classe `obs-vazia` e indique explicitamente "sem observação registrada". Se a ausência coincide com queda de nota, adicione nota editorial em vermelho.
- **Monitore o Resultado independentemente da nota de check-in.** Um cliente com check-in 4,0 mas resultado 2,0 é crítico e deve aparecer no Radar de Atenção.
- **Evite planos genéricos** como "Acompanhar de perto". Recomende "Agendar call quinta com Account Fulano para revisar funnel da etapa 3". Tente ser pragmático e específico.
