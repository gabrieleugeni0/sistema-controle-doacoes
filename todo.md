# TODO

## Fase 1: Análise das novas funcionalidades e planejamento da arquitetura
- [x] Analisar todas as novas funcionalidades e correções solicitadas.
- [ ] Planejar as modificações no esquema do banco de dados.
- [ ] Planejar as modificações nas classes de modelo.
- [ ] Planejar as modificações na interface gráfica (Tkinter).

## Fase 2: Atualização do esquema do banco de dados e modelos
- [x] Modificar a tabela `beneficiarios` para incluir os campos `alimento_necessidade_1`, `alimento_necessidade_2`, `alimento_necessidade_3`.
- [x] Atualizar as classes de modelo (`models.py`) para refletir as mudanças no banco de dados e adicionar métodos auxiliares para as novas funcionalidades.

## Fase 3: Implementação das validações de telefone e e-mail
- [x] Implementar validação de telefone (somente números, formato DDD+número) para doadores e beneficiários.
- [x] Implementar validação de e-mail para doadores e beneficiários.

## Fase 4: Aprimoramento das abas de Doadores e Beneficiários
- [x] Atualizar a interface da aba de Doadores para incluir a descrição do telefone.
- [x] Atualizar a interface da aba de Beneficiários para incluir os 3 campos de necessidade de alimentos e a descrição do telefone.



## Fase 5: Aprimoramento da aba de Doações Recebidas
- [x] Implementar a lógica para buscar doadores por nome e preencher o Combobox.
- [x] Trocar a descrição de "Nome do Item" para "Tipo de Alimento" e fornecer uma lista com os tipos já cadastrados, permitindo entrada livre.
- [x] Fazer o mesmo para o campo "Marca".
- [x] Trocar o formato da "Data de Validade" para DD/MM/YYYY e ajustar a validação.
- [x] Corrigir a validação de ID do Doador, Quantidade e Data de Validade.



## Fase 6: Aprimoramento da aba de Doações Realizadas
- [x] Implementar a lógica para buscar beneficiários por nome e preencher o Combobox.
- [x] Trocar a descrição de "Nome do Item" para "Tipo de Alimento" e fornecer uma lista com os tipos já cadastrados (apenas os que já tiveram entrada).
- [x] Fazer o mesmo para o campo "Marca" (apenas as que já tiveram entrada).
- [x] Trocar o formato da "Data de Validade" para DD/MM/YYYY.
- [x] Implementar validação para não permitir doação caso não haja estoque do alimento.
- [x] Atualizar a aba de Saídas (Doações Realizadas) para exibir os detalhes das doações.



## Fase 7: Criação das abas de Entradas e Saídas
- [x] Criar a aba "Entradas (Doações Recebidas)" para exibir o histórico de doações recebidas.
- [x] Criar a aba "Saídas (Doações Realizadas)" para exibir o histórico de doações realizadas.



## Fase 8: Aprimoramento da aba de Estoque e Alertas de Vencimento
- [x] Na aba de estoque, agrupar por tipo de alimento, com quantidade agrupada por tipo, independente de marca.
- [x] No alerta de vencimento, incluir apenas alimentos com vencimento próximo (30 dias ou menos).



## Fase 9: Testes e validação das novas funcionalidades
- [x] Realizar testes unitários para as classes de modelo de dados.
- [x] Realizar testes manuais da interface gráfica (necessita de ambiente local).



## Fase 10: Atualização da documentação
- [x] Atualizar o `README.md` com as novas funcionalidades.
- [x] Atualizar o `manual_usuario.md` com as novas funcionalidades e instruções de uso.
- [x] Atualizar a `documentacao_tecnica.md` com as mudanças no esquema do banco de dados, classes e fluxo de dados.

