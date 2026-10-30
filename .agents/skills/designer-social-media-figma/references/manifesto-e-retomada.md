# Manifesto e Retomada

Mantenha um registro estruturado privado do lote no diretorio de trabalho do cliente. Isso permite retomar a tarefa sem depender de lembrar o chat inteiro.

## Dados do Lote

- Cliente, mes/ano, modo e escopo autorizado.
- Miro: URL, frame mensal e itens lidos.
- Figma: arquivo, pagina, secao, sessao e IDs.
- Perfil visual: fontes, pesos, cores, logo, referencias abertas e encerramento.
- Posts, cards, assets e estado das etapas.

## Registro Por Post

```json
{
  "date": "04.11",
  "type": "carousel",
  "status": "brief_read",
  "source_item_ids": [],
  "caption_original": null,
  "figma_group_id": null,
  "cards": [
    {
      "number": 1,
      "source_item_ids": [],
      "headline_original": null,
      "body_original": null,
      "cta_original": null,
      "visual_brief_original": null,
      "annotations_original": [],
      "applied_copy": null,
      "copy_corrections": [],
      "image": {
        "provider": null,
        "prompt_original": null,
        "prompt_enriched": null,
        "reference_files": [],
        "local_path": null,
        "upload_path": null,
        "status": "pending",
        "target_node_id": null,
        "image_hash": null
      },
      "figma_frame_id": null,
      "qa": {
        "copy_checked": false,
        "fonts_checked": false,
        "image_applied": false,
        "visual_checked": false,
        "preview_path": null,
        "issues": []
      }
    }
  ]
}
```

Use `static` para um post unico. Nao copiar a contagem do exemplo: posts e cards sao entidades diferentes.

Estados uteis: `brief_read`, `structure_created`, `images_ready`, `composed`, `qa_passed`, `delivered`. Registre falhas e pendencias separadamente. Nao concluir uma etapa somente porque foi iniciada.

## Copy

Preserve original e origem. Correcoes evidentes de digitacao/concordancia podem ser aplicadas quando nao mudam sentido, numero ou promessa; registre antes/depois e informe no andamento. Preserve copy que o usuario exigir como literal.

Trocar headline, numero, beneficio, contagem ou direcao visual nao e revisao gramatical. Resolva a divergencia antes de produzir o post afetado.

Legendas podem ficar no manifesto e na entrega complementar. Nao inserir briefing ou legenda como card extra no canvas.

## Retomar ou Atualizar

1. Leia manifesto e orientacao mais recente.
2. Releia o Miro para as datas afetadas.
3. Confira IDs e conteudo atual do Figma, incluindo ajustes manuais.
4. Compare a mudanca com o estado atual, sem restaurar versoes antigas por padrao.
5. Atualize somente cards e imagens afetados.
6. Revise e substitua as previas correspondentes.

O link mais recente prevalece sobre o registrado anteriormente. Nao insistir em um arquivo antigo.

A skill compartilhada contem apenas processo e exemplos ficticios. Clientes reais, URLs privadas, chaves de arquivo, fotos, prompts privados e outputs pertencem ao contexto do cliente; nao embutir esses dados no pacote.
