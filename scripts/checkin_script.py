import csv
import json
import os
import sys
from datetime import datetime
from collections import defaultdict

ARQUIVO = r"C:\Users\jo_da\OneDrive\Área de Trabalho\Gestão\Check-ins\Operação _ Batista&Co. - Check-ins.csv"
DATA_CORTE_STR = "20/04/2026"

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
