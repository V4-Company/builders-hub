---
name: criativo-gerador-calendario
description: Gera uma planilha Excel formatada com o calendario visual anual de 12 meses (mesclando celulas e cores) para os clientes colarem copys. Use sempre que o usuario pedir para gerar a "grade", "planilha estrutural", ou "calendario" de um cliente novo ou para um ano especifico.
area: criativo
author: v4er
version: 1.0.0
---

# Gerador de Calendário Editorial Visual

Essa skill constrói uma planilha Excel nativa (`.xlsx`) com toda a estrutura visual de 12 meses de um ano. Ela é formatada perfeitamente com células mescladas (2 colunas por dia), cores vermelhas no cabeçalho e 5 linhas extras para suportar textos longos de social media (copys) de cada dia.

## Quando utilizar
Utilize essa skill sempre que o usuário pedir:
- "Gera a grade de calendário pro cliente X"
- "Monta o excel do ano de 2026 pro cliente Y"
- "Cria aquele calendário estrutural de social media"

## Fluxo de Execução

1. **Descubra o destino**: Pergunte ao usuário em qual pasta de cliente (ex: `clientes/nome-do-cliente/docs/`) o arquivo deve ser salvo e com qual nome (ex: `Calendario_2026.xlsx`). Se ele não especificar, sugira criar na pasta principal de `docs/` do cliente que ele estiver focado no momento.
2. **Descubra o ano**: Se o usuário não disser, assuma o ano atual.
3. **Execute o script**:
   Rode o script em Python utilizando o `run_command` da seguinte forma:
   
   ```bash
   python .agents/skills/criativo-gerador-calendario/scripts/gerar_calendario.py "clientes/nome-do-cliente/docs/Calendario_2026.xlsx" 2026
   ```

   *(Nota: O script Python está tanto na pasta `.agents` quanto na `.claude` e eles são idênticos. Você pode referenciar qualquer um dos dois.)*

4. **Entregue o resultado**: Se o comando retornar "Excel gerado com sucesso!", avise o usuário onde o arquivo está salvo. Recomende que ele arraste o arquivo gerado para dentro do Google Drive (em *Arquivo > Importar*) para visualizar a grade completa.

## Dependências
Esta skill requer a biblioteca `openpyxl`. Se durante a execução do comando aparecer um erro de `ModuleNotFoundError`, rode `python -m pip install openpyxl` primeiro e então tente novamente.
