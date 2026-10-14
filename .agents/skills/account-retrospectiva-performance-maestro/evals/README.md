# Avaliação preparada

Os três casos de `evals.json` cobrem:

1. Inside sales com CRM, vendedores, conversas e break-even ausente.
2. E-commerce multicanal com GA4, loja, produtos e criativos.
3. Cliente sem repositório ou definições, exigindo sabatina adaptativa.

Nesta primeira implementação foram executados testes determinísticos de contrato, fórmulas textuais, atribuição, SLA útil e duplo-write. A avaliação qualitativa completa será executada quando o cliente-piloto e o período forem informados, pois o valor principal da skill depende da reconciliação de fontes reais.

O pacote local de `criador-de-skills` não contém `eval-viewer/generate_review.py`; por isso não foi gerado um viewer estático nesta etapa. Não substituir por HTML artesanal. Quando o recurso estiver disponível, gerar o viewer oficial a partir destes casos.
