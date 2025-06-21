
## Manual do Usuário

Este manual fornece instruções detalhadas sobre como utilizar o Sistema de Gerenciamento de Estoque de Doações da Sociedade São Vicente de Paula.

### 1. Visão Geral da Interface

Ao iniciar o `app.py`, a janela principal do sistema será exibida. Ela é organizada em abas para facilitar a navegação entre as diferentes funcionalidades:

-   **Doadores:** Para cadastrar e gerenciar pessoas doadoras.
-   **Beneficiários:** Para cadastrar e gerenciar pessoas que recebem doações.
-   **Doações Recebidas:** Para registrar as doações que chegam à ONG.
-   **Doações Realizadas:** Para registrar as doações que são distribuídas pela ONG.
-   **Estoque Atual:** Para visualizar o inventário atual de alimentos.
-   **Entradas (Doações Recebidas):** Para visualizar o histórico de todas as doações recebidas.
-   **Saídas (Doações Realizadas):** Para visualizar o histórico de todas as doações realizadas.
-   **Alertas de Vencimento:** Para verificar itens próximos da data de validade.

### 2. Cadastramento de Doadores

1.  Clique na aba "Doadores".
2.  Preencha os campos "Nome", "Telefone (Ex: (DD)NNNNN-NNNN)", "Email" e "Endereço" do doador.
    -   O campo Telefone aceita somente números e deve seguir o formato (DD)NNNNN-NNNN ou NNNNN-NNNN.
    -   O campo Email deve ser um endereço de e-mail válido.
3.  Clique no botão "Salvar Doador".
4.  O doador será adicionado à lista abaixo e ao banco de dados.

### 3. Cadastramento de Beneficiários

1.  Clique na aba "Beneficiários".
2.  Preencha os campos "Nome", "Telefone (Ex: (DD)NNNNN-NNNN)", "Email" e "Endereço" do beneficiário.
    -   O campo Telefone aceita somente números e deve seguir o formato (DD)NNNNN-NNNN ou NNNNN-NNNN.
    -   O campo Email deve ser um endereço de e-mail válido.
3.  Preencha os campos "Alimento Necessário 1", "Alimento Necessário 2" e "Alimento Necessário 3" com os tipos de alimentos que o beneficiário mais necessita.
4.  Clique no botão "Salvar Beneficiário".
5.  O beneficiário será adicionado à lista abaixo e ao banco de dados.

### 4. Cadastramento de Doações Recebidas

1.  Clique na aba "Doações Recebidas".
2.  **Doador:** Digite o nome do doador no campo e selecione-o na lista que aparece. Se o doador não estiver cadastrado, cadastre-o primeiro na aba "Doadores".
3.  **Tipo de Alimento:** Digite o tipo de alimento (ex: Arroz) ou selecione um tipo já existente na lista. Você pode adicionar novos tipos diretamente aqui.
4.  **Marca:** Digite a marca do alimento (ex: Tio João) ou selecione uma marca já existente na lista. Você pode adicionar novas marcas diretamente aqui.
5.  **Unidade:** Informe a unidade (ex: saco 5 kg, litro).
6.  **Quantidade:** Informe a quantidade recebida (ex: 10 para 10 sacos de 5kg).
7.  **Data de Validade:** Informe a data de validade no formato DD/MM/YYYY (ex: 31/12/2025).
8.  Clique no botão "Registrar Doação Recebida".
9.  A doação será registrada e o estoque será atualizado.

### 5. Cadastramento de Doações Realizadas

1.  Clique na aba "Doações Realizadas".
2.  **Beneficiário:** Digite o nome do beneficiário no campo e selecione-o na lista que aparece. Se o beneficiário não estiver cadastrado, cadastre-o primeiro na aba "Beneficiários".
3.  **Tipo de Alimento:** Selecione o tipo de alimento na lista. Somente alimentos que já foram recebidos e estão em estoque aparecerão aqui.
4.  **Marca:** Selecione a marca do alimento na lista. Somente marcas de alimentos que já foram recebidos e estão em estoque aparecerão aqui.
5.  **Unidade:** Informe a unidade (ex: saco 5 kg, litro).
6.  **Quantidade:** Informe a quantidade doada.
7.  **Validação de Estoque:** O sistema verificará automaticamente se há estoque suficiente para a doação. Se não houver, uma mensagem de erro será exibida.
8.  Clique no botão "Registrar Doação Realizada".
9.  A doação será registrada e o estoque será atualizado.

### 6. Exibição do Estoque Atual

1.  Clique na aba "Estoque Atual".
2.  A tabela exibirá o estoque atual de alimentos, agrupado por "Tipo de Alimento" e "Unidade", mostrando a "Quantidade Total" disponível para cada tipo, independente da marca.

### 7. Entradas (Doações Recebidas)

1.  Clique na aba "Entradas (Doações Recebidas)".
2.  Esta aba exibe um histórico detalhado de todas as doações que foram recebidas, incluindo informações sobre o doador, tipo de alimento, marca, unidade, quantidade, data de recebimento e data de validade.

### 8. Saídas (Doações Realizadas)

1.  Clique na aba "Saídas (Doações Realizadas)".
2.  Esta aba exibe um histórico detalhado de todas as doações que foram realizadas, incluindo informações sobre o beneficiário, tipo de alimento, marca, unidade, quantidade e data da doação.

### 9. Alertas de Vencimento

1.  Clique na aba "Alertas de Vencimento".
2.  Esta aba exibirá automaticamente os itens que estão próximos da data de validade (30 dias ou menos a partir da data atual).

### Dicas de Uso

-   Mantenha os dados de doadores e beneficiários atualizados.
-   Registre as doações recebidas e realizadas imediatamente para manter o estoque preciso.
-   Verifique a aba "Alertas de Vencimento" regularmente para priorizar a distribuição de itens com validade próxima.




